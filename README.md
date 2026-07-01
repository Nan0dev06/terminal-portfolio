<h1 align="center">nano · terminal portfolio</h1>

<p align="center">
  My portfolio isn't a website you scroll — it's a terminal you connect to.<br>
  A <a href="https://textual.textualize.io/">Textual</a> TUI that greets visitors right inside their own terminal.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-00FF41?style=flat-square&logo=python&logoColor=white">
  <img alt="Textual" src="https://img.shields.io/badge/TUI-Textual-00FF41?style=flat-square">
  <img alt="asyncssh" src="https://img.shields.io/badge/SSH-asyncssh-00FF41?style=flat-square">
</p>

---

## What is this?

This is my personal portfolio, built as a **terminal user interface (TUI)** instead of a web page — my first Python project. It shows an ASCII portrait, an animated intro, a typing bio, and my links, all rendered in a matrix-green terminal aesthetic with switchable themes.

It runs two ways:

- **Locally** — just run the app and it fills your terminal.
- **Over SSH** — deployed on a server, anyone can connect with a single `ssh` command and the portfolio opens in *their* terminal. No website, no browser.

## Features

- 🎨 **Six themes**, toggle live — matrix-green (custom), Nord, Gruvbox, Tokyo Night, Textual Dark, Atom One Dark
- 🖼️ **ASCII portrait** generated from a photo
- ⭐ Animated title with twinkling stars + a typing-effect bio
- 🔗 Clickable GitHub / LinkedIn / email links
- 🔐 **SSH backend** that serves the full TUI to remote visitors — no login, no password

## Controls

| Key | Action        |
|-----|---------------|
| `t` | Cycle themes  |
| `q` | Quit          |

## Run it locally

You only need Python. This shows the portfolio directly in your terminal (no SSH involved):

```bash
# clone, then from the project folder:
python -m venv .venv

# Windows
.\.venv\Scripts\python.exe -m pip install textual==8.2.8 pyfiglet==1.0.2
.\.venv\Scripts\python.exe portfolio.py

# macOS / Linux
source .venv/bin/activate
pip install textual==8.2.8 pyfiglet==1.0.2
python portfolio.py
```

## How the SSH version works

A normal SSH login drops you into a shell. This one drops you into the portfolio instead.

```
visitor types  ssh nano@<host>
        │
        ▼
ssh_server.py accepts the connection (no auth — it's public)
        │
        ▼
it opens a Linux PTY and launches portfolio.py inside it
        │
        ▼
keystrokes + screen output are bridged both ways
        │
        ▼
the full TUI renders in the visitor's terminal
```

Textual needs a real PTY (pseudo-terminal) to detect size, colors, and input — which is why the SSH server must run on **Linux / Docker / a VM**. On Windows it prints a short fallback message instead, because Windows doesn't provide the same PTY behavior.

## Tech stack

| Piece            | Tool                          |
|------------------|-------------------------------|
| TUI framework    | [Textual](https://textual.textualize.io/) |
| ASCII title      | [pyfiglet](https://github.com/pwaller/pyfiglet) |
| SSH server       | [asyncssh](https://asyncssh.readthedocs.io/) |
| Portrait art     | [Pillow](https://python-pillow.org/) (`ascii_art.py`) |

## Deploying it publicly (optional)

The app works locally without any of this. To let strangers connect over SSH, the server needs to run on a machine with a public IP.

<details>
<summary><b>Ubuntu VM (Google Cloud, Oracle Cloud, any VPS)</b></summary>

```bash
sudo apt update && sudo apt install -y git python3 python3-venv
git clone https://github.com/Nan0dev06/terminal-portfolio.git
cd terminal-portfolio
bash deploy/install_ubuntu.sh
```

The installer defaults to port `22`, sets up a `systemd` service, and starts on boot. Open inbound TCP port `22` in the cloud firewall, then visitors connect with `ssh nano@YOUR_SERVER_IP`.
</details>

<details>
<summary><b>Fly.io (Docker)</b></summary>

```bash
fly launch --no-deploy   # reads fly.toml
fly deploy
```

`fly.toml` maps external port `22` → container `2222`, so the connect command stays clean: `ssh nano@<app>.fly.dev`.
</details>

## Project layout

```
portfolio.py            the Textual TUI (the portfolio itself)
portfolio.tcss          styles
ssh_server.py           SSH backend that serves the TUI over a PTY
ascii_art.py            turns a photo into the ASCII portrait
docs/index.html         landing page with the copyable connect command
deploy/                 Ubuntu installer + systemd service
Dockerfile / fly.toml   container + Fly.io deploy config
```

---

<p align="center">
  Built by <b>Nour Al Shami</b> · CS student, heading toward AI engineering<br>
  <a href="https://github.com/Nan0dev06">GitHub</a> · <a href="https://www.linkedin.com/in/nour-al-shami-3701a037a/">LinkedIn</a>
</p>
