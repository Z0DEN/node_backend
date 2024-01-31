import datetime, secrets
import json, os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import User, Folder, File, server_data 
from .node_auth import node_connection
from .tokens import *


global status_list


def RJR(status=False, response_data={}, msg=False):
    response_data['status'] = status if status else "Success, or not success, that is the question"
    response_data['msg'] = status_list[status] + msg if status and msg else status_list[status] or msg if status or msg else "???UNDEFINED ERROR???"
    return JsonResponse(response_data)


@csrf_exempt
def AddUser(request):
    print('start adding user')
    username = json.loads(request.body)['username']

    if not username:
        return RJR(13)
    if User.objects.filter(username=username).exists():
        return RJR(17)

    new_user = User(
            username = username,
    )
    new_user.save()
    print(new_user)
    user_dir = os.path.join("/storage", username)
    print(user_dir)
    os.makedirs(user_dir)
    
    return RJR(21)

@csrf_exempt
def GetUserData(request):
    data = json.loads(request.body)
    username = data.get('username', None)
    user = User.objects.get(username=username)
    for folder in user.folders:
        print(folder)

def CreateFolder(request):
    data = json.loads(request.body)
    folder_name = data.get('folder_name', None)
    



@csrf_exempt
def test(request):
    print('start test')
    return RJR(22)




    
#    Folder.objects.create(
#        username=new_user,
#        FolderName="None",
#        FolderParent="None",
#    )


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
