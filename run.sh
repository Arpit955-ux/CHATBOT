#!/usr/bin/env sh
set -eu

echo "Starting Quotes Recommendation Chatbot with Docker..."

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: Docker is not installed. Install Docker Desktop first."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Error: Docker daemon is not running. Start Docker Desktop and retry."
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  docker compose up --build
elif command -v docker-compose >/dev/null 2>&1; then
  docker-compose up --build
else
  echo "Error: Docker Compose is not available."
  echo "Install Docker Compose plugin or docker-compose."
  exit 1
fi
