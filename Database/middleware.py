from flask import request, Response, g
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


class JWTMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        header = request.headers
        try:
            request.decoded_jwt = authenticate(header)
        except Exception as e:
            start_response('401 Unauthorized', [])
            return [bytes(str(e), 'utf-8')]
        return self.app(environ, start_response)


def authenticate(header):
    if 'Authorization' in header:
        auth_header = header.get('Authorization')
        token = auth_header.split(' ')[1]
    else:
        raise Exception('No authorization header')
    decoded = access_token_verify(token)
    return decoded


def access_token_verify(token):
    try:
        token_decoded = jwt.decode(token, os.getenv('SECRET_KEY_SD'), algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError as e:
        raise Exception("Token is Invalid: " + str(e))
    else:
        return token_decoded


def refresh_token_verify(token):
    pass


def create_access_token(token):
    pass


def create_refresh_token(token):
    pass
