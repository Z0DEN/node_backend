from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MainApp'

#    def ready(self):
#        from .models import server_data
#        from .signals import node_connection
#
#        from django.db.models.signals import post_migrate
#        
#        post_migrate.connect(node_connection, sender=server_data)
