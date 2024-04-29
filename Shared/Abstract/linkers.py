from abc import ABC, abstractmethod


class DLBLLinker(ABC):
    def __init__(self):
        pass

    # User methods
    @abstractmethod
    def get_entry(self, coll, identifier, entry_id):
        pass

    @abstractmethod
    def get_all_entries(self, coll):
        pass

    @abstractmethod
    def add_entry(self):
        pass

    @abstractmethod
    def update_entry(self):
        pass

    @abstractmethod
    def delete_entry(self, coll, entry_id):
        pass


class CLBLLinker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_user(self, user_id, email):
        pass

    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass

    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def token(self):
        pass
