#!/bin/bash

# this assumes docker is running and docker-compose is installed

compose_file="redis.yml"

echo "Starting redis with compose_file=${compose_file}"
docker-compose -f $compose_file up -d

exit 0
