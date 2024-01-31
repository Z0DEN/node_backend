from .models import User, Folder, File

user = User.objects.create(username="copilot")

folder = Folder.objects.create(name="test", user=user)

file = File.objects.create_file(upload_to="files", name="example.txt", folder=folder, user=user)

