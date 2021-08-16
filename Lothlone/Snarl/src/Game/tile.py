from .tiletype import TileType 

class Tile:
    """
    Class to represent an individual tile in a room/hallway/grid. This
    should allow us to better standardize the appearance and type of tile 
    (door, walkable, non-walkable, etc.) and help us get more information 
    about a position relative to the level (ex. which room someone on this tile is in).
    The default tile (calling Tile() without any arguments creates a void tile)

    Fields:
        type (enum): A tile_type enum representing what type of tile this is
        walkable (boolean): True if a player/adv can walk on this tile
        origin (tuple): An optional (row, col) tuple indicating the origin of the 
            room/hallway the tile is a part of. This should be room.origin if
            a room tile (walkable or door), hallway.start if a hallway tile, 
            and None if the tile is non-walkable/void.

    Methods:
        __str__(): Returns the appearance of the tile
    """
    
    def __init__(self, walkable=False, type=TileType.void, origin=None):

        self.type = type
        self.is_walkable = walkable
        self.origin = origin
    
    # get the ASCII appearance of the tile based on it's type and whether it's walkable
    def __str__(self):
        if self.is_walkable:
            if self.type == TileType.door:
                return "|"
            else:
                return "."
        else:
            return " "

