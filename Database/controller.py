from Database.client import Client
from Shared.Abstract import DLBLLinker
from flask import request, Response
from dotenv import load_dotenv
from pymongo import errors
from bson import ObjectId
from bson.json_util import dumps
import os

load_dotenv()


# Data Layer Controller
# Responsible for handling requests from the Business Layer
class Controller(DLBLLinker):
    def __init__(self):
        super().__init__()
        try:
            # Tries to connect to main database
            self.client = Client(os.getenv('DB_CLIENT'), os.getenv('DB_CONNECT'))
        except Exception as e:
            print('Error: ' + str(e))
            try:
                # If connection to main database is not possible, tries to connect to secondary database
                self.client = Client(os.getenv('DB_CLIENT_BACKUP'), os.getenv('DB_CONNECT'))
            except Exception as e:
                # If both databases are down it just closes down
                print('Error: ' + str(e))
                exit()

    # Tries to find and if found returns a single entry in the requested collection with the specified id
    def get_entry(self, coll, identifier, entry_id):
        try:
            if identifier == '_id':
                # If the id is the actual id of the document it needs to be converted into a ObjectId Object
                entry_id = ObjectId(entry_id)
            doc = self.client.db[coll].find({identifier: entry_id})
            doc_json = dumps(doc)
        except Exception as e:
            return Response(str(e), status=404)
        if doc:
            return Response(doc_json, status=200, mimetype='application/json')
        return Response('Content not found', status=404)

    # Returns all documents in a single collection
    def get_all_entries(self, coll):
        try:
            doc = self.client.db[coll].find({})
            doc_json = dumps(doc)
        except Exception as e:
            return Response(str(e), status=404)
        return Response(doc_json, status=200, mimetype='application/json')

    # Creates a new document in the specified collection
    # Request needs a json string with "coll" and "query" names to fulfill the request
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
        return Response('Entry successfully added', status=201)

    # Updates an existing document
    # If document does not exist it returns status 404
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
            return Response('Content successfully updated', status=202)
        return Response('Content not found', status=404)

    # Deletes an exiting document
    # Like update_entry if the document does not exist it returns status 404
    def delete_entry(self, coll, entry_id):
        try:
            deleted = self.client.db[coll].delete_one({'_id': ObjectId(entry_id)})
        except Exception as e:
            return Response(str(e), status=400)
        if deleted.deleted_count:
            return Response('Content successfully deleted', status=204)
        return Response('Content not found', status=404)
