#!/bin/bash

git clone https://github.com/anthonydahanne/terracotta-oss-docker.git 

cp docker-compose.yml terracotta-oss-docker/client/

echo ""
echo "Run ./start.sh to start Spring Pet Clinic docker demo"
