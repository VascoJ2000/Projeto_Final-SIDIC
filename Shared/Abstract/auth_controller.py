from abc import ABC, abstractmethod


class AuthController(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def token(self):
        pass
