from Shared.Abstract import CLBLLinker
from Server.client import BLClient
from Server.middleware import auth
from flask import request, Response, g, make_response, render_template
from dotenv import load_dotenv
from argon2 import PasswordHasher
import datetime
import jwt
import os
import random
import smtplib

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
            # Checks if user is not already verified
            entry_data = self.cli.get_entry('Users', 'email', email)[0]
            if not entry_data['verified']:
                return Response('User is not verified', status=409)

            # Gets user info from database and verifies if password matches
            entry_password = entry_data['password']
            password_verify(password, entry_password)

            # Creates Access and Refresh Tokens
            user_id = entry_data['_id']
            access_token = generate_token(user_id, email, False)
            refresh_token = generate_token(user_id, email, True)

            # Stores Refresh Token in database
            json_data = {'coll': 'Tokens',
                         'query': {
                             'user_id': user_id,
                             'email': email,
                             'refresh_token': refresh_token
                         }}
            self.cli.add_entry(json_data)

            # Creates a response object and set tokens in cookies
            res = make_response("Login successful", 200)
            res.set_cookie('chatflow-access_token', access_token)
            res.set_cookie('chatflow-refresh_token', refresh_token)
        except Exception as e:
            return Response(str(e), status=400)
        return res

    def signin(self):
        try:
            # Extracts the information send by the client and resends it to the data layer for storage
            username = request.json['name']
            user_email = request.json['email']
            password = password_hash(request.json['password'])
            json_data = {'coll': 'Users',
                         'query': {
                             'name': username,
                             'email': user_email,
                             'password': password,
                             'verified': False
                         }}
            self.cli.add_entry(json_data)

            # Creates verification key, sends it to given email and stores it for confirmation
            key = generate_verification_key()
            json_data = {'coll': 'Verify',
                         'query': {
                             'email': user_email,
                             'key': key
                         }}
            send_verification_email(user_email, key)
            # Remove print after smtp is implemented
            print(key)
            self.cli.add_entry(json_data)
        except Exception as e:
            return Response(str(e), status=400)
        return Response('User successfully registered', status=201)

    @auth(key=os.getenv('REFRESH_KEY'))
    def logout(self):
        pass

    @auth(key=os.getenv('REFRESH_KEY'))
    def token(self):
        pass

    # Returns the html page where people can insert the code
    def verify_email_page(self):
        pass

    def verify_email(self):
        try:
            user_email = request.json['email']
            # Checks if user is not already verified
            entry_data = self.cli.get_entry('Users', 'email', user_email)[0]
            if entry_data['verified']:
                return Response('User is already verified', status=409)

            # Confirms if key sent is the same as in database
            entry_data = self.cli.get_entry('Verify', 'email', user_email)[0]
            key = request.json['key']
            if entry_data['key'] != key:
                return Response('Invalid key', status=403)

            # Changes user status to verified on database
            json_data = {"coll": "Users",
                         "identifier": "email",
                         "entry_id": user_email,
                         "new_values": {"$set": {"verified": True}}
                         }
            self.cli.update_entry(json_data)
        except Exception as e:
            return Response(str(e), status=400)
        return Response('User successfully verified', status=202)


def password_hash(password):
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password


def password_verify(input_password, hashed_password):
    ph = PasswordHasher()
    if ph.verify(hashed_password, input_password):
        return True
    raise Exception('Password is invalid!')


# Generates a new jwt
# refresh works as a conditional that defines the type of token
def generate_token(user_id, email, refresh):
    if not refresh:
        expires = datetime.timedelta(minutes=30)
        key = os.getenv('ACCESS_KEY')
    else:
        expires = datetime.timedelta(weeks=1)
        key = os.getenv('REFRESH_KEY')
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + expires
    }
    jwt_token = jwt.encode(payload, key, algorithm='HS256')
    return jwt_token


# Generates a new key to confirm email ownership
def generate_verification_key():
    return ''.join(random.choices('0123456789', k=6))


# Sends given message to given email
# TODO: Integrate with smtp
def send_verification_email(email, code):
    pass
