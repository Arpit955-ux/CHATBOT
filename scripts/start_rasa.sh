#!/bin/sh
set -eu

cd /app

if ! ls models/*.tar.gz >/dev/null 2>&1; then
  echo "No trained model found. Training a new model..."
  rasa train
fi

echo "Starting Rasa server on port 5005..."
exec rasa run --enable-api --cors "*" --port 5005
