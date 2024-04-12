from abc import ABC, abstractmethod


class BaseController(ABC):
    def __init__(self):
        pass

    # User methods
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
