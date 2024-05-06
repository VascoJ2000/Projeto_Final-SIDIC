from functools import wraps
from flask import request, Response, g
from dotenv import load_dotenv
from ChatFlow.db import db_cli
import jwt
import os

load_dotenv()


def auth_access(func):
    @wraps(func)
    def _auth_access(*args, **kwargs):
        if request.cookies.get('chatflow-access_token'):
            try:
                g.decoded_jwt = verify_token(request.cookies.get('chatflow-access_token'))
                email = g.decoded_jwt['email']
            except Exception as e:
                return Response(str(e), status=401)
            if db_cli['Users'].find_one({'email': email})['logged_in']:
                return func(*args, **kwargs)

            return Response('Session timeout. Pls login again!', 403)

        return Response('No token', status=403)

    return _auth_access


def verify_token(token):
    try:
        token_decoded = jwt.decode(token, os.getenv('ACCESS_KEY'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except Exception as e:
        raise Exception("Token is Invalid: " + str(e))
    return token_decoded
