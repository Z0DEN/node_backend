import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import MainUserModel, UserDataModel


def AddUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        if not user:
            return HttpResponse("POST request have no 'username' field")

        new_user = MainUserModel(
                username = username,
        )

        new_user.save()
        
        new_user_data = UserDataModel(
            username=new_user,
            FolderName=None,
            FolderParent=None,
        )

        response_data = {
            'success': True,
        }

        return JsonResponse(response_data, safe=False)

    else:
        print('method=get')
        return HttpResponse('Invalid request method.')
