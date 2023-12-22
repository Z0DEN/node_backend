import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import main_user_model, user_data_model, server_data 
from .node_auth import node_connection

global status_list

def gen_secret_key():
    return secrets.token_hex(32)

def RJR(status=False, msg=False):
    response_data = {
        "status": status if status else "Success, or not success, that is the question",
        "msg": status_list[status] + msg if status and msg else status_list[status] or msg if status or msg else "???UNDEFINED ERROR???",
    }
    return JsonResponse(response_data)


@csrf_exempt
def AddUser(request):
    username = request.POST['username']

    if not username:
        return RJR(13)
    if main_user_model.objects.filter(username=username).exists():
        return RJR(17)

    secret_key = gen_secret_key()

    refresh_payload = {
        "sub": username,
        "exp": refresh_expiration,
        "iat": issued_at,
        "scopes": scopes,
    }

    access_payload = {
        "sub": username,
        "exp": access_expiration,
        "iat": issued_at,
        "scopes": scopes,
    }

    user_a_token = generate_token(access_payload, secret_key)
    user_ref_token = generate_token(refresh_payload, secret_key) 

    new_user = main_user_model(
            username = username,
            user_access_token = user_a_token, 
            user_refresh_token = user_ref_token, 
            secret_key = secret_key, 
    )
    new_user.save()
    
    user_data_model.objects.create(
        username=new_user,
        FolderName="None",
        FolderParent="None",
    )

    return RJR(21)


@csrf_exempt
def test(request):
    return RJR(22)



@csrf_exempt
def fail(request):
   return RJR(15) 


    

# --------------------------------------------------- #
#                     SERVER AUTH
# --------------------------------------------------- #

node_connection()

# --------------------------------------------------- #


# ------------------------------------------------------------- #
#                            STATUSES                           #
# ------------------------------------------------------------- #
#   1<..>  -> Error
#   2<..>  -> Success
#   3<..>  -> Warning
#   4<..>  -> Info

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
