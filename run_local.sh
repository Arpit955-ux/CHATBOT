#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"

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
export FLASK_PORT="${FLASK_PORT:-5000}"

echo "Starting Quotes Recommendation Chatbot in local NLP mode on http://localhost:${FLASK_PORT}"
python app.py
