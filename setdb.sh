#!/bin/sh

HOSTNAME=$(hostname)
PASSWORD=$(openssl rand -base64 12)

sudo -u postgres psql -c "CREATE DATABASE $HOSTNAME;"
sudo -u postgres psql -c "CREATE USER django_user WITH PASSWORD '$PASSWORD';"
sudo -u postgres psql -c "ALTER ROLE django_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE django_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $HOSTNAME TO django_user;"

echo 'export DBPASSWORD="'$PASSWORD'"' >> ~/.bashrc
exec $SHELL
