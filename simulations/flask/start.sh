#!/bin/bash

source /tmp/netpipevenv/bin/activate

echo ""
echo "Starting Flask RESTplus Example (with swagger) listening on TCP port 8080"
echo "http://localhost:8080/api/v1/"
echo ""

cd flask-rest
export FLASK_CONFIG=development
invoke app.run --port=8080
