#!/bin/bash

set -e  # Stop script on error

sudo docker compose down --remove-orphans 
sudo docker buildx prune -f
sudo docker compose up --build --remove-orphans -d
sudo docker compose logs -f
