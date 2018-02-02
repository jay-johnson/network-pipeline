#!/bin/bash

source /tmp/netpipevenv/bin/activate

echo "Starting Django listening on TCP port 8080"
echo "http://localhost:8080/admin"
echo ""

export DJANGO_SECRET_KEY=supersecret

cd django-project-template
python ./manage.py runserver 0.0.0.0:8080
