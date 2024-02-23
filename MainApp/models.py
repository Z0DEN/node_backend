from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser


def user_directory_path(instance, filename):
    return f'{instance.folder.user.username}/{filename}'


class FileManager(models.Manager):
    def create_file(self, file, folder):
        try:
            file_instance = self.create(file=file, name=file.name, user=folder.user)
            file_instance.parents.add(folder)
            return file_instance, True
        except IntegrityError as e:
            return None, False


    def create_folder(self, name, parent, user, is_root):
        folder, created = self.get_or_create(name=name, parent=parent, user=user, is_root=is_root)
        return folder, created


class UserManager(models.Manager):
    def create_user(self, username):
        user = self.create(username=username)
        user.folders.create_folder(name=None, parent=None, user=user, is_root=True)
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
    parent = models.CharField(max_length=256, null=True, default='Folder')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders", default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    is_root = models.BooleanField(default=True)

    objects = FileManager()

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=256, default="file")
    parents = models.ManyToManyField(Folder, related_name="files")
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
