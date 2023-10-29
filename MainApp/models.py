from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class clouduser(AbstractUser):
    node_domain = models.CharField(max_length=20)
    groups = models.ManyToManyField(
        Group,
        related_name='clouduser_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='clouduser_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class NodeModel(models.Model):
    node_domain = models.CharField(max_length=20, unique=True)
    ip_address = models.CharField(max_length=12, unique=True)
    user_quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.node_domain
