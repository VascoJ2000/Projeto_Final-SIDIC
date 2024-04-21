from Shared.Abstract import DLBLLinker, CLBLLinker
from Shared import Client


class Controller(DLBLLinker, CLBLLinker):
    def __init__(self):
        super().__init__()
        self.cli = Client()

    # Business Layer to Data Layer methods
    def get_entry(self, coll, entry_id):
        pass

    def get_all_entries(self, coll):
        pass

    def add_entry(self, data=None):
        pass

    def update_entry(self, coll=None, entry_id=None, new_data=None):
        pass

    def delete_entry(self, coll, entry_id):
        pass

    # User Layer to Business Layer methods
    def get_user(self, user_id, email):
        pass

    def add_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def login(self, email, password):
        pass

    def token(self):
        pass