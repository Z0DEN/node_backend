import uuid
from django.db import models, IntegrityError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser


def user_directory_path(instance, filename):
    return f'{instance.user.username}/{filename}'


class FolderDeletionError(Exception):
    pass


class FileManager(models.Manager):
    def create_file(self, file, item_id, parent_id):
        user = self.instance
        if parent_id == 'null':
            parent_id = None
        try:
            file_instance = self.create(file=file, name=file.name, item_id=item_id, parent_id=[parent_id], user=user)
            return file_instance, True
        except IntegrityError as e:
            return None, False


    def add_parent(item_id, parent_id):
        user = self.instance
        file_instance = user.files.get(item_id=item_id)
        parent_list = file_instance.parent_id
        parent_list.append(parent_id)
        file_instance.parent_id = parent_list
        file_instance.save()
        

    def create_folder(self, name, parent_id, item_id):
        user = self.instance
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
        return user




# ---------------------------------------------------------------------------------------------------- #

class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    available_space = models.BigIntegerField(default=16_106_127_360)
    taken_space = models.BigIntegerField(default=0)

    objects = UserManager()


    def get_files(self):
        user_files = []
        for file in self.files.all():
            file_data = {
                'type': 'file',
                'name': file.name,
                'item_id': file.item_id,
                'parent_id': file.parent_id,
                'date_added': file.date_added,
                'size': file.file.size,
            }
            user_files.append(file_data) 
        return user_files


    def get_folders(self):
        user_folders = []
        for folder in self.folders.all():
            folder_data = {
                'type': 'folder',
                'name': folder.name,
                'item_id': folder.item_id,
                'parent_id': [folder.parent_id],
                'date_added': folder.date_added,
            }
            user_folders.append(folder_data)
        return user_folders


    def __str__(self):
        return self.username


class Folder(models.Model):
    name = models.CharField(max_length=256, null=True, default=None)
    parent_id = models.CharField(max_length=256, null=True, default=None)
    item_id = models.CharField(max_length=256, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders", default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = FileManager()


    def delete(self, *args, **kwargs):
        try:
            child_folders = Folder.objects.filter(user=self.user, parent_id=self.item_id)
            for folder in child_folders:
                folder.delete()

            files = File.objects.filter(user=self.user, parent_id__contains=[self.item_id])
            for file in files:
                file.delete()
        except Exception as e:
            raise FolderDeletionError(f"{self.name}")
        else:
            super().delete(*args, **kwargs)

        return       
    
    
        def __str__(self):
            return self.name


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=256, default="file")
    item_id = models.CharField(unique=True, max_length=256, null=True, default=None)
    parent_id = models.JSONField(blank=True, null=True, default=list)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files", default=1)

    objects = FileManager()


    def delete(self, *args, **kwargs):
        self.user.taken_space -= self.file.file.size
        self.user.save()
        self.file.delete(save=False)
        super(File, self).delete(*args, **kwargs)


    def __str__(self):
        return self.name


class server_data(models.Model):
    secret_key = models.CharField(unique=True, max_length=1024)
    personal_key = models.CharField(max_length=64)
    main_server_access_token = models.CharField(unique=True, max_length=1024)
    main_server_refresh_token = models.CharField(unique=True, max_length=1024)
    date_added = models.DateTimeField(auto_now=True)
