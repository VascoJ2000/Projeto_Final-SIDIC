import requests
import time


class Client:
    def __init__(self):
        self.server_url = None

    def get_request(self, route, search_id1, search_id2, token=None):
        url = self.server_url + f"{route}/{search_id1}&{search_id2}"
        if token:
            if search_id1 is None and search_id2 is None:
                url = self.server_url + f"{route}/"
            response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response
        else:
            raise Exception('Error: ' + str(response.json()['Error']))

    def post_request(self, route, data, token=None):
        url = self.server_url + route
        if token:
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post(url, headers=headers, json=data)
        else:
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response
        else:
            raise Exception('Error: ' + str(response.json()['Error']))

    def update_request(self, route, data, token=None):
        url = self.server_url + route
        if token:
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}
            response = requests.put(url, headers=headers, json=data)
        else:
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            return response
        else:
            raise Exception('Error: ' + str(response.json()['Error']))

    def delete_request(self, route, data, token=None):
        url = self.server_url + f"{route}"
        if token:
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}
            response = requests.delete(url, headers=headers, json=data)
        else:
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.delete(url, headers=headers, json=data)

        if response.status_code == 200:
            return response
        else:
            raise Exception('Error: ' + str(response.json()['Error']))

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
