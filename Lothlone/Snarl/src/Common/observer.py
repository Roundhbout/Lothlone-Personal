from abc import ABC, abstractmethod


class Observer(ABC):
    def __init__(self):
        # game_manager.register_user(username)
        self.id = None
        self.gamestate = None

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def set_id(self, id):
        pass

    @abstractmethod
    def update_gamestate(self, gamestate):
        pass
