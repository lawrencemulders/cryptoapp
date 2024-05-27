#!/bin/bash

# Define the image name
IMAGE_NAME="cryptoapp-image"

# Path to the plist file
PLIST_FILE="$HOME/Library/LaunchAgents/launchd_job.plist"

# Check if the plist file exists. If so, delete
if [ -f "$PLIST_FILE" ]; then
    echo "Plist file already exists. Deleting..."
    rm "$PLIST_FILE"
fi

# Initialize plist file
PYTHON_SCRIPT="generate_plist_launchd.py"
python "$PYTHON_SCRIPT"

# Navigate to the root directory
cd "$(dirname "$0")"/..

# Build Docker image if no image exists yet
docker build -t "$IMAGE_NAME" -f docker/Dockerfile .

# Run Docker container with environment variables from .env file
docker run -it --name cryptoapp --env-file app/.env "$IMAGE_NAME"

# Load plist file into launchd
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$LAUNCHD_DIR/launchd_job.plist"

if [ -f "$PLIST_FILE" ]; then
    # Set Service ID from plist file
    SERVICE_ID="com.cryptoapp.docker"

    # Constructing the service target
    SERVICE_TARGET="gui/$(id -u)/$SERVICE_ID"

    # Load the launchd job
    launchctl load ~/Library/LaunchAgents/launchd_job.plist

    # Enable the launchd job
    launchctl enable "$SERVICE_TARGET"
    echo "Launchd job enabled successfully."

    # Kickstart the launchd job
    launchctl kickstart "$SERVICE_TARGET"
    echo "Launchd job started successfully."
else
    echo "Error: Launchd plist file '$PLIST_FILE' not found."
    exit 1
fi
