from __main__ import app
from flask import request, Response, make_response, render_template
from db.client import db_cli
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


@app.route('/auth/<email>&<password>', methods=['GET'])
def login(email, password):
    try:
        # Checks if user is not already verified
        entry_data = db_cli.db['Users'].find_one({'email': email})
        if not entry_data:
            raise KeyError(f'User {email} is not registered')
        if not entry_data['verified']:
            return Response('User is not verified', status=409)

        # Gets user info from database and verifies if password matches
        entry_password = entry_data['password']
        password_verify(password, entry_password)

        # Creates Access and Refresh Tokens
        user_id = str(entry_data['_id'])
        access_token = generate_token(user_id, email, False)
        refresh_token = generate_token(user_id, email, True)

        # Stores Refresh Token in database
        query = {'user_id': ObjectId(user_id),
                 'email': email,
                 'refresh_token': refresh_token
                 }
        db_cli.db['Tokens'].insert_one(query)

        # Creates a response object and set tokens in cookies
        res = make_response("Login successful", 200)
        res.set_cookie('chatflow-access_token', access_token)
        res.set_cookie('chatflow-refresh_token', refresh_token)
    except Exception as e:
        return Response(str(e), status=400)
    return res


@app.route('/auth', methods=['POST'])
def signin():
    try:
        # Extracts the information send by the client and resends it to the database for storage
        username = request.json['name']
        user_email = request.json['email']
        password = password_hash(request.json['password'])
        query = {'name': username,
                 'email': user_email,
                 'password': password,
                 'verified': False
                 }
        db_cli.db['Users'].insert_one(query)

        # Creates verification key, sends it to given email and stores it for confirmation
        key = generate_verification_key()
        query = {'email': user_email,
                 'key': key
                 }
        send_verification_email(user_email, key)
        print(key)  # TODO: Remove print after smtp is implemented
        db_cli.db['Verify'].insert_one(query)
    except errors.DuplicateKeyError:
        return Response('Email already in use!', status=409)
    except Exception as e:
        return Response(str(e), status=400)
    return Response('User successfully registered', status=201)


@app.route('/auth', methods=['DELETE'])
def logout():
    try:
        refresh_token = request.cookies.get('chatflow-refresh_token')
        user_id = db_cli.db['Tokens'].find_one({'refresh_token': refresh_token})['user_id']
        db_cli.db['Tokens'].delete_many({'user_id': user_id})
    except Exception as e:
        return Response(str(e), status=403)
    return Response('Logout successful! You can close the browser.', status=200)


@app.route('/auth/token', methods=['GET'])
def token():
    pass


# Returns the html page where people can insert the code
@app.route('/auth/verify', methods=['GET'])
def verify_email_page(self):
    return render_template('verify_email.html')  # TODO: Create verify email html page


@app.route('/auth/verify', methods=['POST'])
def verify_email():
    try:
        user_email = request.json['email']
        # Checks if user is not already verified
        entry_data = db_cli.get_entry('Users', 'email', user_email)[0]
        if entry_data['verified']:
            return Response('User is already verified', status=409)

        # Confirms if key sent is the same as in database
        entry_data = db_cli.get_entry('Verify', 'email', user_email)[0]
        key = request.json['key']
        if entry_data['key'] != key:
            return Response('Invalid key', status=403)

        # Changes user status to verified on database
        json_data = {"coll": "Users",
                     "identifier": "email",
                     "entry_id": user_email,
                     "new_values": {"$set": {"verified": True}}
                     }
        db_cli.update_entry(json_data)
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

