#!/bin/bash
echo "Stopping docker services"
docker-compose down
docker rm -f  $(docker ps -aq)
docker rmi $(docker images -q)
echo "Operation completed!"
