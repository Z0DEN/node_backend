from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import MainUserModel, UserDataModel


def AddUser(request):
    if request.method == 'POST':

        user = request.POST['username']

        if not user:
            return HttpResponse("POST request have no 'username' field")

        new_user = UserDataModel(
            username=user,
            FolderName=None,
            FolderParent=None,
            date_added=
        )

        new_user.save()

        # Add a Content-Type header to the response
        response = JsonResponse({
            'success': True,
            'node_domain': node_domain,
            'ip_address': ip_address,
            'date': date,
        })


    else:
        print('method=get')
        return HttpResponse('Invalid request method.')
