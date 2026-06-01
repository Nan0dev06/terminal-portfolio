# Terminal SSH Portfolio

An SSH portfolio that opens a Textual TUI instead of a normal shell.

Visitors connect with:

```bash
ssh nano@yourdomain -p 2222
```

Inside the portfolio:

- `t` cycles color themes
- `q` quits

## Why This Backend Works

Textual needs a real PTY so it can detect terminal size, colors, and keyboard input. The SSH backend in `ssh_server.py` accepts the SSH session, creates a Linux pseudo-terminal, starts `portfolio.py` inside that PTY, and bridges input/output between the visitor and the app.

That means the full TUI runs correctly on Linux hosts and containers. On Windows, the server shows a small fallback message because Windows does not provide the same PTY behavior for this setup.

## Run Locally

The full SSH experience should be tested on Linux, WSL, or Docker:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ssh_server.py
```

Then connect from another terminal:

```bash
ssh nano@localhost -p 2222
```

The server intentionally allows any username and does not ask for a password because this is a public portfolio, not a login shell.

## Free/Easy Hosting Options

GitHub is good for storing the code, but it cannot host a public raw SSH service by itself. Termius is an SSH client, so it helps you connect from desktop/mobile, but it is not a server host.

Good options for this project:

- Google Cloud Free Tier e2-micro VM, because it is a Linux VM with a public IP and can expose TCP port `2222`.
- Oracle Cloud Free Tier Ubuntu VM, if you regain access and want the most generous always-free VM.
- Fly.io, because it can expose a TCP service and deploy directly from this Dockerfile, but new accounts should treat it as low-cost/trial rather than guaranteed permanent free.
- Any small Linux VPS or free student VM that lets you expose TCP port `2222`.

## Deploy To An Ubuntu VM

Use this path for Google Cloud, Oracle Cloud, or any Ubuntu VPS:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv
git clone https://github.com/YOUR_USERNAME/terminal-portfolio.git
cd terminal-portfolio
bash deploy/install_ubuntu.sh
```

Open inbound TCP port `2222` in the cloud firewall, then connect:

```bash
ssh nano@YOUR_SERVER_IP -p 2222
```

The service is installed as `nano-portfolio` and starts on boot.

## Deploy To Fly.io

1. Install the Fly CLI.
2. Log in with `fly auth login`.
3. From this project folder, run:

```bash
fly launch --no-deploy
fly deploy
```

If Fly asks about the app name, either keep `nano-terminal-portfolio` or choose a unique name. After deploy:

```bash
ssh nano@nano-terminal-portfolio.fly.dev -p 2222
```

For a custom domain, point it at Fly and keep using port `2222` unless your host supports forwarding port `22`.
