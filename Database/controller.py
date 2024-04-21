from Database.client import Client
from Shared.Abstract import DLBLLinker
from flask import request, Response
from dotenv import load_dotenv
from pymongo import errors
from bson import ObjectId
import json
import os

load_dotenv()


class Controller(DLBLLinker):
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
    def get_entry(self, coll, entry_id):
        try:
            doc = list(self.client.db[coll].find({'_id': ObjectId(entry_id)}))
        except Exception as e:
            return Response(str(e), status=404)
        if doc:
            return Response(json.dumps({'doc': str(doc)}), status=201, mimetype='application/json')
        return Response('Content not found', status=404)

    def get_all_entries(self, coll):
        try:
            doc = list(self.client.db[coll].find({}))
        except Exception as e:
            return Response(str(e), status=404)
        return Response(json.dumps({'doc': str(doc)}), status=201, mimetype='application/json')

    def add_entry(self):
        try:
            request_json = request.get_json()
            coll = request_json['coll']
            query = request_json['query']
            doc_id = self.client.db[coll].insert_one(query).inserted_id
        except errors.CollectionInvalid as e:
            return Response(str(e), status=404)
        except Exception as e:
            return Response(str(e), status=400)
        return Response(str(doc_id), status=201)

    def update_entry(self):
        try:
            request_json = request.get_json()
            coll = request_json['coll']
            entry_id = request_json['entry_id']
            new_values = request_json['new_values']
            updated = self.client.db[coll].update_one({'_id': ObjectId(entry_id)}, new_values)
        except Exception as e:
            return Response(str(e), status=400)
        if updated.modified_count:
            return Response('Content successfully updated', status=200)
        return Response('Content not found', status=404)

    def delete_entry(self, coll, entry_id):
        try:
            deleted = self.client.db[coll].delete_one({'_id': ObjectId(entry_id)})
        except Exception as e:
            return Response(str(e), status=400)
        if deleted.deleted_count:
            return Response('Content successfully deleted', status=200)
        return Response('Content not found', status=404)
