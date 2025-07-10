#!/bin/bash

# Use this file if you want to run the scraper locally, self-host it, or both.
# Check the README file for more info.

echo "Generating requirements.txt from pyproject.toml..."
poetry export -f requirements.txt --output requirements.txt --without-hashes
echo "Done."

echo "Building Oraculo image..."
docker build --no-cache -t oraculo . --platform=linux/amd64
echo "Done"

echo "Starting Oraculo container..."
docker run -d oraculo --name oraculo