#!/bin/bash

# this assumes docker is running and docker-compose is installed

echo "Stopping nredis1 nrabbit1"
docker-compose -f redis.yml stop
docker-compose -f rabbitmq.yml stop

if [[ "$?" == "0" ]]; then
    docker rm nredis1 nrabbit1 >> /dev/null 2>&1
fi

exit 0
