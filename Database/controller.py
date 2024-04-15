from Database.db import DB
from dotenv import load_dotenv
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
    def get_entry(self, collection, identifier, entry_id):
        pass

    def add_entry(self, collection, entry):
        pass

    def delete_entry(self, collection, identifier, entry_id):
        pass

    def update_entry(self, collection, identifier, entry_id, field, new_value):
        pass

    # Auth routes
