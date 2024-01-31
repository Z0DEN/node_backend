from django.http import HttpResponse
from MainApp.models import User, Folder, File

def upload_file(request):
    if request.method == 'POST':
        user = User.objects.get(username="copilot")
        if user is None:
            user = User.objects.create_user(username="copilot")

        folder = user.folders.get(name="test")
        if folder is None:
            folder = Folder.objects.create_folder(name="test", parent=None, user=user)

        file = request.FILES['file']  # 'file' это имя вашего поля input type=file в форме
        file = File.objects.create_file(name=file.name, folder=folder, file=file)

        return HttpResponse('File uploaded successfully')
