from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DB:
    def __init__(self, uri, db):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db]

        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
