CERTBOT_PASSWORD=$(openssl rand -base64 12)

echo 'export CERTBOT_PASSWORD="'$CERTBOT_PASSWORD'"' >> ~/.bashrc

openssl genrsa -des3 -passout pass:$CERTBOT_PASSWORD -out django.key 2048
openssl req -new -key django.key -out django.csr -subj "/emailAddress=maksarestov2000@gmail.com/C=RU/O=CloudBlesKCORP" -passin pass:$CERTBOT_PASSWORD
openssl x509 -req -days 365 -in django.csr -signkey django.key -out certificate.crt -passin pass:$CERTBOT_PASSWORD 

exec /bin/bash
