#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
MAX_PORT="${MAX_PORT:-5100}"

port_in_use() {
  # lsof is available on macOS and most Linux distros.
  lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
}

find_free_port() {
  port="$1"
  while [ "$port" -le "$MAX_PORT" ]; do
    if ! port_in_use "$port"; then
      echo "$port"
      return 0
    fi
    port=$((port + 1))
  done
  return 1
}

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: Python is not installed. Install Python 3.10+ and retry."
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$PYTHON_BIN" -m venv .venv
fi

# shellcheck disable=SC1091
. .venv/bin/activate

python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt

export FORCE_LOCAL_NLP=1
REQUESTED_PORT="${FLASK_PORT:-5000}"
if port_in_use "$REQUESTED_PORT"; then
  FREE_PORT="$(find_free_port "$((REQUESTED_PORT + 1))" || true)"
  if [ -z "$FREE_PORT" ]; then
    echo "Error: no free port available between ${REQUESTED_PORT} and ${MAX_PORT}."
    exit 1
  fi
  export FLASK_PORT="$FREE_PORT"
  echo "Port ${REQUESTED_PORT} is busy. Using port ${FLASK_PORT}."
else
  export FLASK_PORT="$REQUESTED_PORT"
fi

echo "Starting Quotes Recommendation Chatbot in local NLP mode on http://localhost:${FLASK_PORT}"
python app.py
