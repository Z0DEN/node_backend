from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class main_user_model(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=255)
    user_access_token = models.CharField(max_length=1024, default="access_token")
    user_refresh_token = models.CharField(max_length=1024, default="refresh_token")
    secret_key = models.CharField(max_length=64, default="secret_key")
    date_added = models.DateTimeField(auto_now_add=True)



class user_data_model(models.Model):
    username = models.OneToOneField(main_user_model, on_delete=models.CASCADE)
    FolderName = models.CharField(max_length=256)
    FolderParent = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)


class server_data(models.Model):
    secret_key = models.CharField(unique=True, max_length=1024)
    main_server_access_token = models.CharField(unique=True, max_length=1024)
    main_server_refresh_token = models.CharField(unique=True, max_length=1024)
    local_server_access_token = models.CharField(unique=True, max_length=1024)
    local_server_refresh_token = models.CharField(unique=True, max_length=1024)
    date_added = models.DateTimeField(auto_now=True)
