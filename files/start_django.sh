#!/bin/bash

if [ -f "/certificate.crt" ]; then
	password=$CERTBOT_PASSWORD
	echo $password
	expect -c '
	spawn python3 /node_backend/manage.py runsslserver --certificate /certificate.crt --key /django.key 0.0.0.0:8002
	expect "Enter PEM pass phrase:"
	send "'"$password"'\r"
	interact
	'
else
	python3 /node_backend/manage.py makemigrations
	python3 /node_backend/manage.py migrate

	CERTBOT_PASSWORD=$(openssl rand -base64 12)

	echo 'export CERTBOT_PASSWORD="'$CERTBOT_PASSWORD'"' >> ~/.bashrc

	openssl genrsa -des3 -passout pass:$CERTBOT_PASSWORD -out django.key 2048
	openssl req -new -key django.key -out django.csr -subj "/emailAddress=maksarestov2000@gmail.com/C=RU/O=CloudBlesKCORP" -passin pass:$CERTBOT_PASSWORD
	openssl x509 -req -days 365 -in django.csr -signkey django.key -out certificate.crt -passin pass:$CERTBOT_PASSWORD

	expect -c '
	spawn python3 /node_backend/manage.py runsslserver --certificate /certificate.crt --key /django.key 0.0.0.0:8002
	expect "Enter PEM pass phrase:"
	send "'"$CERTBOT_PASSWORD"'\r"
	interact
	'
	exec /bin/bash
fi
