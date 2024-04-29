from Shared.Abstract import CLBLLinker
from Server.client import BLClient
from Server.middleware import auth
from flask import request, Response, g
import json


class Controller(CLBLLinker):
    def __init__(self):
        super().__init__()
        self.cli = BLClient()

    # User methods
    def get_user(self, user_id, email):
        pass

    def add_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass

    # Authentication methods
    def login(self, email, password):
        try:
            print(email)
            print(type(email))
            doc_json = self.cli.get_entry('Users', 'email', email)
            doc = doc_json['doc']
        except Exception as e:
            return Response(str(e), status=404)
        return Response(doc, status=200, mimetype='application/json')

    def logout(self):
        pass

    def signin(self, email, password):
        pass

    def token(self):
        pass
