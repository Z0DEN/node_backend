import requests
import socket

def get_hostname():
    try:
        hostname = socket.gethostname()  # Получаем доменное имя компьютера
        return hostname
    except socket.error:
        return "Не удалось получить доменное имя"

print(get_hostname())


def get_ip_address():
    try:
        # Создаем временное сокетное соединение
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))  # IP-адрес Google Public DNS и любой порт
        ip_address = sock.getsockname()[0]  # Получаем IP-адрес
        sock.close()  # Закрываем сокет
        return ip_address
    except socket.error:
        return "Не удалось получить IP-адрес"


url = 'http://192.168.0.98:8001/NodeConnection/'

headers={'Content-Type': 'application/json'}

ip_address = get_ip_address()
node_domain = get_hostname() 

data = {
    'node_domain': ip_address,
    'ip_address': node_domain,
}

response = requests.post(url, data=data, headers=headers)

if response.status_code == 201:
    print('Нода успешно добавлена')
    node = response.json()
    print(node)
else:
    print('Ошибка при добавлении ноды')

