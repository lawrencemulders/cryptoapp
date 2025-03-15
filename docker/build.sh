#!/bin/bash

# Define variables
IMAGE_NAME="cryptoapp-image"
CONTAINER_NAME="cryptoapp"
DOCKERFILE_PATH="docker/Dockerfile"
ENV_FILE="backend/.env"

# Navigate to the root directory
cd "$(dirname "$0")"/..

# Check if the Dockerfile exists
if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo "Error: Dockerfile not found at $DOCKERFILE_PATH"
    exit 1
fi

# Build Docker image if it does not already exist
if ! docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "Building Docker image '$IMAGE_NAME'..."
    docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" .
else
    echo "Docker image '$IMAGE_NAME' already exists. Skipping build."
fi

# Check if a container with the same name is running
if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -w "$CONTAINER_NAME" > /dev/null 2>&1; then
    echo "Stopping existing container '$CONTAINER_NAME'..."
    docker stop "$CONTAINER_NAME"
    echo "Removing existing container '$CONTAINER_NAME'..."
    docker rm "$CONTAINER_NAME"
fi

# Verify the environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Run Docker container
echo "Running Docker container '$CONTAINER_NAME'..."
docker run -it --name "$CONTAINER_NAME" --env-file "$ENV_FILE" "$IMAGE_NAME"
