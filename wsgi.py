import os
from django.core.wsgi import get_wsgi_application
from daphne import server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
