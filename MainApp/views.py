import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import main_user_model, user_data_model, server_data 
from .node_auth import node_connection

global status_list

def RJR(status=False, msg=False):
    response_data = {
        "status": status if status else "Success, or not success, that is the question",
        "msg": status_list[status] + msg if status and msg else status_list[status] or msg if status or msg else "???UNDEFINED ERROR???",
    }
    return JsonResponse(response_data)


@csrf_exempt
def AddUser(request):
    if request.method != 'POST':
        return RJR(12) 

    username = request.POST['username']
    bearer_header = request.headers.get('Authorization')

    if not username:
        return RJR(13)

    if not bearer_header or not bearer_header.startswith('Bearer '):
        return RJR(16, "You need to produce token in authorization headers")

    token = bearer_header.split(' ')[1]
    

    new_user = main_user_model(
            username = username,
    )
    new_user.save()
    
    new_user_data = user_data_model(
        username=new_user,
        FolderName="None",
        FolderParent="None",
    )
    new_user_data.save()


    return JsonResponse(response_data, safe=False)

@csrf_exempt
def test(request):
    if request.method != 'POST':
        return RJR(12)


    bearer_header = request.headers.get('Authorization')
    print(bearer_header)

    if not bearer_header or not bearer_header.startswith('Bearer '):
        return RJR(16, "You need to produce token in authorization headers")

    token = bearer_header.split(' ')[1]
    return RJR(20, f"You are genius as fuck: {token}")
    


    

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
