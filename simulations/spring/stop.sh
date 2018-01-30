#!/bin/bash

source /tmp/netpipevenv/bin/activate

docker-compose -f docker-compose.yml stop >> /dev/null 2>&1
docker stop client_tsa_1 client_petclinic_1 >> /dev/null 2>&1
docker rm client_tsa_1 client_petclinic_1 >> /dev/null 2>&1
