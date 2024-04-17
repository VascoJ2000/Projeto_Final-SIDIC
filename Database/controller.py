from Database.db import DB
from Shared.middleware import auth
from flask import request, Response, g
from dotenv import load_dotenv
from pymongo import errors
import jwt
import secrets
import os

load_dotenv()


class Controller:
    def __init__(self):
        try:
            self.db = DB(os.getenv('DB_CLIENT'), os.getenv('DB_CONNECT'))
        except Exception as e:
            print('Erro: ' + str(e))
            try:
                self.db = DB(os.getenv('DB_CLIENT_BACKUP'), os.getenv('DB_CONNECT'))
            except Exception as e:
                print('Erro: ' + str(e))

    # Common routes
    @auth(key=os.getenv('SECRET_KEY_SD'))
    def get_entry(self, collection, query):
        try:
            coll = self.db.db.collection[collection]
            doc = coll.find(query)
        except Exception as e:
            return Response('404 Not Found', str(e))
        return Response(doc, mimetype='application/json'), 201

    @auth(key=os.getenv('SECRET_KEY_SD'))
    def add_entry(self):
        try:
            request_json = request.get_json()
            collection = request_json['collection']
            query = request_json['query']
            coll = self.db.db.collection[collection]
            coll.insert_one(query)
        except errors.CollectionInvalid as e:
            return Response('404 Not Found', str(e))
        except Exception as e:
            return Response('400 Bad Request', str(e))
        return Response('201 Created')

    @auth(key=os.getenv('SECRET_KEY_SD'))
    def delete_entry(self):
        try:
            request_json = request.get_json()
            collection = request_json['collection']
            query = request_json['query']
            coll = self.db.db.collection[collection]
            coll.delete_many(query)
        except Exception as e:
            return Response('400 Not Found', str(e))
        return Response('200 OK')

    @auth(key=os.getenv('SECRET_KEY_SD'))
    def update_entry(self):
        try:
            request_json = request.get_json()
            collection = request_json['collection']
            query = request_json['query']
            new_values = request_json['new_values']
            coll = self.db.db.collection[collection]
            coll.update_one(query, new_values)
        except Exception as e:
            return Response('400 Not Found', str(e))
        return Response('200 OK')

    # Auth routes
    def create_access_token(self):
        try:
            ip_client = request.remote_addr
            coll = self.db.db.collection['Servers']
            query = {'ip': ip_client}
            doc = coll.find({}, query)
            if doc == {}:
                return Response('403 Forbidden', 'IP does not match allowed connections')

            token_data = request.get_json()['Token']
            key = doc[0]['Key']
            decoded = jwt.decode(token_data, key=key, algorithms=['HS256'])
            new_key = decoded['new_key']
            new_values = {'Key': new_key}
            coll.update_one(query, new_values)

            server_type = decoded['server_type']
            token = {'ip': ip_client, 'server_type': server_type}
            access_token = jwt.encode(token, os.getenv('SECRET_KEY_SD'), algorithm='HS256')
        except Exception as e:
            return Response('400 Bad Request', str(e))
        return Response(access_token, mimetype='application/json'), 201

    def create_temp_key(self):
        try:
            ip_client = request.remote_addr
            coll = self.db.db.collection['Servers']
            query = {'ip': ip_client}
            tmp_key = secrets.token_urlsafe(32)
            new_values = {'Key': tmp_key}
            coll.update_one(query, new_values)
            token = jwt.encode(new_values, os.getenv('SECRET_KEY_SD'), algorithm='HS256')
        except Exception as e:
            return Response('404 Not Found', str(e))
        return Response(token, mimetype='application/json'), 201
