#!/bin/bash

if [ -f "/fullchain.pem" ]; then
	python3 /node_backend/manage.py runsslserver --certificate /fullchain.pem --key /privkey.pem 0.0.0.0:8002
else
	python3 /node_backend/manage.py makemigrations
	python3 /node_backend/manage.py migrate

	certbot certonly --standalone -d $HOSTNAME.whoole.space
fi
