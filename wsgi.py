import os
from django.core.wsgi import get_wsgi_application
from daphne import server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'node_backend.settings')

application = get_wsgi_application()
