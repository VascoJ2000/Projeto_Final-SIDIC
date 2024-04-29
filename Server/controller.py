from Shared.Abstract import CLBLLinker
from Server.client import BLClient
from Server.middleware import auth
from flask import request, Response, g
from dotenv import load_dotenv
from argon2 import PasswordHasher
import datetime
import json
import jwt
import os


load_dotenv()


class Controller(CLBLLinker):
    def __init__(self):
        super().__init__()
        self.cli = BLClient()

    # User methods
    @auth(key=os.getenv('ACCESS_KEY'))
    def get_user(self, user_id, email):
        pass

    @auth(key=os.getenv('ACCESS_KEY'))
    def add_user(self):
        pass

    @auth(key=os.getenv('ACCESS_KEY'))
    def update_user(self):
        pass

    @auth(key=os.getenv('ACCESS_KEY'))
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


def password_hash(password):
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password


def password_verify(input_password, hashed_password):
    ph = PasswordHasher()
    if ph.verify(input_password, hashed_password):
        return True
    raise Exception('Password is invalid!')


def generate_token(user_data):
    payload = {
        'User_id': user_data['User_id'],
        'Email': user_data['Email'],
        'Username': user_data['Username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    jwt_token = jwt.encode(payload, os.getenv('ACCESS_KEY'), algorithm='HS256')
    return jwt_token
