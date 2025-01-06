#!/bin/bash
if [ -z "$1" ]; then
    echo "Enter .env file. Example: $0 example.env"
    exit 1
else
    echo "Running docker services"
    echo "Passed env file: $1"
    docker-compose --env-file $1 up -d
    docker ps -a
fi
