#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting Quotes Recommendation Chatbot with Docker..."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Switching to local NLP mode..."
  exec ./run_local.sh
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not running. Switching to local NLP mode..."
  exec ./run_local.sh
fi

if docker compose version >/dev/null 2>&1; then
  docker compose up --build
elif command -v docker-compose >/dev/null 2>&1; then
  docker-compose up --build
else
  echo "Docker Compose is not available. Switching to local NLP mode..."
  exec ./run_local.sh
fi
