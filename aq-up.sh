#!/bin/bash
if [ -z "$1" ]; then
    echo "Enter .env file. Example: $0 example.env"
    exit 1
else
    echo "Running docker services"
    echo "Passed env file: $1"
    cd db_scripts
    python3 convert_jpg_to_binary.py --dict_name example_excercise_pictures --safe_mode yes
    cd ..
    docker-compose --env-file $1 up -d
    docker ps -a
fi
