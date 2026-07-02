#!/bin/bash

set -e

VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
  source $VENV_DIR/bin/activate
fi

echo "Starting server..."

uvicorn src.main:app \
  --reload \
  --host 127.0.0.1 \
  --port 8000