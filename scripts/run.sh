#!/bin/bash

# Configuration
DOCKER_DIR="/home/fideles/Desktop/projects/oraculo"

# Navigate to the Docker project directory
cd "$DOCKER_DIR" || {
    echo "ERROR: Could not change to directory $DOCKER_DIR"
    exit 1
}

# Start the containers
echo "Starting Docker containers..."
docker compose up -d 

# Check if docker-compose up was successful
if [ $? -eq 0 ]; then
    echo "Docker containers started successfully"
else
    echo "ERROR: Failed to start Docker containers"
    exit 1
fi
