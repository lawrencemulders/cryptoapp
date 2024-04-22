#!/bin/bash

# Directory containing Dockerfile
SCRIPT_DIR=$(dirname "$0")
DOCKERFILE_DIR="$SCRIPT_DIR"

# Name of Docker image
IMAGE_NAME="cryptoapp-image"

# Initialize plist file
PYTHON_SCRIPT="$DOCKERFILE_DIR/generate_plist_launchd.py"
python "$PYTHON_SCRIPT"

# Build Docker image
docker build -t "$IMAGE_NAME" "$DOCKERFILE_DIR"

# Load plist file into launchd
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$LAUNCHD_DIR/launchd_job.plist"

if [ -f "$PLIST_FILE" ]; then
    launchctl load "$PLIST_FILE"
    echo "Launchd job loaded successfully."
else
    echo "Error: Launchd plist file '$PLIST_FILE' not found."
    exit 1
fi
