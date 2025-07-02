#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
IMAGE_NAME="your_dockerhub_username/django-tettings-ci_cd"
COMMIT_HASH=$(git rev-parse --short HEAD)

# Build the Docker image
docker build -t $IMAGE_NAME:$COMMIT_HASH .

# Push the image to Docker Hub
docker push $IMAGE_NAME:$COMMIT_HASH

# Run the container locally
docker run -d -p 8000:8000 --env-file .env $IMAGE_NAME:$COMMIT_HASH

echo "Deployment complete. The site is running locally on http://localhost:8000"