#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Function to wait for PostgreSQL to be ready
wait_for_postgres() {
  while ! nc -z localhost 5432; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
  done
}

# Check if .env file is provided
if [ -z "$1" ]; then
    echo "Enter .env file. Example: $0 example.env"
    exit 1
else
    echo "Running docker services"
    echo "Passed env file: $1"

    # Create and activate virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m virtualenv --no-download -p python3.8 venv
    fi

    source venv/bin/activate

    # Install required packages
    pip3 install -r app/requirements.txt

    # Run Docker Compose
    docker-compose --env-file $1 up -d

    # Wait for PostgreSQL to be ready
    wait_for_postgres

    # Execute Python scripts
    cd db_scripts
    find . -type d -name "__pycache__" -exec rm -r {} +
    python3 convert_jpg_to_binary.py --dict_name example_excercise_pictures --safe_mode yes
    cd ..

    # Deactivate virtual environment
    echo -e "\n ${GREEN}Operation completed! ${NC}\n"

    # chmod +x db_scripts/inject_db_seed.sh

    # sh db_scripts/inject_db_seed.sh

    # Show running Docker containers
    docker ps -a
fi
