#!/bin/bash
ip_address=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgresdb)
echo "Container's ip: $ip_address"