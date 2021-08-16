from .tile import Tile
from .tiletype import TileType


class Level:
    """
    Class to represent a Level in the game. Contains the rooms and hallways of the level, and all the objects in it

    Parameters:
        rooms (list): list of rooms in the level.
        hallways (list): list of hallways in the level.
        objects (list): list of objects in the level. These arent represented in the grid, but get added when rendered
        bounds (tuple): A (row, col) tuple representing the size of the grid
        grid (list): A list of lists of chars (soon to be tiles) indicating the layout of the level. Formed based on the 
            rooms and hallways
    
    Methods:
        add_object(object): add an object to the list of objects
        remove_object(object): remove an object from the list of objects
        get_neighbors(grid, coord, cardinal): not a part of the class, but it's helpful. Returns all
            neighboring coordinates of coord in grid. Returns only cardinal neighbors if cardinal is True.
    """

    def __init__(self, rooms, hallways, objects):
        # Given lists of rooms and hallways, returns the dimensions of the smallest rectangular grid needed to
        # represent them
        def get_boundaries(rooms, hallways):
            eastmost = 0
            southmost = 0
            for room in rooms:
                origin = room.origin
                bounds = room.bounds
                east = origin[1] + bounds[1]
                south = origin[0] + bounds[0]
                if east > eastmost:
                    eastmost = east
                if south > southmost:
                    southmost = south

            for hall in hallways:
                for point in hall.all_points:
                    east = point[1]
                    south = point[0]
                    if east > eastmost:
                        eastmost = east
                    if south > southmost:
                        southmost = south

            return southmost, eastmost

        # Initialize a grid with rooms and hallways
        def generate_grid(rooms, hallways, bounds):
            southmost, eastmost = bounds
            # Initialize a blank grid with the bounds
            grid = [[Tile() for i in range(eastmost)] for j in range(southmost)]

            # Generate rooms
            for room in rooms:
                top_left = room.origin
                top_left_row, top_left_col = top_left
                for row, r in enumerate(room.tiles):
                    for col, tile in enumerate(r):
                        # Have to increment these values by 1 to account for the grid buffer
                        new_row = row + top_left_row
                        new_col = col + top_left_col
                        # Make sure the room we're placing doesn't overlap any already placed rooms
                        if grid[new_row][new_col].type != TileType.void:
                            raise ValueError(
                                "Current room overlaps with another room: {}".format(grid[new_row][new_col].type))
                        grid[new_row][new_col] = tile

            # Generate hallways
            for hall in hallways:
                if (grid[hall.start[0]][hall.start[1]].type != TileType.door or
                        grid[hall.end[0]][hall.end[1]].type != TileType.door):
                    raise ValueError(
                        "Hallway doesn't connect to a door: {}".format(grid[hall.end[0]][hall.end[1]].type))

                for point in hall.all_points:
                    point_row, point_col = point
                    if grid[point_row][point_col].type != TileType.void:
                        raise ValueError("Current hallway overlaps with something at ({}, {})".format(
                            point_row, point_col))
                    grid[point_row][point_col] = Tile(True, TileType.hallway, hall.start)

            """
            # Generates walls on any non-floor/door tile
            for row, r in enumerate(grid):
                for col in range(len(r)):
                    if grid[row][col].type == tile_type.void:
                        # Uncomment the line below if we only want walls to be ones surrounding floor tiles
                        if "." in getNeighbors(grid, (row, col), False):
                            grid[row][col] = "█"
            """
            return grid

        self.rooms = rooms
        self.hallways = hallways
        self.objects = objects
        self.bounds = get_boundaries(rooms, hallways)
        self.grid = generate_grid(rooms, hallways, self.bounds)

        # Fill halls_connected field for all rooms.
        for hall in hallways:
            hall.start_room.halls_connected.append(hall)
            hall.end_room.halls_connected.append(hall)

    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, objectId):
        self.objects = [obj for obj in self.objects if obj.id != objectId]

    def render(self):
        return [['{:4}'.format(str(item)) for item in row] for row in self.grid]

    # Prints the level in a nicely formatted string
    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(str(item)) for item in row]) for row in self.grid])


# returns the coordinates of the neighbors of coord within grid, 
def get_neighbors(grid, coord, cardinal):
    row, col = coord
    
    lists = [[[r, c] 
            for r in range(max(row - 1, 0), min(row + 2, len(grid)))]
                for c in range(max(col - 1, 0), min(col + 2, len(grid[0])))]
    all_neighbors = sum(lists, [])

    # Cardinal neighbors have odd indices in the list, so we can keep only those if needed
    if cardinal:
        all_neighbors = [all_neighbors[i] for i in range(len(all_neighbors)) if i % 2 != 0]
    return [tuple(neighbor) for neighbor in all_neighbors]
