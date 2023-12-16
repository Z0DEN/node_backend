#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json, requests, os, sys


def node_connection():
    url1 = 'http://192.168.0.98:8005/NodeConnection/'
    url2 = 'http://176.197.34.213:8005/NodeConnection/'
    headers = {'Content-Type': 'application/json'}
    
    IN_IP = os.environ.get('IN_IP')
    EX_IP = os.environ.get('EX_IP')
    node_domain = os.environ.get('HOSTNAME')
    UUID = os.environ.get('UUID')
    
    data = {
        'node_domain': node_domain,
        'IN_IP': IN_IP,
        'EX_IP': EX_IP,
        'UUID' : UUID,
        'local_connection': True,
    }

    response = None
    
    try:
        response = requests.post(url1, data=json.dumps(data), headers=headers)
    except requests.exceptions.RequestException:
         data["local_connection"] = False
         response = requests.post(url2, data=json.dumps(data), headers=headers)
    
    if response == None:
        sys.exit()
        print("No response was received")

    data = response.json() 

    msg = data["msg"]
    status = data["status"]
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    if status >= 20 and status < 30:
        print(f"Success: {status} \nmsg: {msg} \naccess_token: {access_token} \nrefresh_token: {refresh_token}")
    elif status < 20:
        print(f"Failed to make connection: {status} \nmsg: {msg} \naccess_token: {access_token} \nrefresh_token: {refresh_token}")


def main():
    """Run administrative tasks."""
    node_connection()
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
