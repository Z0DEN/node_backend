import uuid
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser


def user_directory_path(instance, filename):
    return f'{instance.user.username}/{filename}'


class FileManager(models.Manager):
    def create_file(self, file, folder, item_id, user):
        try:
#            with open('output.txt', 'w') as print_file:
#                print(file, folder, item_id, user, file=print_file)
            file_instance = self.create(file=file, name=file.name, item_id=item_id, user=user)
            file_instance.parent_id.add(folder)
            return file_instance, True
        except IntegrityError as e:
            return None, False


    def create_folder(self, name, parent_id, item_id, user):
        folder_exists = user.folders.filter(name=name, parent_id=parent_id).exists()
        if folder_exists:
            return None, False
        folder = self.create(name=name, parent_id=parent_id, item_id=item_id, user=user)
        return folder, True 


class UserManager(models.Manager):
    def create_user(self, username):
        if User.objects.filter(username=username).exists():
            return None
        user = self.create(username=username)
        user.folders.create_folder(name=None, parent_id=None, item_id=None, user=user)
        return user


# ---------------------------------------------------------------------------------------------------- #

class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return self.username


class Folder(models.Model):
    name = models.CharField(max_length=256, null=True, default=None)
    parent_id = models.CharField(max_length=256, null=True, default=None)
    item_id = models.CharField(max_length=256, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders", default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = FileManager()

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=256, default="file")
    item_id = models.CharField(max_length=256, null=True, default=None)
    parent_id = models.ManyToManyField(Folder, related_name="child_files")
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files", default=1)
    objects = FileManager()

    def __str__(self):
        return self.name


class server_data(models.Model):
    secret_key = models.CharField(unique=True, max_length=1024)
    personal_key = models.CharField(max_length=64, default="personal_key")
    main_server_access_token = models.CharField(unique=True, max_length=1024)
    main_server_refresh_token = models.CharField(unique=True, max_length=1024)
    date_added = models.DateTimeField(auto_now=True)
