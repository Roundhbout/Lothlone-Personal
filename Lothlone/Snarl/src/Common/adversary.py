from abc import ABC, abstractmethod


class Adversary(ABC):
    def __init__(self, username):
        self.id = None
        self.username = username
        self.gamestate = None
        self.last_move = None
        self.result = None

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_move(self, gamestate):
        pass

    @abstractmethod
    def set_id(self, id):
        pass

    @abstractmethod
    def update_gamestate(self, gamestate):
        pass

    @abstractmethod
    def set_response(self, move, result):
        pass