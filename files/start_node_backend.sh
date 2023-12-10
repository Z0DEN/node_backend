#!/bin/bash


HOSTNAME=$(hostname)
PASSWORD=$(openssl rand -base64 12)
EXTERNAL_IP=$(curl -s https://api.ipify.org)
INTERNAL_IP=$(hostname -I | awk '{print $1}')
UUID=$(dbus-uuidgen | tr '[:upper:]' '[:lower:]')


sudo -u postgres psql -c "CREATE DATABASE $HOSTNAME;"
sudo -u postgres psql -c "CREATE USER django_user WITH PASSWORD '$PASSWORD';"
sudo -u postgres psql -c "ALTER ROLE django_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE django_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $HOSTNAME TO django_user;"


echo 'export EX_IP="'$EXTERNAL_IP'"' >> ~/.bashrc
echo 'export IN_IP="'$INTERNAL_IP'"' >> ~/.bashrc
echo 'export DBPASSWORD="'$PASSWORD'"' >> ~/.bashrc
echo 'export DBPASSWORD="'$HOSTNAME'"' >> ~/.bashrc
echo 'export UUID="'$UUID'"' >> ~/.bashrc


docker run --name nodeback -d --network=host -v /var/run/postgresql/:/var/run/postgresql/ -e DBNAME=$HOSTNAME -e EX_IP=$EXTERNAL_IP -e IN_IP=$INTERNAL_IP -e DBPASSWORD=$PASSWORD z0den/node-dev:latest


exec $SHELL
