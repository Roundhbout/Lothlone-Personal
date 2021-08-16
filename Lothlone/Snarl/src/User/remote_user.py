from ..Common.user import User
from ..json_utils import *
from ..Remote.utils import *


class RemoteUser(User):
    def __init__(self, username, conn):
        super().__init__(username)
        self.conn = conn

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_move(self):
        msg = "move"
        send_msg(msg, self.conn)
        msg = recv_msg(self.conn)
        move = msg['to']
        if move is not None:
            move = tuple(move)
        return move

    def set_id(self, id):
        self.id = id

    def player_update(self, update):
        msg = player_update_to_json(update, self.username)
        send_msg(msg, self.conn)

    def set_response(self, move, result):
        msg = result
        send_msg(msg, self.conn)

    def start_level(self, level_num, player_list):
        msg = {"type": "start-level", "level": level_num, "players": player_list}
        send_msg(msg, self.conn)
        
    def end_level(self, key, exits, ejects):
        msg = {"type": "end-level", "key": key, "exits": exits, "ejects": ejects}
        send_msg(msg, self.conn)

    def end_game(self, score_list):
        msg = {"type": "end-game", "scores": score_list}
        send_msg(msg, self.conn)

    def set_end_result(self, message):
        pass
