import datetime, secrets
import json, os
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import User, Folder, File, server_data 
from .node_auth import node_connection
from .tokens import *


global STATUS_LIST


def RJR(status=False, response_data={}, msg=False):
    response_data['status'] = status if status else None
    response_data['msg'] = STATUS_LIST[status] + msg if status and msg else STATUS_LIST[status] or msg if status or msg else "Success, or not success, that is the question"
    return JsonResponse(response_data)


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
    user_files = []
    for folder in user.folders.all():
        if folder.name is not None:
            folder_data = {
                'type': 'folder',
                'name': folder.name,
                'folder_id': folder.folder_id,
                'parent_id': list(folder.parent_id),
                'date_added': folder.date_added,
            }
            user_files.append(folder_data)
    for file in user.files.all():
        parents = list(file.parents.all().values_list('folder_id', flat=True))
        file_data = {
            'type': 'file',
            'name': file.name,
            'parent': parents,
            'date_added': file.date_added,
        }
        user_files.append(file_data) 
    return RJR(status=20, response_data={'data': user_files})


@csrf_exempt
def CreateFolder(request):
    data = json.loads(request.body)
    folder_name = data.get('folder_name', None)
    folder_id = data.get('folder_id', None)
    folder_parent_id = data.get('folder_parent_id', None)
    username = data.get('username')
    if folder_name is None or folder_parent_id is None or folder_id is None:
        return RJR(13)

    user = User.objects.get(username=username)

    _, created = user.folders.create_folder(name=folder_name, parent_id=folder_parent_id, folder_id=folder_id, user=user)

    if not created:
        return RJR(18, msg=folder_name)
    else:
        return RJR(24)


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
        _, created = File.objects.create_file(file=file, folder=folder, user=user)

        if not created:
            existed_files.append(file.name)

    if existed_files:
        return RJR(status=18, msg=', '.join(existed_files), response_data={'existed_files': existed_files})

    return RJR(25)


@csrf_exempt
def DownloadFiles(request):
    data = json.loads(request.body)
    username = data.get('username')
    file_name = data.get('file_name', False)
    if not file_name:
        return RJR(status=13, msg='file_name should be non-empty string')
    user = User.objects.get(username=username)
    try:
        file = user.files.get(name=file_name)
    except ObjectDoesNotExist:
        return RJR(status=13, msg="file does not exist")

    with open('output.txt', 'w') as print_file:
        print(file.file, file=print_file)

    return FileResponse(file.file, as_attachment=True, filename=file.name)





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
