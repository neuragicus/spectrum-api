#!/bin/bash

# Install appropriate dependencies based on the environment
case "$1" in
    "app")
        exec gunicorn --workers=1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
        ;;
    "test")
        # Install test dependencies if not already installed
        poetry install --only=test --no-interaction --no-ansi
        echo "Running tests..."
        exec pytest -v
        ;;
esac
