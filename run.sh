#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

MAX_PORT="${MAX_PORT:-5100}"

port_in_use() {
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

echo "Starting Quotes Recommendation Chatbot with Docker..."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Switching to local NLP mode..."
  exec ./run_local.sh
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not running. Switching to local NLP mode..."
  exec ./run_local.sh
fi

# Choose a free host port for web UI if 5000 is occupied.
REQUESTED_WEB_PORT="${WEB_PORT:-5000}"
if port_in_use "$REQUESTED_WEB_PORT"; then
  FREE_WEB_PORT="$(find_free_port "$((REQUESTED_WEB_PORT + 1))" || true)"
  if [ -z "$FREE_WEB_PORT" ]; then
    echo "No free port available between ${REQUESTED_WEB_PORT} and ${MAX_PORT}. Switching to local NLP mode..."
    exec ./run_local.sh
  fi
  export WEB_PORT="$FREE_WEB_PORT"
  echo "Port ${REQUESTED_WEB_PORT} is busy. Docker web UI will use http://localhost:${WEB_PORT}"
else
  export WEB_PORT="$REQUESTED_WEB_PORT"
fi

if docker compose version >/dev/null 2>&1; then
  docker compose up --build
elif command -v docker-compose >/dev/null 2>&1; then
  docker-compose up --build
else
  echo "Docker Compose is not available. Switching to local NLP mode..."
  exec ./run_local.sh
fi
