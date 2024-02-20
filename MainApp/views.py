import datetime, secrets
import json, os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import User, Folder, File, server_data 
from .node_auth import node_connection
from .tokens import *


global status_list


def RJR(status=False, response_data={}, msg=False, data=[]):
    response_data['status'] = status if status else "Success, or not success, that is the question"
    response_data['msg'] = status_list[status] + msg if status and msg else status_list[status] or msg if status or msg else "???UNDEFINED ERROR???"
    if data:
        response_data['data'] = data
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
#    print(new_user)
#    user_dir = os.path.join("/storage", username)
#    print(user_dir)
#    os.makedirs(user_dir)
    
    return RJR(21)

@csrf_exempt
def GetUserData(request):
    data = json.loads(request.body)
    username = data.get('username', None)
    user = User.objects.get(username=username)
    user_files = []
    for folder in user.folders.all():
        folder_data = {
            'type': 'folder',
            'name': folder.name,
            'parent': folder.parent,
            'date_added': folder.date_added,
        }
        user_files.append(folder_data)
        for file in folder.files.all():
            file_data = {
                'type': 'file',
                'name': file.name,
                'parent': file.parent,
                'date_added': file.date_added,
            }
            user_files.append(file_data) 
    return RJR(status=20, data=user_files)


@csrf_exempt
def CreateFolder(request):
    data = json.loads(request.body)
    folder_name = data.get('folder_name', None)
    folder_parent = data.get('folder_parent', None)
    username = data.get('username')
    
    user = User.objects.get(username=username)

    folder, created = user.folders.create_folder(name=folder_name, parent=folder_parent, user=user)
    if not created:
        return RJR(status=18)
    else:
        return RJR(status=24)


@csrf_exempt
def UploadFiles(request):
    parent = request.POST.get('parent')
    username = request.POST.get('username')
    files = request.FILES.getlist('user_files')
    user = User.objects.get(username=username)
    folder = user.folders.get(name=parent)
    if folder is None:
        return RJR(status=13, msg=f"folder {parent} does not exist")

    existed_files = []
    for file in files:
        _, created = File.objects.create_file(file=file, name=file.name, folder=folder)
        if not created:
            existed_file.append(file.name)
    if existed_files:
        return RJR(status=13, msg=f"this file(s) already exist(s): {', '.join(existed_files)}")

    return RJR(status=25)


@csrf_exempt
def DownloadFiles(request):
    data = json.loads(request.body)
    username = data.get('username')
    file_names = data.get('file_names', False)
    if not file_names:
        return RJR(status=13, msg='file_names should be non-empty array')
    user = User.objects.get(username=username)
    paths = []
    FileDoesNotExist = []
    for name in file_names:
        try:
            paths.append(user.files.get(name=name).file.path)
        except ObjectDoesNotExist:
            FileDoesNotExist.append(name)

    return RJR(status=20, msg=f"{paths}")



    
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
    18: 'Folder or file already exist. ',
    # ------------------------------------------------------------- #
    20: "Undefined success. ",
    21: "Node or user was successfully created. ",
    22: "Token is Valid. ",
    23: "Data successfully changed. ",
    24: "Folder or file was successfully created. ",
    25: "Files was successfully saved. ",
    # ------------------------------------------------------------- #
    30: "Undefined warning. ",
    # ------------------------------------------------------------- #
    40: "Undefined info. ",
}
