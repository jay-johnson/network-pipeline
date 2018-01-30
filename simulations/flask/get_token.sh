#!/bin/bash

# https://github.com/frol/flask-restplus-server-example#authentication-with-login-and-password-resource-owner-password-credentials-grant
user="root"
password="q"

if [[ "${FLASK_USER}" ]]; then
    user="${FLASK_USER}"
fi
if [[ "${FLASK_PASSWORD}" ]]; then
    password="${FLASK_PASSWORD}"
fi

echo ""
echo "Getting OAuth token for user=${user}"
curl -vvvv "http://127.0.0.1:8080/auth/oauth2/token?grant_type=password&client_id=documentation&username=${user}&password=${password}"
last_status=$?
if [[ "${last_status}" != "0" ]]; then
    echo "Failed to get a token with user=${user}"
    exit 1
fi
