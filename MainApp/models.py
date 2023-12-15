from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class MainUserModel(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=255)


class UserDataModel(models.Model):
    username = models.OneToOneField(MainUserModel, on_delete=models.CASCADE)
    FolderName = models.CharField(max_length=256)
    FolderParent = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)
