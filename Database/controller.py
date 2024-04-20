from Database.client import Client
from Shared.Abstract.base_controller import DLBLController
from flask import request, Response, g
from dotenv import load_dotenv
from pymongo import errors
import json
import os

load_dotenv()


class Controller(DLBLController):
    def __init__(self):
        super().__init__()
        try:
            self.client = Client(os.getenv('DB_CLIENT'), os.getenv('DB_CONNECT'))
        except Exception as e:
            print('Erro: ' + str(e))
            try:
                self.client = Client(os.getenv('DB_CLIENT_BACKUP'), os.getenv('DB_CONNECT'))
            except Exception as e:
                print('Erro: ' + str(e))

    # Common routes
    def get_entry(self, collection, entry_id):
        try:
            coll = self.client.db.collection[collection]
            doc = list(coll.find({'ip': entry_id}))
        except Exception as e:
            return Response(str(e), status=404)
        return Response(json.dumps({'doc': doc}), status=201, mimetype='application/json')

    def add_entry(self):
        try:
            request_json = request.get_json()
            collection = request_json['collection']
            query = request_json['query']
            coll = self.client.db.collection[collection]
            coll.insert_one(query)
        except errors.CollectionInvalid as e:
            return Response(str(e), status=404)
        except Exception as e:
            return Response(str(e), status=400)
        return Response('201 Created', status=201)

    def delete_entry(self):
        try:
            request_json = request.get_json()
            collection = request_json['collection']
            query = request_json['query']
            coll = self.client.db.collection[collection]
            coll.delete_many(query)
        except Exception as e:
            return Response(str(e), status=400)
        return Response('200 OK', status=200)

    def update_entry(self):
        try:
            request_json = request.get_json()
            collection = request_json['collection']
            query = request_json['query']
            new_values = request_json['new_values']
            coll = self.client.db.collection[collection]
            coll.update_one(query, new_values)
        except Exception as e:
            return Response(str(e), status=400)
        return Response('Content successfully updated', status=200)
