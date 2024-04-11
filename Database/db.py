from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DB:
    def __init__(self, uri, db):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db]

        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

    def get_entry(self, identifier, entry_id, collection):
        pass

    def add_entry(self, collection, entry):
        pass

    def delete_entry(self, identifier, entry_id, collection):
        pass

    def update_entry(self, identifier, entry_id, collection, field, new_value):
        pass
