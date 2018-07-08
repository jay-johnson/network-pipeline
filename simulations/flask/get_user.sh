#!/bin/bash

# https://github.com/frol/flask-restplus-server-example#authentication-with-login-and-password-resource-owner-password-credentials-grant
user="root"
password="q"
endpoint="http://127.0.0.1:8010"

if [[ "${FLASK_USER}" ]]; then
    user="${FLASK_USER}"
fi
if [[ "${FLASK_PASSWORD}" ]]; then
    password="${FLASK_PASSWORD}"
fi
if [[ "${FLASK_ENDPOINT}" ]]; then
    password="${FLASK_ENDPOINT}"
fi

echo ""
echo "Getting OAuth token for user=${user}"
res=$(curl -vvvv "${endpoint}/auth/oauth2/token?grant_type=password&client_id=documentation&username=${user}&password=${password}")
last_status=$?
if [[ "${last_status}" != "0" ]]; then
    echo "Failed to get a token with user=${user}"
    exit 1
fi

token=$(echo "${res}" | sed -e 's/"/ /g' | awk '{print $4}')

echo "User token=${token}"

echo ""
echo "Getting user=${user} details"
curl --header "Authorization: Bearer ${token}" "${endpoint}/api/v1/users/me"
if [[ "${last_status}" != "0" ]]; then
    echo "Failed to get user=${user} details"
    exit 1
fi

echo ""
exit 0
