import argparse
import asyncio
import os
import platform
import signal
import struct
import subprocess
import sys
from pathlib import Path

import asyncssh

if platform.system() != "Windows":
    import fcntl
    import pty
    import termios


ROOT = Path(__file__).resolve().parent
PORTFOLIO = ROOT / "portfolio.py"
HOST_KEY = ROOT / "ssh_host_key"
DEFAULT_TERM_SIZE = (80, 24, 0, 0)


def set_terminal_size(fd: int, width: int, height: int, pixwidth: int = 0, pixheight: int = 0) -> None:
    if platform.system() == "Windows":
        return
    width = width or DEFAULT_TERM_SIZE[0]
    height = height or DEFAULT_TERM_SIZE[1]
    size = struct.pack("HHHH", height, width, pixheight, pixwidth)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, size)


def plain_fallback() -> str:
    return (
        "\r\nNano's terminal portfolio needs a Linux PTY to render the full Textual UI.\r\n"
        "Run this server on Linux, Docker, Fly.io, or a VM, then connect with:\r\n\r\n"
        "  ssh nano@yourdomain -p 2222\r\n\r\n"
        "Press q after connecting to quit.\r\n"
    )


class PortfolioSession(asyncssh.SSHServerSession):
    def __init__(self) -> None:
        self.chan = None
        self.master_fd = None
        self.process = None
        self.reader_task = None
        self.term_type = "xterm-256color"
        self.term_size = DEFAULT_TERM_SIZE

    def connection_made(self, chan) -> None:
        self.chan = chan

    def pty_requested(self, term_type, term_size, term_modes) -> bool:
        self.term_type = term_type or self.term_type
        self.term_size = term_size or self.term_size
        return True

    def terminal_size_changed(self, width, height, pixwidth, pixheight) -> None:
        self.term_size = (width, height, pixwidth, pixheight)
        if self.master_fd is not None:
            set_terminal_size(self.master_fd, width, height, pixwidth, pixheight)
        if self.process and platform.system() != "Windows":
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGWINCH)
            except ProcessLookupError:
                pass

    def shell_requested(self) -> bool:
        if platform.system() == "Windows":
            self.chan.write(plain_fallback().encode())
            self.chan.exit(0)
            return True

        width, height, pixwidth, pixheight = self.term_size
        width = width or DEFAULT_TERM_SIZE[0]
        height = height or DEFAULT_TERM_SIZE[1]
        self.master_fd, slave_fd = pty.openpty()
        set_terminal_size(self.master_fd, width, height, pixwidth, pixheight)

        env = os.environ.copy()
        env.update(
            {
                "TERM": self.term_type,
                "COLUMNS": str(width),
                "LINES": str(height),
                "TEXTUAL_COLOR_SYSTEM": "truecolor",
            }
        )

        self.process = subprocess.Popen(
            [sys.executable, str(PORTFOLIO)],
            cwd=ROOT,
            env=env,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            start_new_session=True,
        )
        os.close(slave_fd)
        self.reader_task = asyncio.create_task(self._read_from_pty())
        return True

    def exec_requested(self, command) -> bool:
        return self.shell_requested()

    def data_received(self, data, datatype) -> None:
        if self.master_fd is None:
            return
        if isinstance(data, str):
            data = data.encode()
        try:
            os.write(self.master_fd, data)
        except OSError:
            self.close()

    def eof_received(self) -> bool:
        self.close()
        return False

    def connection_lost(self, exc) -> None:
        self.close()

    async def _read_from_pty(self) -> None:
        loop = asyncio.get_running_loop()
        try:
            while True:
                data = await loop.run_in_executor(None, os.read, self.master_fd, 4096)
                if not data:
                    break
                self.chan.write(data)
        except OSError:
            pass
        finally:
            exit_status = self.process.poll() if self.process else 0
            self.close(cancel_reader=False)
            if self.chan:
                self.chan.exit(exit_status or 0)

    def close(self, cancel_reader: bool = True) -> None:
        if cancel_reader and self.reader_task and not self.reader_task.done():
            self.reader_task.cancel()
        if self.process and self.process.poll() is None:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None


class PortfolioSSHServer(asyncssh.SSHServer):
    def connection_requested(self, dest_host, dest_port, orig_host, orig_port):
        return False

    def begin_auth(self, username) -> bool:
        return False

    def session_requested(self):
        return PortfolioSession()


async def ensure_host_key() -> None:
    if not HOST_KEY.exists():
        key = asyncssh.generate_private_key("ssh-rsa")
        HOST_KEY.write_text(key.export_private_key().decode(), encoding="utf-8")
        os.chmod(HOST_KEY, 0o600)


async def start_server(host: str, port: int) -> None:
    await ensure_host_key()
    await asyncssh.create_server(
        PortfolioSSHServer,
        host,
        port,
        server_host_keys=[str(HOST_KEY)],
        encoding=None,
        line_editor=False,
    )
    print(f"Portfolio SSH server listening on {host}:{port}")
    await asyncio.Future()


def parse_args():
    parser = argparse.ArgumentParser(description="Serve the Textual portfolio over SSH.")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "2222")))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        asyncio.run(start_server(args.host, args.port))
    except (OSError, asyncssh.Error) as exc:
        sys.exit(f"SSH server failed: {exc}")


if __name__ == "__main__":
    main()
