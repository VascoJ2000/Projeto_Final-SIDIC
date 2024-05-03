from flask import request, Response, g
from functools import wraps
import jwt


def auth(*args, **kwargs):
    def _auth(func):
        @wraps(func)
        def __auth():
            try:

                g.token = cookies_verify(True)
                g.decoded = token_verify(g.token, kwargs['key'])
            except Exception as e:
                return Response('401 Unauthorized', str(e))
        return __auth
    return _auth


def cookies_verify(refresh):
    if refresh:
        return request.cookies.get('chatflow-refresh_token')
    else:
        return request.cookies.get('chatflow-access_token')


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
