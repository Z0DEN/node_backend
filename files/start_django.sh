#!/bin/bash

if [ -f "/etc/letsencrypt/live/$HOSTNAME.whooole.space/fullchain.pem" ]; then
	python3 /node_backend/manage.py runsslserver --certificate /etc/letsencrypt/live/$HOSTNAME.whooole.space/fullchain.pem --key /etc/letsencrypt/live/$HOSTNAME.whooole.space/privkey.pem 0.0.0.0:8002
else
	python3 /node_backend/manage.py makemigrations
	python3 /node_backend/manage.py migrate

	/usr/bin/python3 /bin/certbot certonly --standalone -n -m maksarestov2000@gmail.com --agree-tos -d $HOSTNAME.whooole.space

	python3 /node_backend/manage.py runsslserver --certificate /etc/letsencrypt/live/$HOSTNAME.whooole.space/fullchain.pem --key /etc/letsencrypt/live/$HOSTNAME.whooole.space/privkey.pem 0.0.0.0:8002

fi
