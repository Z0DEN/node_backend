#!/usr/bin/expect -f

set password $env(CERTBOT_PASSWORD)

spawn python3 /node_backend/manage.py runsslserver --certificate /certificate.crt --key /django.key 0.0.0.0:8002
expect "Enter PEM pass phrase:"
send "$password\r"
interact
