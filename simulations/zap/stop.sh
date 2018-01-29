#!/bin/bash

docker-compose -f zap-compose.yml stop >> /dev/null 2>&1

docker stop zap >> /dev/null 2>&1
docker rm zap >> /dev/null 2>&1
