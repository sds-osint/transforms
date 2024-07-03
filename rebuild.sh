#!/bin/bash

set -e

# Step 1: Stop and remove containers, networks, images, and volumes
sudo docker compose down --remove-orphans

# Step 2: Remove unused data
sudo docker system prune -f --volumes

# Step 3: Remove unused images
sudo docker image prune -f

# Step 4: Remove dangling volumes
sudo docker volume prune -f

# Step 5: Build and start containers
sudo docker compose up --build --remove-orphans -d

# Step 6: Display logs
sudo docker compose logs -f
