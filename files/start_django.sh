#!/bin/bash

if [ -f "/etc/letsencrypt/live/$HOSTNAME.whoole.space/fullchain.pem" ]; then
	python3 /node_backend/manage.py runsslserver --certificate /etc/letsencrypt/live/$HOSTNAME.whoole.space/fullchain.pem --key /etc/letsencrypt/live/$HOSTNAME.whoole.space/privkey.pem 0.0.0.0:8002
else
	python3 /node_backend/manage.py makemigrations
	python3 /node_backend/manage.py migrate

	/usr/bin/python3 /usr/local/bin/certbot certonly --standalone -n -m maksarestov2000@gmail.com -a --agree-tos -d $HOSTNAME.whoole.space
fi
