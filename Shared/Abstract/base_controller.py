from abc import ABC, abstractmethod


class DLBLController(ABC):
    def __init__(self):
        pass

    # User methods
    @abstractmethod
    def get_entry(self, collection, entry_id):
        pass

    @abstractmethod
    def add_entry(self):
        pass

    @abstractmethod
    def update_entry(self):
        pass

    @abstractmethod
    def delete_entry(self):
        pass


class CLBLController(ABC):
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
    def token(self):
        pass
