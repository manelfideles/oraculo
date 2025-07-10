#!/bin/bash

# Use this file if you want to self-host the bot.
# Check the README file for more info.

# Configuration: **Absolute** path to Dockerfile/docker-compose.yml dir in the root of the project
DOCKER="<absolute_path_to_dockercompose_file>"

cd "$DOCKER" || {
    echo "ERROR: Could not change to directory $DOCKER"
    exit 1
}

echo "Starting Docker container..."
docker compose up -d 

if [ $? -eq 0 ]; then
    echo "Oraculo container started successfully"
else
    echo "ERROR: Failed to start Oraculo container"
    exit 1
fi
