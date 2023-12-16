#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json, requests, os, sys


def node_connection():
    url1 = 'http://192.168.0.98:8001/NodeConnection/'
    url2 = 'http://176.197.34.213:8001/NodeConnection/'
    headers = {'Content-Type': 'application/json'}
    
    IN_IP = os.environ.get('IN_IP')
    EX_IP = os.environ.get('EX_IP')
    node_domain = os.environ.get('HOSTNAME')
    UUID = os.environ.get('UUID')
    
    data_local_conn = {
        'node_domain': node_domain,
        'IN_IP': IN_IP,
        'EX_IP': EX_IP,
        'UUID' : UUID,
        'local_connection': True,
    }
    data = {
        'node_domain': node_domain,
        'IN_IP': IN_IP,
        'EX_IP': EX_IP,
        'UUID' : UUID,
        'local_connection': False,
    }
    response = None
    
    try:
        response = requests.post(url1, data=json.dumps(data_local_conn), headers=headers)
    except requests.exceptions.RequestException:
        try:
            response = requests.post(url2, data=json.dumps(data), headers=headers)
        except requests.exceptions.RequestException:
    
    if response == None:
        sys.exit()
    

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    node_connection()
