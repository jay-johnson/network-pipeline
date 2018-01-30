#!/bin/bash

source /tmp/netpipevenv/bin/activate

echo ""
echo "Starting Pet Clinic application listening on TCP port 8080"
echo "http://localhost:8080/petclinic"
echo ""

cd terracotta-oss-docker/client
docker-compose up -d

echo "Sleeping to let to containers boot up"
sleep 10

docker logs petclinic

echo ""
echo "View the Pet Clinic at:"
echo "http://localhost:8080/petclinic"
