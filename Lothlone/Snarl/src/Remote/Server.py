import json
import socket

from ..Game.game_manager import GameManager
from ..User.remote_user import RemoteUser
from ..Observer.local_observer import LocalObserver
from .utils import *


class Server:
    def __init__(self, levels, max_num_clients=4, reg_timeout=60, observe=False, host="127.0.0.1", port=45678):
        self.levels = levels
        self.max_num_clients = max_num_clients
        self.reg_timeout = reg_timeout
        self.observe = observe
        self.host_addr = host
        self.port = port
        self.clients = []
        self.gm = GameManager(self.levels, 0)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host_addr, self.port))

    def welcome_and_request_name(self, conn):
        welcome = {"type": "welcome", "info": "Lothlone Server"}
        send_msg(welcome, conn)
        send_msg("name", conn)
        name = recv_msg(conn)
        print("Registering {0}".format(name))
        self.gm.register_user(RemoteUser(name, conn))
    
    def wait_for_players(self, count):
        for i in range(count):
            conn, addr = self.socket.accept()
            print("New connection {0}/{1}: {2}".format(len(self.clients)+1, self.max_num_clients, addr))
            self.clients.append(conn)
            self.welcome_and_request_name(conn)

    def start(self):
        with self.socket as sock:
            sock.listen(self.max_num_clients)

            # accept the minimum number of players to actually play the game (1)
            print("Waiting for first player to join...\n")
            self.wait_for_players(1)

            # wait for more players with a timeout
            print("Waiting for additional players to join...\n")
            sock.settimeout(self.reg_timeout)

            try:
                self.wait_for_players(self.max_num_clients - 1)
            except socket.timeout:
                print("Timeout: ")
                pass
            print("Starting Game with {0} players\n".format(len(self.clients)))
            
            if self.observe:
                observer = LocalObserver()
                self.gm.register_observer(observer)

            self.gm.start_game()
