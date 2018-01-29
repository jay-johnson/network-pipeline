#!/bin/bash

source /tmp/netpipevenv/bin/activate

docker stop zap >> /dev/null 2>&1
docker rm zap >> /dev/null 2>&1
docker-compose -f zap-compose.yml up -d

echo "sleeping to let zap boot up"
date
sleep 10
date

echo "checking the logs"
docker logs zap
docker ps -a | grep zap

echo "zap should be ready"
docker exec -it zap zap-cli quick-scan -s xss,sqli --spider -r -e '*' http://localhost:8080/
