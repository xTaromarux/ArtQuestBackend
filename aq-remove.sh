#!/bin/bash
echo "Removing docker services"
docker-compose down
docker image rm monoaq-postgres:latest
docker image rm monoaq
deactivate