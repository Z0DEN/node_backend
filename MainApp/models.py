from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser


def user_directory_path(instance, filename):
    return f'{instance.folder.user.username}/{filename}'


class FileManager(models.Manager):
    def create_file(self, file, name, folder):
        try:
            file, created = self.get_or_create(file=file, name=name, parent=folder.name, folder=folder)
            return file, created
        except IntegrityError:
            return None, False


    def create_folder(self, name, parent, user):
        folder, created = self.get_or_create(name=name, parent=parent, user=user)
        return folder, created


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
    name = models.CharField(max_length=256, default='Folder')
    parent = models.CharField(max_length=256, default='root')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders", default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = FileManager()

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(unique=True, max_length=256, default="file")
    parent = models.CharField(max_length=256, default='root')
    date_added = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files", default=1)
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
