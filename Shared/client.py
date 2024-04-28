import requests
import time


class Client:
    def __init__(self):
        self.server_url = None

    def connect(self, host, port, max_attempts=12):
        for i in range(max_attempts):
            response = requests.get(f'http://{host}:{port}/')
            if response.status_code == 200:
                data = response.json()
                server_ip = data['Server_ip']
                server_port = str(data['Server_port'])
                self.server_url = f'http://{server_ip}:{server_port}/'
                return print(f'Cliente connected to server on port {server_port}')
            elif response.status_code == 425:
                time.sleep(2)
            else:
                raise Exception(str(response.json()['error']))
        raise Exception('Cliente cannot find a available server')
