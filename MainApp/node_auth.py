from MainApp.models import server_data
import os, requests, json, jwt, secrets, datetime
from datetime import datetime, timedelta


def generate_token(payload, secret_key):
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_token(token, secret_key):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded, 22
    except jwt.ExpiredSignatureError:
        return 14
    except jwt.InvalidTokenError:
        return 15


def node_connection():
    url1 = 'http://192.168.0.98:8005/NodeConnection/'
    url2 = 'http://176.197.34.213:8005/NodeConnection/'
    headers = {'Content-Type': 'application/json'}

    node_domain = os.environ.get('HOSTNAME')
    IN_IP = os.environ.get('IN_IP')
    EX_IP = os.environ.get('EX_IP')
    UUID = os.environ.get('UUID')
    secret_key = secrets.token_hex(32)
    issued_at = datetime.utcnow()
    access_expiration = issued_at + timedelta(minutes=100)
    refresh_expiration = issued_at + timedelta(hours=1)

    refresh_payload = {
        "sub": node_domain,
        "exp": refresh_expiration,
        "iat": issued_at,
    }

    access_payload = {
        "sub": node_domain,
        "exp": access_expiration,
        "iat": issued_at,
    }

    local_access_token = generate_token(access_payload, secret_key)
    local_refresh_token = generate_token(refresh_payload, secret_key)

    data = {
        'node_domain': node_domain,
        'IN_IP': IN_IP,
        'EX_IP': EX_IP,
        'UUID' : UUID,
        'local_connection': True,
        'node_access_token': local_access_token,
        'node_refresh_token': local_refresh_token,
    }

    response = None

    try:
        response = requests.post(url1, data=json.dumps(data), headers=headers)
    except requests.exceptions.RequestException:
         data["local_connection"] = False
         response = requests.post(url2, data=json.dumps(data), headers=headers)

    if response == None:
        sys.exit()
        print("No response was received")

    data = response.json()

    msg = data["msg"]
    status = data["status"]
    main_access_token = data["access_token"]
    main_refresh_token = data["refresh_token"]

    if status >= 20 and status < 30:
        print(f"Success: {status} \nmsg: {msg} \nmain_access_token: {main_access_token} \nmain_refresh_token: {main_refresh_token}")
    elif status < 20:
        print(f"Failed to make connection: {status} \nmsg: {msg} \nmain_access_token: {main_access_token} \nmain_refresh_token: {main_refresh_token}")

    if status == 21:
        server_data.objects.all().delete()
        new_data = server_data(
            main_server_access_token = main_access_token,
            main_server_refresh_token = main_refresh_token,
            local_server_access_token =  local_access_token,
            local_server_refresh_token = local_refresh_token,
            secret_key = secret_key
        )
        new_data.save()
