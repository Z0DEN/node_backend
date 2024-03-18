import os, requests, json, jwt, secrets, datetime, redis
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.cache import cache
from MainApp.models import server_data
from .tokens import *

RPASSWORD = os.environ.get('RPASSWORD')
REDISKA = redis.Redis(host='localhost', port=6379, password=RPASSWORD, db=0)

personal_key = "personal_key"

global status_list

def RJR(response_data={}, status=False, msg=False):
    response_data['status'] = status if status else "Success, or not success, that is the question"
    response_data['msg'] = status_list[status] + msg if status and msg else status_list[status] or msg if status or msg else "???UNDEFINED ERROR???"
    return JsonResponse(response_data)


def generate_token(payload, secret_key):
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_token(token, secret_key):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded, 22
    except jwt.ExpiredSignatureError:
        return None, 14
    except jwt.InvalidTokenError:
        return None, 15


def get_data():
    node_domain = os.environ.get('HOSTNAME')
    IN_IP = os.environ.get('IN_IP')
    EX_IP = os.environ.get('EX_IP')
    UUID = os.environ.get('UUID')
    PORT = os.environ.get('PORT')
    SPACE = os.environ.get('SPACE')

    secret_key = secrets.token_hex(32)
    issued_at = datetime.utcnow()
    access_expiration = issued_at + timedelta(minutes=30)
    refresh_expiration = issued_at + timedelta(days=5)
#   access_expiration = issued_at + timedelta(minutes=1)
#   refresh_expiration = issued_at + timedelta(minutes=3)
    
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
        'port': PORT,
        'node_available_space': SPACE,
        'node_access_token': local_access_token,
        'node_refresh_token': local_refresh_token,
    }
    return local_access_token, local_refresh_token, secret_key, data


def send_data(data_to_send, func, token_type='main_server_access_token'):
    obj = server_data.objects.first()
    request_url = f'https://whoole.space/{func}/'
    headers = {'Content-Type': 'application/json'}

    if obj is not None and token_type != 'None': 
        token = getattr(obj, token_type)
        headers['Authorization'] = f'Bearer ' + token 
    else:
        headers['Authorization'] = 'personal ' + personal_key

    try:
        response = requests.post(request_url, data=json.dumps(data_to_send), headers=headers)
    except Exception as e:
        print(f"Error occurs while connection: {e}")

    data = response.json()
    status = data["status"]

    if status == 22 or status == 23 or status == 21:
        return data
    elif status == 14 and token_type != 'main_server_refresh_token': 
        return send_data(data_to_send, func, 'main_server_refresh_token')
    else:
        return send_data(data_to_send, func, 'None')


def node_connection():
    local_access_token, local_refresh_token, secret_key, data_to_send = get_data()
    
    response_data = send_data(data_to_send, 'NodeConnection') 
    
    msg = response_data["msg"]
    status = response_data["status"]
    main_access_token = response_data["access_token"]
    main_refresh_token = response_data["refresh_token"]
    
    if status >= 20 and status < 30:
        print(f"Success: {status} \nmsg: {msg} \nmain_access_token: {main_access_token} \nmain_refresh_token: {main_refresh_token}\n")
    elif status < 20:
        print(f"Failed to make connection: {status} \nmsg: {msg} \nmain_access_token: {main_access_token} \nmain_refresh_token: {main_refresh_token}\n")
        return

    SaveTokens(main_access_token, main_refresh_token, secret_key, status)


@csrf_exempt
def UpdateNodeTokens(request):
    data = json.loads(request.body)
    main_server_access_token = data["access_token"]
    main_server_refresh_token = data["refresh_token"]

    if (
        main_server_access_token is None
        or main_server_refresh_token is None
    ):
        return RJR(13)
    
    local_access_token, local_refresh_token, secret_key, _ = get_data()
    response_data ={
        'access_token':  local_access_token,
        'refresh_token':  local_refresh_token,
    }
    SaveTokens(main_server_access_token, main_server_refresh_token, secret_key, 23)
    return RJR(response_data=response_data,status=23)

     
def SaveTokens(main_access_token, main_refresh_token, secret_key, status):
    if status == 21:
        new_data = server_data(
            main_server_access_token = main_access_token,
            main_server_refresh_token = main_refresh_token,
            secret_key = secret_key
        )
        new_data.save()
        REDISKA.setex('server_secret_key', 6000, secret_key)

    if status == 23:
        obj, created = server_data.objects.get_or_create(id=1)
        data_to_update = {
            'main_server_access_token': main_access_token,
            'main_server_refresh_token': main_refresh_token,
            'secret_key': secret_key,
        }
        server_data.objects.filter(id=obj.id).update(**data_to_update)
        REDISKA.setex('server_secret_key', 6000, secret_key)


node_connection()


status_list = {
    10: "Undefined error. ",
    11: "Node already exists. ",
    12: "Invalid request method. ",
    13: "Invalid request data. ",
    14: "Token is expired. ",
    15: "Invalid Token. ",
    16: "Request have no auth token (Bearer). ",
    17: "User already exist. ", 
    # ------------------------------------------------------------- #
    20: "Undefined success. ",
    21: "Node or user was successfully created. ",
    22: "Token is Valid. ",
    23: "Data successfully changed. ",
    # ------------------------------------------------------------- #
    30: "Undefined warning. ",
    # ------------------------------------------------------------- #
    40: "Undefined info. ",
}
