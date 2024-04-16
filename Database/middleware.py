from flask import request, Response, g
from functools import wraps
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


def auth(func):
    @wraps(func)
    def _auth(*args, **kwargs):
        try:
            token = authorization_verify(request.headers)
            if request.path.startswith('/token/refresh'):
                key = os.getenv('SECRET_KEY_SD')
            elif request.path.startswith('/'):
                key = os.getenv('SECRET_KEY_SD')
            else:
                return _auth
            g.decoded = token_verify(token, key)
        except Exception as e:
            return Response('401 Unauthorized', str(e))
        return _auth


def authorization_verify(header):
    if 'Authorization' in header:
        auth_header = header.get('Authorization')
        token = auth_header.split(' ')[1]
    else:
        raise Exception('No authorization header')
    return token


def token_verify(token, key):
    try:
        token_decoded = jwt.decode(token, key, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError as e:
        raise Exception("Token is Invalid: " + str(e))
    else:
        return token_decoded
