#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${PORT:-22}"
SERVICE_FILE="/etc/systemd/system/nano-portfolio.service"
TMP_SERVICE="$(mktemp)"

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/.venv/bin/python" -m pip install -r "$APP_DIR/requirements.txt"

sed \
  -e "s|__APP_DIR__|$APP_DIR|g" \
  -e "s|__USER__|$USER|g" \
  -e "s|__PORT__|$PORT|g" \
  "$APP_DIR/deploy/nano-portfolio.service" > "$TMP_SERVICE"

sudo mv "$TMP_SERVICE" "$SERVICE_FILE"
sudo systemctl daemon-reload
sudo systemctl enable nano-portfolio
sudo systemctl restart nano-portfolio

echo "Nano portfolio SSH server is running on port $PORT."
echo "Open TCP port $PORT in your cloud firewall, then connect with:"
if [ "$PORT" = "22" ]; then
  echo "ssh nano@YOUR_SERVER_IP"
else
  echo "ssh nano@YOUR_SERVER_IP -p $PORT"
fi
