from django.db import models


class UserDataModel(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    FolderName = models.CharField(max_length=256)
    FolderParent = models.CharField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True)
