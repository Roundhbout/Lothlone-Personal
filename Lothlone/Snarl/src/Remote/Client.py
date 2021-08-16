import socket
from .utils import *
from ..json_utils import *
from ..User.local_user import LocalUser

class Client:
    def __init__(self, username, host_addr="127.0.0.1", port=45678):
        self.username = username
        self.addr = host_addr
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.players = []

    def start(self):
        self.socket.connect((self.addr, self.port))
        welcome = recv_msg(self.socket)
        print("Welcome! {}".format(welcome['info']))
        name = recv_msg(self.socket)
        if name == "name":
            send_msg(self.username, self.socket)
        user = LocalUser(self.username)
        while True:
            msg = recv_msg(self.socket)
            #print("Received message: " + str(msg))

            # move request
            if msg == "move":
                move = user.get_move()
                movedict = {"type" : "move", "to" : move}
                send_msg(movedict, self.socket)
                continue
            elif msg == 'OK' or msg == 'Key' or msg == 'Exit' or msg == 'Eject' or msg == 'Invalid':
                # result from a move
                user.set_response(move, msg)
                continue

            type = msg['type']

            if type == 'start-level':
                self.players = msg["players"]
                user.start_level(msg["level"], msg["players"])

            # game update
            elif type == 'player-update':
                update = player_update_json_to_player_update(msg, self.username)
                user.player_update(update)

            # end of level update
            elif type == 'end-level':
                
                user.end_level(msg["key"], msg["exits"], msg["ejects"])

            # end of game update
            elif type == 'end-game':
                
                user.end_game(msg["scores"])
                break
