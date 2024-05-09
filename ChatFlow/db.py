from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import gridfs
import sys
import os


load_dotenv()


try:
    client = MongoClient(os.getenv('DB_CLIENT'), server_api=ServerApi('1'))
    client.admin.command('ping')
except Exception as e:
    print('Connection to database failed: ' + str(e))
    print('Shutting down server...')
    sys.exit(1)
print('Pinged your deployment. You successfully connected to MongoDB!')
db_cli = client[os.getenv('DB_CONNECT')]
fs = gridfs.GridFS(db_cli)
