from flask import request, Response, make_response, render_template, Blueprint
from ChatFlow.db import db_cli
from dotenv import load_dotenv
from argon2 import PasswordHasher
from bson import ObjectId
from pymongo import errors
import datetime
import jwt
import os
import random
import smtplib

load_dotenv()

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        # Extracts the information send by the client
        email = request.json['email']
        password = request.json['password']

        # Checks if user is not already verified
        entry_data = db_cli['Users'].find_one({'email': email})
        if not entry_data:
            raise KeyError(f'User {email} is not registered')
        if not entry_data['verified']:
            return Response('User is not verified', status=409)

        # Changes user status to logged_in = true
        db_cli['Users'].update_one({'email': email}, {'$set': {'logged_in': True}})

        # Gets user info from database and verifies if password matches
        entry_password = entry_data['password']
        password_verify(password, entry_password)

        # Creates Access and Refresh Tokens
        user_id = str(entry_data['_id'])
        access_token = generate_token(user_id, email, False)
        refresh_token = generate_token(user_id, email, True)

        # Stores Refresh Token in database
        query = {
            'user_id': ObjectId(user_id),
            'email': email,
            'refresh_token': refresh_token
        }
        db_cli['Tokens'].insert_one(query)

        # Creates a response object and set tokens in cookies
        res = make_response("Login successful", 200)
        res.set_cookie('chatflow-access_token', access_token)
        res.set_cookie('chatflow-refresh_token', refresh_token)
    except Exception as e:
        return Response(str(e), status=400)
    return res


@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        # Extracts the information send by the client and resends it to the database for storage
        user_email = request.json['email']
        password = password_hash(request.json['password'])
        query = {
            'name': None,
            'email': user_email,
            'password': password,
            'age': None,
            'gender': None,
            'country': None,
            'city': None,
            'address': None,
            'phone': None,
            'occupation': None,
            'logged_in': False,
            'verified': False
        }
        db_cli['Users'].insert_one(query)

        # Creates verification key, sends it to given email and stores it for confirmation
        key = generate_verification_key()
        query = {'email': user_email,
                 'key': key
                 }
        send_verification_email(user_email, key)
        print(key)  # TODO: Remove print after smtp is implemented
        db_cli['Verify'].insert_one(query)
    except errors.DuplicateKeyError:
        return Response('Email already in use!', status=409)
    except Exception as e:
        return Response(str(e), status=400)
    return Response('User successfully registered', status=201)


@auth_bp.route('/auth', methods=['DELETE'])
def logout():
    try:
        # Checks the token and then deletes copies from database
        refresh_token = request.cookies.get('chatflow-refresh_token')
        user_id = db_cli['Tokens'].find_one({'refresh_token': refresh_token})['user_id']
        db_cli['Tokens'].delete_many({'user_id': user_id})

        # Changes user status to logged_in = false
        db_cli['Users'].update_one({'_id': user_id}, {'$set': {'logged_in': False}})
    except Exception as e:
        return Response(str(e), status=403)
    return Response('Logout successful! You can close the browser.', status=200)


@auth_bp.route('/auth/token', methods=['GET'])
def token():
    error_status = 401
    try:
        # Checks the refresh token and then creates access token and sends it
        refresh_token = request.cookies.get('chatflow-refresh_token')
        token_info = db_cli['Tokens'].find_one({'refresh_token': refresh_token})
        if not token_info:
            raise Exception('Token not found in database')

        user_info = db_cli['Users'].find_one({'_id': token_info['user_id']})
        access_token = generate_token(str(user_info['_id']), token_info['email'], False)

        res = make_response("Login successful", 200)
        res.set_cookie('chatflow-access_token', access_token)
    except Exception as e:
        return Response(str(e), status=error_status)
    return res


# Returns the html page where people can insert the code
@auth_bp.route('/auth/verify', methods=['GET'])
def verify_email_page(self):
    return render_template('verify_email.html')  # TODO: Create verify email html page


@auth_bp.route('/auth/verify', methods=['POST'])
def verify_email():
    try:
        user_email = request.json['email']
        # Checks if user is not already verified
        entry_data = db_cli['Users'].find_one({'email': user_email})
        if not entry_data:
            raise KeyError(f'User {user_email} is not registered')
        if entry_data['verified']:
            return Response('User is already verified', status=409)

        # Confirms if key sent is the same as in database
        entry_data = db_cli['Verify'].find_one({'email': user_email})
        key = request.json['key']
        if entry_data['key'] != key:
            return Response('Invalid key', status=403)
        db_cli['Verify'].delete_one({'email': user_email})

        # Changes user status to verified on database
        query = {"email": user_email }
        new_values = {"$set": {"verified": True}}
        db_cli['Users'].update_one(query, new_values)
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
def send_verification_email(email, code):  # TODO: Integrate with smtp
    pass

