import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from MainApp.models import main_user_model, user_data_model 


def test(request):
    return render(request, "main/home.html")

@csrf_exempt
def AddUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        if not username:
            return HttpResponse("POST request have no 'username' field")

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

        response_data = {
            'success': True,
        }

        return JsonResponse(response_data, safe=False)

    else:
        print('method=get')
        return HttpResponse('Invalid request method.')
