#!/usr/bin/env python3

import sys
import json
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Snarl.src.Game.level import get_neighbors
import Snarl.src.json_utils

input = json.load(sys.stdin)

input_room = input[0]
point = input[1]

point_row, point_col = point

newRoom = json_utils.json_to_room(input_room)


result = []
if newRoom.tiles[point_row - newRoom.origin[0]][point_col - newRoom.origin[1]] != " ":
    # Account for the grid shift if origin is not (0,0)
    traversables = []
    neighbors = get_neighbors(newRoom.tiles, [point_row - newRoom.origin[0], point_col - newRoom.origin[1]], True)
    for n in neighbors:
        temp_row, temp_col = n
        if newRoom.tiles[temp_row][temp_col] != " ":
            traversables.append([temp_row + newRoom.origin[0], temp_col + newRoom.origin[1]])

    result.append("Success: Traversable points from ")
    result.append(point)
    result.append(" in room at ")
    result.append(newRoom.origin)
    result.append(" are ")
    result.append(traversables)

# Not in room
else:
    result.append("Failure: Point ")
    result.append(point)
    result.append(" is not in room at ")
    result.append(newRoom.origin)
    
print(json.dumps(result))
