#!/bin/bash
docker exec aqbackend python create_tables.py
docker exec aqbackend python populate_tables.py