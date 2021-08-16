import random

from .game_status import GameStatus
from .tiletype import TileType


class GameState:
    def __init__(self, players, adversaries, level, round_num=0, current_player_id=0,
                 level_num=0, status=GameStatus.not_started):
        self.players = players
        self.adversaries = adversaries
        self.level = level
        self.round_num = round_num
        self.currentPlayerId = current_player_id
        self.level_num = level_num
        self.status = status
        self.player_with_key = None

    def add_player(self, player):
        self.players.append(player)

    def get_player(self, id):
        for player in self.players:
            if player.id == id:
                return player

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

    def get_player_at_position(self, position):
        for player in self.players:
            if player.position == position:
                return player

    def get_adversary(self, id):
        for adv in self.adversaries:
            if adv.id == id:
                return adv

    def get_adversary_at_position(self, position):
        for adv in self.adversaries:
            if adv.position == position:
                return adv

    def get_object(self, id):
        for obj in self.level.objects:
            if obj.id == id:
                return obj

    def get_object_by_name(self, name):
        for obj in self.level.objects:
            if obj.name == name:
                return obj

    def get_object_at_position(self, position):
        for obj in self.level.objects:
            if obj.position == position:
                return obj

    def find_placement_location(self):
        candidates = []
        for row in range(self.level.bounds[0]):
            for col in range(self.level.bounds[1]):
                candidates.append((row, col))
        random.shuffle(candidates)
        for c in candidates:
            if self.get_object_at_position(c):
                continue
            if self.get_player_at_position(c):
                continue
            if self.get_adversary_at_position(c):
                continue
            tile = self.level.grid[c[0]][c[1]]
            if tile.type == TileType.room and tile.is_walkable:
                return c
        raise Exception('No valid starting locations')

    def render(self):
        # Get grid of rooms and hallways
        grid = self.level.render()
        # Place objects
        for obj in self.level.objects:
            grid[obj.position[0]][obj.position[1]] = obj.appearance
        # Place adversaries
        for adv in self.adversaries:
            grid[adv.position[0]][adv.position[1]] = adv.appearance
        # Place players
        for player in self.players:
            grid[player.position[0]][player.position[1]] = player.appearance
        return grid

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(str(item)) for item in row]) for row in self.render()])
