from .tile import Tile
from .tiletype import TileType


class Room:
    """
    Class to represent a room.

    Parameters:
        origin (tuple): A coordinate [row,col] representing the location of the room in relation to the level
        bounds (tuple): An [row,col] tuple representing the boundaries of the room, relative to the room
        tiles (List): A 2D array (represented by a list of lists) with Tiles indicating which tiles
            within the room are non-walls. Errors if dimension of tiles do not match bounds
        doors (List): A list of [row,col] tuples representing the location of doors in relation to the room.
            Errors if door is not on boundary of room
        neighbors (List): A list of hallways representing all the hallways that the room connects to.
            This field gets populated when initializing the level.
    """

    def __init__(self, origin, bounds, tiles, doors):
        # Verify valid coordinates
        if origin[0] < 0 or origin[1] < 0:
            raise ValueError("Invalid room coordinates: {}".format(origin))
        self.origin = origin
        # Verify valid bounds
        if bounds[0] <= 0 or bounds[1] <= 0:
            raise ValueError("Invalid room bounds: {}".format(bounds))
        self.bounds = bounds

        # Verify that the tiles are of correct size and that doors are on the boundaries
        if len(tiles) == 0 or len(tiles) != bounds[0]:
            raise ValueError("Improper layout of tiles: {}".format(tiles))
        for row in tiles:
            if len(row) == 0 or len(row) != bounds[1]:
                raise ValueError("Improper layout of tiles: {}".format(tiles))
        self.tiles = tiles

        for d in doors:
            row, col = d
            temp_row, temp_col = bounds[0] - 1, bounds[1] - 1
            # if not ((0 <= row <= temp_row and (col == 0 or col == temp_col))
            #         or ((row == 0 or row == temp_row) and 0 <= col <= temp_col)):
            #     raise ValueError("Invalid door position: {}, {}".format(row, col))
        self.doors = doors

        # should there be a difference between tiles that are non-walkable in a room and void tiles that aren't in a
        # room (artifact of the level.grid's empty space)
        for row in tiles:
            for tile in row:
                tile.origin = self.origin
                tile.type = TileType.room

        for d in doors:
            row, col = d
            cur_tile = self.tiles[row][col]
            cur_tile.type = TileType.door
        self.halls_connected = []

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(str(tile)) for tile in row]) for row in self.tiles])
