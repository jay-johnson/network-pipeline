#!/bin/bash

source /tmp/netpipevenv/bin/activate

git clone https://github.com/frol/flask-restplus-server-example.git flask-rest
cd flask-rest
pip install -r requirements.txt
pip install -r tasks/requirements.txt

cp ../config.py ./config.py

echo ""
echo "Run ./start.sh to run Flask"
