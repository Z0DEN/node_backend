# Generated by Django 4.2.7 on 2023-12-20 14:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_remove_main_user_model_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_user_model',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server_data',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server_data',
            name='local_server_access_token',
            field=models.CharField(default='local_access_token', max_length=1024, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server_data',
            name='local_server_refresh_token',
            field=models.CharField(default='local_refresh_token', max_length=1024, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server_data',
            name='secret_key',
            field=models.CharField(default='secret_key', max_length=1024, unique=True),
            preserve_default=False,
        ),
    ]
