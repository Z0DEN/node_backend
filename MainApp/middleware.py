import jwt
import os
import redis
import json
from django.middleware.common import MiddlewareMixin 
from django.shortcuts import resolve_url
from django.http import JsonResponse
from MainApp.models import server_data, User
from MainApp.node_auth import send_data, node_connection

# ++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++===

global STATUS_LIST, REDISKA

RPASSWORD = os.environ.get('RPASSWORD')
REDISKA = redis.Redis(host='localhost', port=6379, password=RPASSWORD, db=0)

# ++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++===

    
def RJR(status=False, response_data={}, msg=False):
    response_data['status'] = status if status else None
    response_data['msg'] = STATUS_LIST[status] + msg if status and msg else STATUS_LIST[status] or msg if status or msg else "Success, or not success, that is the question"
    return JsonResponse(response_data)


def decode_token(token, secret_key):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded, 22
    except jwt.ExpiredSignatureError:
        return None, 14
    except jwt.InvalidTokenError:
        return None, 15


# ++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++===

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method != "POST":
            return RJR(12)

        bearer_header = request.headers.get('Authorization')
    
        if not bearer_header:
            return RJR(16)
    
        from_header = bearer_header.split(' ')[0]
        header_type = bearer_header.split(' ')[1]
        token = bearer_header.split(' ')[2]
    
        if from_header == 'server':
            if header_type == 'personal':
                local_personal_key = server_data.objects.get(personal_key='personal_key').personal_key
                return RJR(15) if local_personal_key != token else None
            else:
                secret_key = REDISKA.get('server_secret_key')
                secret_key = sever_data.objects.get('secret_key') if secret_key == 'nil' else secret_key
                _, status = decode_token(token, secret_key)
                return RJR(status) if status != 22 else None
    
        elif from_header == 'user':
            node_UUID = os.environ.get('UUID')
            username = request.headers.get('username')
            if node_UUID is None or username is None:
                return RJR(status=13)
            data_to_send = {
                'username': username,
                'Bearer': token,
                'node_UUID': node_UUID,
            }
            response_data = send_data(data_to_send, 'TokenVerify')
            node_validate_status = response_data.get('node_validate_status', None)
            user_validate_status = response_data.get('user_validate_status', None)
            if node_validate_status != 22 or node_validate_status is None:
                node_connection()
                return RJR(31)
            if user_validate_status != 22 or user_validate_status is None:
                return RJR(user_validate_status)
    
            if User.objects.filter(username=username).exists() == False:
                User.objects.create_user(username)

# make adding user token to redis?????
# make adding user token to redis?????
# make adding user token to redis?????
# make adding user token to redis?????




# ------------------------------------------------------------- #
#                            STATUSES                           #
# ------------------------------------------------------------- #
#   1<..>  -> Error
#   2<..>  -> Success
#   3<..>  -> Warning
#   4<..>  -> Info

STATUS_LIST = {
    10: "Undefined error. ",
    11: "Node already exists. ",
    12: "Invalid request method. ",
    13: "Invalid request data. ",
    14: "Token is expired. ",
    15: "Invalid Token. ",
    16: "Request have no auth token (Bearer). ",
    # ------------------------------------------------------------- #
    20: "Undefined success. ",
    21: "Node or user was successfully created. ",
    22: "Token is Valid. ",
    23: "Data successfully changed. ",
    # ------------------------------------------------------------- #
    30: "Undefined warning. ",
    31: "Something went wrong, try again. ", 
    # ------------------------------------------------------------- #
    40: "Undefined info. ",
}
