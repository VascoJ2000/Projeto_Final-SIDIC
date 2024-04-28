from Shared.Abstract import CLBLLinker
from Server import BLClient
from Server import server, auth
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
        pass

    def logout(self):
        pass

    def signin(self, email, password):
        pass

    def token(self):
        pass
