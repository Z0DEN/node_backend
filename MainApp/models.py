from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class main_user_model(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=255)
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=1024)
    secret_key = models.CharField(max_length=64)



class user_data_model(models.Model):
    username = models.OneToOneField(main_user_model, on_delete=models.CASCADE)
    FolderName = models.CharField(max_length=256)
    FolderParent = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)


class server_data(models.Model):
    main_server_access_token = models.CharField(unique=True, max_length=1024)
    main_server_refresh_token = models.CharField(unique=True, max_length=1024)
