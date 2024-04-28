from Shared import Client
from Shared.Abstract import DLBLLinker
import requests
import json


class BLClient(Client, DLBLLinker):
    def __init__(self):
        super().__init__()

    # Business Layer to Data Layer methods
    def get_entry(self, coll, entry_id):
        url = self.server_url + f'/{coll}&{entry_id}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.status_code)

    def get_all_entries(self, coll):
        url = self.server_url + f'/all/{coll}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.status_code)

    def add_entry(self, data=None):
        if data is None:
            return False
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = self.server_url
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return True
        raise Exception(response.status_code)

    def update_entry(self, coll=None, entry_id=None, value=None, new_data=None):
        if coll or entry_id or new_data is None:
            return False
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = self.server_url
        data = {"coll": coll, "entry_id": entry_id, "new_values": {"$set": {value: new_data}}}
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 202:
            return True
        raise Exception(response.status_code)

    def delete_entry(self, coll, entry_id):
        url = self.server_url + f'/{coll}&{entry_id}'
        response = requests.delete(url)
        if response.status_code == 204:
            return True
        raise Exception(response.status_code)
    