from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, username):
        # game_manager.register_user(username)
        self.id = None
        self.username = username
        self.update = None
        self.last_move = None
        self.result = None

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def set_id(self, id):
        pass

    @abstractmethod
    def player_update(self, update):
        pass

    @abstractmethod
    def set_response(self, move, result):
        pass

    @abstractmethod
    def start_level(self, level_num, player_list):
        pass 
    
    @abstractmethod
    def end_level(self, key, exits, ejects):
        pass
    
    @abstractmethod
    def end_game(self, score_list):
        pass

    @abstractmethod
    def set_end_result(self, message):
        pass
