import enum


class TileType(enum.Enum):
    """
    Enum to represent the type of tile a tile is
    """
    void = 0
    room = 1
    door = 2
    hallway = 3
