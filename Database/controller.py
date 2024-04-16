from Database.db import DB
from Shared.middleware import auth
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
    @auth(os.getenv('SECRET_KEY_SD'))
    def get_entry(self, collection, identifier, entry_id):
        pass

    @auth(os.getenv('SECRET_KEY_SD'))
    def add_entry(self, collection, entry):
        pass

    @auth(os.getenv('SECRET_KEY_SD'))
    def delete_entry(self, collection, identifier, entry_id):
        pass

    @auth(os.getenv('SECRET_KEY_SD'))
    def update_entry(self, collection, identifier, entry_id, field, new_value):
        pass

    # Auth routes
    @auth(os.getenv('SECRET_KEY_SD_REFRESH'))
    def create_access_token(self):
        pass

    @auth(os.getenv('SECRET_KEY_SD_REFRESH'))
    def create_refresh_token(self):
        pass
