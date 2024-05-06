from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()


class DBClient:
    def __init__(self, uri, db):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db]

        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")


db_cli = DBClient(os.getenv('DB_CLIENT'), os.getenv('DB_CONNECT'))
# db_cli = DBClient(os.getenv('DB_CLIENT_BACKUP'), os.getenv('DB_CONNECT'))
