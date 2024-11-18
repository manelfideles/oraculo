#!/bin/bash

# Use this file if you want to self-host the bot.
# This file is meant to be copied into the /usr/local/bin/ folder e.g.:
# `cp run.sh /usr/local/bin/run.sh`
#

# Configuration: **Absolute** path to Dockerfile/docker-compose.yml dir in the root of the project
DOCKER="<absolute_path_to_dockercompose_file>"

# Navigate to the Docker project directory
cd "$DOCKER" || {
    echo "ERROR: Could not change to directory $DOCKER"
    exit 1
}

# Start the containers
echo "Starting Docker container..."
docker compose up -d 

# Check if docker-compose up was successful
if [ $? -eq 0 ]; then
    echo "Oraculo container started successfully"
else
    echo "ERROR: Failed to start Oraculo container"
    exit 1
fi
