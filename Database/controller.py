from Shared.Abstract.auth_controller import AuthController
from Shared.Abstract.base_controller import BaseController
from Database.db import DB
from dotenv import load_dotenv
import os

load_dotenv()


class Controller(AuthController, BaseController):
    def __init__(self):
        super().__init__()
        try:
            self.db = DB(os.getenv('DB_CLIENT'), os.getenv('DB_CONNECT'))
        except Exception as e:
            print('Erro: ' + str(e))
            try:
                self.db = DB(os.getenv('DB_CLIENT_BACKUP'), os.getenv('DB_CONNECT'))
            except Exception as e:
                print('Erro: ' + str(e))

    # Authentication methods
    def login(self, email, password):
        pass

    def token(self):
        pass

    # User methods
    def get_user(self, user_id, email):
        pass

    def add_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass