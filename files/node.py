import json, requests, os, sys

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
print("\nData:", json.dumps(data, indent=4))
response = None

try:
    response = requests.post(url1, data=json.dumps(data_local_conn), headers=headers)
    print("Основной сервер подключен локально", "\n")
except requests.exceptions.RequestException:
    try:
        response = requests.post(url2, data=json.dumps(data), headers=headers)
    except requests.exceptions.RequestException:
        print("Не удалось подключиться к серверу.", "\n")

if response == None:
    sys.exit()

print("Status:", response.status_code, "\n")
print("Response:", response.text, "\n")
