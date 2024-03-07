import datetime, secrets
import json, os
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import User, Folder, File, server_data 
from .node_auth import node_connection
from .tokens import *


global STATUS_LIST


def RJR(status=False, msg=False, response_data={}, headers={}):
    response_data['status'] = status if status else None
    response_data['msg'] = STATUS_LIST[status] + msg if status and msg else STATUS_LIST[status] or msg if status or msg else "Success, or not success, that is the question"
    
    return JsonResponse(response_data, headers=headers)


@csrf_exempt
def AddUser(request):
    username = json.loads(request.body)['username']

    if not username:
        return RJR(13)
    if User.objects.filter(username=username).exists():
        return RJR(17)

    new_user = User.create_user(username=username)

    return RJR(21)

@csrf_exempt
def GetUserData(request):
    data = json.loads(request.body)
    username = data.get('username', None)
    user = User.objects.get(username=username)

    user_folders = user.get_folders()
    user_files = user.get_files()

    user_data = []
    user_data.extend(user_files + user_folders)

    return RJR(status=20, response_data={'data': user_data})


@csrf_exempt
def CreateFolder(request):
    data = json.loads(request.body)
    folder_name = data.get('folder_name', None)
    item_id = data.get('item_id', None)
    parent_id = data.get('parent_id', True)
    username = data.get('username')
    if folder_name is None or parent_id is True or item_id is None:
        return RJR(13)

    user = User.objects.get(username=username)

    _, created = user.folders.create_folder(name=folder_name, parent_id=parent_id, item_id=item_id)

    if not created:
        return RJR(18, msg=folder_name)
    else:
        return RJR(24)


@csrf_exempt
def UploadFiles(request):
    parent_id = request.POST.get('parent_id')
    username = request.POST.get('username')
    files = request.FILES.getlist('user_files')
    user = User.objects.get(username=username)
    if files is None:
        return RJR(13)

    existed_files = []
    for file in files:
        item_id = request.POST.get(file.name)
        _, created = user.files.create_file(file=file, item_id=item_id, parent_id=parent_id)
        if not created:
            existed_files.append(item_id)

    if existed_files:
        return RJR(status=18, msg=', '.join(existed_files), response_data={'existed_files': existed_files})

    return RJR(25)


@csrf_exempt
def DownloadFiles(request):
    data = json.loads(request.body)
    username = data.get('username')
    item_id = data.get('item_id', False)
    if not item_id:
        return RJR(status=13, msg='item_id should be non-empty string')

    user = User.objects.get(username=username)
    try:
        file = user.files.get(item_id=item_id)
    except ObjectDoesNotExist:
        return RJR(status=13, msg="file does not exist")
    
    file_response = FileResponse(file.file, as_attachment=True, filename=file.name, headers={'isFiles':True})
    return file_response 


@csrf_exempt
def DeleteFolder(request):
    data = json.loads(request.body)
    username = data.get('username')
    item_id = data.get('item_id', False)
    if not item_id:
        return RJR(status=13, msg='item_id should be non-empty string')

    user = User.objects.get(username=username)
    try:
        folder = user.folders.get(item_id=item_id)
    except ObjectDoesNotExist:
        return RJR(status=13, msg="folder does not exist")
    
    try:
        folder.delete_folder()
    except FolderDeletionError as e:
        return RJR(status=10, msg=f"Error occurs while deletion folder: {e}")
    else:
        return RJR(status=20, msg="Folder was deleted successfully")



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
    17: "User already exist. ", 
    18: 'Folder or file with these names already exist: ',
    # ------------------------------------------------------------- #
    20: "Undefined success. ",
    21: "Node or user was successfully created. ",
    22: "Token is Valid. ",
    23: "Data successfully changed. ",
    24: "Folder was successfully created. ",
    25: "Files was successfully saved. ",
    # ------------------------------------------------------------- #
    30: "Undefined warning. ",
    # ------------------------------------------------------------- #
    40: "Undefined info. ",
}
