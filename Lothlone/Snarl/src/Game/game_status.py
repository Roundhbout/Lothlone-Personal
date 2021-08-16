import enum


class GameStatus(enum.Enum):
    not_started = 0
    in_progress = 1
    defeat = 2
    victory = 3
