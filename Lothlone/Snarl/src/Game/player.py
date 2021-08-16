from .player_status import PlayerStatus


class Player:
    def __init__(self, id, name, position, appearance, stats):
        self.id = id
        self.name = name
        self.position = position
        self.appearance = appearance
        self.status = PlayerStatus.isInLevel
        self.stats = stats
        self.keys_collected = 0
        self.times_exited = 0
        self.times_ejected = 0

    def move(self, position):
        self.position = position

    def exit(self):
        self.status = PlayerStatus.isExited

    def expel(self):
        self.status = PlayerStatus.isExpelled
