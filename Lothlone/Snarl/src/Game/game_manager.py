import copy
import math

from ..Adversary.ghost import Ghost
from ..Adversary.zombie import Zombie
from .adversary import Adversary
from .game_status import GameStatus
from .gamestate import GameState
from .player import Player
from .player_status import PlayerStatus
from .tiletype import TileType
from ..Common.user import User
from . import rule_checker as checker
from .tile import Tile
from .player_update import PlayerUpdate


class GameManager:
    def __init__(self, levels, start_level_num):
        self.users = {}
        self.adversary_controllers = []
        self.observers = {}
        self.levels = levels
        self.gamestate = GameState([], [], levels[start_level_num])

    def register_user(self, user):
        """creates and adds a new player to the gamestate with unique
        id and appearance and starting location, and returns the id of the newly created player"""
        user_id = len(self.users)
        user.set_id(user_id)

        self.users[user_id] = user
        # Add a new Player to the GameState
        start_location = self.gamestate.find_placement_location()
        new_player = Player(user_id, user.get_username(), start_location, user.get_username()[0].upper(), {'movementDistance': 2,
                                                                                'visionDistance': 2})
        self.gamestate.add_player(new_player)
        return user_id

    def register_observer(self, observer):
        observer_id = len(self.observers)
        observer.set_id(observer_id)
        self.observers[observer_id] = observer
        return observer_id

    def initialize_gamestate(self, level_num):
        self.gamestate.level = self.levels[level_num]
        self.gamestate.level_num = level_num
        self.gamestate.player_with_key = None
        self.gamestate.adversaries = []
        for p in self.gamestate.players:
            p.position = None
        for i in range(math.floor((level_num + 1) / 2) + 1):
            self.gamestate.adversaries.append(Adversary(i, 'z' + str(i), 'zombie', self.gamestate.find_placement_location()))
            zombie_controller = Zombie('z' + str(i))
            zombie_controller.set_id(i)
            self.adversary_controllers.append(zombie_controller)
        for j in range(math.floor(level_num - 1 / 2)):
            self.gamestate.adversaries.append(Adversary(i + j, 'g' + str(j), 'ghost', self.gamestate.find_placement_location()))
            ghost_controller = Ghost('g' + str(i))
            ghost_controller.set_id(i+j)
            self.adversary_controllers.append(ghost_controller)
        for p in self.gamestate.players:
            p.position = self.gamestate.find_placement_location()
            p.status = PlayerStatus.isInLevel
        self.start_level()

    def start_level(self):
        for user in self.users.values():
            user.start_level(self.gamestate.level_num, [p.name for p in self.gamestate.players])

    def broadcast(self, message):
        for i in range(len(self.users)):
            u = self.users.get(i)
            u.set_end_result(message)

    def update_observers(self):
        for obs in self.observers.values():
            obs.update_gamestate(self.gamestate)

    def update_users(self):
        for user in self.users.values():
            update = self.create_player_update(self.gamestate, user.id)
            user.player_update(update)

    def start_game(self):
        self.gamestate.status = GameStatus.in_progress
        self.initialize_gamestate(self.gamestate.level_num)
        while self.gamestate.status == GameStatus.in_progress:
            self.update_observers()
            self.update_users()
            self.player_turn(self.gamestate.currentPlayerId)
            self.gamestate.currentPlayerId += 1
            if self.gamestate.currentPlayerId >= len(self.gamestate.players):
                self.gamestate.currentPlayerId = 0
                for i in range(len(self.adversary_controllers)):
                    move = self.adversary_controllers[i].get_move(self.gamestate)
                    self.gamestate.get_adversary(i).move(move)
                    p = self.gamestate.get_player_at_position(move)
                    if p is not None:
                        u = self.users.get(p.id)
                        u.set_response(u.last_move, 'Eject')
                        p.times_ejected += 1
                        p.expel()
                self.gamestate.round_num += 1
            if checker.is_level_over(self.gamestate):
                level_victory = False
                for player in self.gamestate.players:
                    if player.status is PlayerStatus.isExited:
                        level_victory = True
                for user in self.users.values():
                    exits = [p.name for p in self.gamestate.players if p.status == PlayerStatus.isExited]
                    ejects = [p.name for p in self.gamestate.players if p.status == PlayerStatus.isExpelled]
                    user.end_level(self.gamestate.player_with_key, exits, ejects)

            # Check if game is over, exit game
            if checker.is_game_over(self.gamestate, len(self.levels)):
                if checker.is_level_over(self.gamestate):
                    self.gamestate.status = GameStatus.defeat
                else:
                    self.gamestate.status = GameStatus.victory
                break
            elif checker.is_level_over(self.gamestate) and level_victory:
                self.initialize_gamestate(self.gamestate.level_num + 1)

        # After end of game, print messages to users
        if self.gamestate.status == GameStatus.defeat:
            message = "All players have been ejected, lost on level " + str(self.gamestate.level_num + 1) + "\n"
        elif self.gamestate.status == GameStatus.victory:
            message = "You won the game by completing " + str(self.gamestate.level_num + 1) + " levels!\n"
        self.broadcast(message)

        # TODO why?
        if len(self.users):
            # loop through users, print how many times they successfully exited, keys, give them rankings
            # store info in user?
            stats = []
            for i in range(len(self.users)):
                p = self.gamestate.get_player(i)
                stats.append({"type": "player-score", "name": p.name, "exits": p.times_exited,
                              "ejects": p.times_ejected, "keys": p.keys_collected})
            rank_list = sorted(stats, key=lambda x: (x['exits'], x['keys']))
            ranks = "Rankings:\n"
            for j in rank_list:
                ranks += "{}: Times Exited: {}, Keys Collected: {}\n".format(j['name'], j['exits'], j['keys'])
            self.broadcast(ranks)
            for user in self.users.values():
                user.end_game(rank_list)

    def create_player_update(self, gamestate, id):
        
        current_player = gamestate.get_player(id)
        player_row, player_col = current_player.position
        vision_distance = current_player.stats['visionDistance']

        def is_visible(position):
            row, col = position
            return abs(player_row - row) <= vision_distance and abs(player_col - col) <= vision_distance

        # get visible actors
        filtered_actors = []
        for player in gamestate.players:
            if is_visible(player.position):
                filtered_actors.append(player)

        for adversary in gamestate.adversaries:
            if is_visible(adversary.position):
                filtered_actors.append(adversary)

        # get visible objects
        filtered_objects = []
        for obj in gamestate.level.objects:
            if is_visible(obj.position):
                filtered_objects.append(obj)

        # get visible layout (5x5 grid with vision distance of 2)
        filtered_grid = []
        level_grid = gamestate.level.grid
        for r in range(-2, 3):
            new_row = []
            for c in range(-2, 3):
                try:
                    new_row.append(level_grid[player_row + r][player_col + c])
                except IndexError:
                    new_row.append(Tile())
            filtered_grid.append(new_row)

        return PlayerUpdate(filtered_grid, current_player.position, filtered_objects, filtered_actors)

    def player_turn(self, id):
        user = self.users.get(id)
        player = self.gamestate.get_player(id)
        if player.status != PlayerStatus.isInLevel:
            return

        valid_move = False
        while not valid_move:
            player_move = user.get_move()
            # if move returned is empty, player stays put
            if player_move is None:
                requested_position = player.position
            else:
                requested_position = player_move
            # validate move
            valid_move = checker.is_player_move_valid(self.gamestate, id, requested_position)
            if not valid_move:
                user.set_response(requested_position, "Invalid")

        # move player
        player.move(requested_position)
        
        # check if there is an object there
        obj = self.gamestate.get_object_at_position(requested_position)

        # check if there is an adversary there
        if self.gamestate.get_adversary_at_position(requested_position) is not None:
            user.set_response(player_move, 'Eject')
            player.times_ejected += 1
            player.expel()
            # no need to check for object interactions

        # process object interaction
        elif obj is None:
            user.set_response(player_move, 'OK')
        elif obj.name == 'key':
            self.gamestate.level.remove_object(obj.id)
            player.keys_collected += 1
            self.gamestate.player_with_key = player.name
            user.set_response(player_move, 'Key')
        elif obj.name == 'exit' and 'key' not in [obj.name for obj in self.gamestate.level.objects]:
            user.set_response(player_move, 'Exit')
            player.exit()
            player.times_exited += 1
        else:
            user.set_response(player_move, 'OK')

        return
