from Database.db import DB
from Shared.middleware import auth
from flask import request, Response, g
from dotenv import load_dotenv
from pymongo import errors
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
    @auth(os.getenv('SECRET_KEY_SD'))
    def get_entry(self, collection, query):
        try:
            coll = self.db.db.collection[collection]
            doc = coll.find(query)
        except Exception as e:
            return Response('404 Not Found', str(e))
        return Response(doc, mimetype='application/json'), 201

    @auth(os.getenv('SECRET_KEY_SD'))
    def add_entry(self, collection, query):
        try:
            coll = self.db.db.collection[collection]
            coll.insert_one(query)
        except errors.CollectionInvalid as e:
            return Response('404 Not Found', str(e))
        except Exception as e:
            return Response('400 Not Found', str(e))
        return Response('201 Created')

    @auth(os.getenv('SECRET_KEY_SD'))
    def delete_entry(self, collection, query):
        try:
            coll = self.db.db.collection[collection]
            coll.delete_many(query)
        except Exception as e:
            return Response('400 Not Found', str(e))
        return Response('200 OK')

    @auth(os.getenv('SECRET_KEY_SD'))
    def update_entry(self, collection, query, new_values):
        try:
            coll = self.db.db.collection[collection]
            coll.update_one(query, new_values)
        except Exception as e:
            return Response('400 Not Found', str(e))
        return Response('200 OK')

    # Auth routes
    @auth(os.getenv('SECRET_KEY_SD_REFRESH'))
    def create_access_token(self):
        pass

    def create_refresh_token(self):
        pass
