from django.db import models
from django.contrib.auth.models import AbstractBaseUser


def user_directory_path(instance, filename):
    return f'{instance.folder.user.username}/{filename}'


class FileManager(models.Manager):
    def create_file(self, name, folder, file):
        file = self.create(file=file, name=name, folder=folder)
        return file


    def create_folder(self, name, parent, user):
        folder = self.create(name=name, parent=parent, user=user)
        return folder



class UserManager(models.Manager):
    def create_user(self, username):
        user = self.create(username=username)
        return user

    def get_all_users(self):
        users = self.all()
        return users

# ---------------------------------------------------------------------------------------------------- #

class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return self.username


class Folder(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    date_added = models.DateTimeField(auto_now_add=True)

    objects = FileManager()

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=256)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    date_added = models.DateTimeField(auto_now_add=True)

    objects = FileManager()

    def __str__(self):
        return self.name


class server_data(models.Model):
    secret_key = models.CharField(unique=True, max_length=1024)
    personal_key = models.CharField(max_length=64, default="personal_key")
    main_server_access_token = models.CharField(unique=True, max_length=1024)
    main_server_refresh_token = models.CharField(unique=True, max_length=1024)
    date_added = models.DateTimeField(auto_now=True)
