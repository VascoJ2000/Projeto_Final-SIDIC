from Shared.Abstract import CLBLLinker
from Server.client import BLClient
from Server.middleware import auth
from flask import request, Response, g, jsonify
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
            # Gets user info from database and verifies if password matches
            doc = self.cli.get_entry('Users', 'email', email)['doc']
            doc_password = doc['password']
            password_verify(password, doc_password)

            # Creates Access and Refresh Tokens
            user_id = doc['_id']
            user_email = doc['email']
            access_token = generate_token(user_id, user_email, False)
            refresh_token = generate_token(user_id, user_email, True)

            # Stores Refresh Token in database
            # TODO: Check if data is registered in database
            json_data = {'coll': 'Tokens',
                         'query': {
                            'user_id': user_id,
                            'email': user_email,
                            'refresh_token': refresh_token
                         }}
            self.cli.add_entry(json_data)
        except Exception as e:
            return Response(str(e), status=404)
        return jsonify({'Token': {'Access': access_token, 'Refresh': refresh_token}}, status=200)

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


def generate_token(user_id, email, refresh):
    if not refresh:
        expires = datetime.timedelta(minutes=30)
        key = os.getenv('ACCESS_KEY')
    else:
        expires = datetime.timedelta(weeks=1)
        key = os.getenv('REFRESH_KEY')
    payload = {
        'User_id': user_id,
        'Email': email,
        'exp': datetime.datetime.utcnow() + expires
    }
    jwt_token = jwt.encode(payload, key, algorithm='HS256')
    return jwt_token
