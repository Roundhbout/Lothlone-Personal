#!/usr/bin/env python3

import sys
import json
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import Snarl.src.json_utils

input = json.loads(''.join(sys.stdin.readlines()))

input_level = input[0]
point = input[1]

point_row, point_col = point

newLevel = json_utils.json_to_level(input_level)

# ------------output testing------------

test_traversable = False
test_object = None
test_type = "void"

test_reachable = []

grid_point = newLevel.grid[point_row][point_col]

# check if point is traversable
if grid_point != " ":
    test_traversable = True

# check if point is on a tile that contains an object
for obj in newLevel.objects:
    if obj.position == point:
        test_object = obj.name
        break

# check if point is in a hallway or room, and get reachable rooms (if applicable)

for hall in newLevel.hallways:
    if tuple(point) in hall.all_points:
        test_type = "hallway"
        type_point = hall.start
        test_reachable.append(hall.start_room.origin)
        test_reachable.append(hall.end_room.origin)
        break

if test_type != "hallway":
    for room in newLevel.rooms:
        # get the origin and bounds(size) of the room
        room_origin = room.origin
        origin_row, origin_col = room_origin
        room_bounds = room.bounds
        bound_row, bound_col = room_bounds
        # need to scale room bounds by origin since size is relative to room, not level
        bound_row += origin_row
        bound_col += origin_col

        # if the point is within the bounds of the room
        if origin_col <= point_col <= bound_col and origin_row <= point_row <= bound_row:
            test_type = "room"
            for h in room.halls_connected:
                test_reachable.append(h.get_connecting_room(room).origin)

# ------------output json------------
output = {}

output["traversable"] = test_traversable
output["object"] = test_object
output["type"] = test_type
output["reachable"] = test_reachable

print(json.dumps(output))
