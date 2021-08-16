import sys
import os
import copy

"""
since most input jsons for testing are of a different form
from how we represent objects, we have to translate them.
instead of copying code for each testfile, we decided to
compile translations into one file so each test file can
focus more on the actual test being done.
"""

from .Game.room import Room
from .Game.hallway import Hallway
from .Game.object import Object
from .Game.level import Level
from .Game.gamestate import GameState
from .Game.player import Player
from .Game.adversary import Adversary
from .Game.game_status import GameStatus
from .Game.tile import Tile
from .Game.tiletype import TileType
from .Game.player_status import PlayerStatus
from .Game.game_manager import GameManager
from .Game.player_update import PlayerUpdate

def json_to_layout(layout_json):
    # go through every tile in the layout
    layout = []
    for row, r in enumerate(layout_json):
        new_row = []
        for col, val in enumerate(r):
            if val == 0:
                new_row.append(Tile())
            elif val == 2:
                new_row.append(Tile(True, TileType.door))
            else:
                new_row.append(Tile(True, TileType.room))
        layout.append(new_row)
    return layout


def json_to_room(room_json):
    # Make sure request is for room
    if room_json["type"] != "room":
        raise ValueError("Not a room input")

    # Origin is in a data type we can pass to room so just get it
    origin = room_json["origin"]

    # get the rows and columns field and make it into a tuple-like data type
    bounds = room_json["bounds"]
    bounds = bounds["rows"], bounds["columns"]

    # layout is different from our room structure so we need to translate it
    layout = room_json["layout"]
    # this list will store coordinates of the doors in the room
    doors = []

    # go through every tile in the layout
    for row, r in enumerate(layout):
        for col, val in enumerate(r):
            # if the tile is a wall, just make it blank
            if val == 0:
                layout[row][col] = Tile()
            # otherwise this is a walkable tile
            else:
                # if the tile is a door tile then we'll want to store it's coordinates
                if val == 2:
                    doors.append([row, col])
                # make the walkable tile the correct indicator
                # (door tiles will be made back into doors by the room initialization)
                layout[row][col] = Tile(True, TileType.room, origin)

    return Room(origin, bounds, layout, doors)


def json_to_objects(objects_json):
    return [Object(idx, obj["type"], tuple(obj["position"]), obj["type"][0].lower()) for idx, obj in enumerate(objects_json)]


def json_to_hallway(hallway_json, room_list):
    start = tuple(hallway_json["from"])
    end = tuple(hallway_json["to"])

    waypoints = [tuple(p) for p in hallway_json["waypoints"]]

    for room in room_list:
        for door in room.doors:
            if start[0] == door[0] + room.origin[0] and start[1] == door[1] + room.origin[1]:
                start_room = room
            if end[0] == door[0] + room.origin[0] and end[1] == door[1] + room.origin[1]:
                end_room = room

    if start_room is None or end_room is None:
        raise ValueError("Hallway doesn't align with any rooms")

    return Hallway(start, end, waypoints, start_room, end_room)


def json_to_adversaries(adversary_json):
    adversaries = []
    for idx, adv in enumerate(adversary_json):
        if adv["type"] == "zombie":
            adversaries.append(Adversary(idx, adv['name'], 'zombie', tuple(adv["position"]), {"moveSpeed": 1}))
        elif adv["type"] == "ghost":
            adversaries.append(Adversary(idx, adv['name'], 'ghost', tuple(adv["position"]), {"moveSpeed": 1}))
    return adversaries


def json_to_players(player_json):
    players = []
    for idx, p in enumerate(player_json):
        if p["type"] == "player":
            players.append(Player(idx, p["name"], tuple(p["position"]), str(idx), {"movementDistance": 2, "viewDistance": 2}))
    return players


def json_to_level(level_json):
    if level_json["type"] != "level":
        raise ValueError("Not a level JSON: {}".format(level_json["type"]))

    # ------------room translation------------
    rooms = [json_to_room(r) for r in level_json["rooms"]]

    # ------------hallway translation------------
    hallways = [json_to_hallway(h, rooms) for h in level_json["hallways"]]

    # ------------object creation/translation------------
    objects = json_to_objects(level_json["objects"])

    # ------------level creation------------
    return Level(rooms, hallways, objects)


def json_to_gamestate(state_json, round_num=0, current_player_id=0, level_num=0, status=GameStatus.not_started):
    if state_json["type"] != "state":
        raise ValueError("JSON is not of type \"state\", is of type: {}".format(state_json["type"]))

    players = json_to_players(state_json["players"])
    level = json_to_level(state_json["level"])
    adversaries = json_to_adversaries(state_json["adversaries"])

    # newLevelState = translate_level_state(state_json["level"], state_json["adversaries"])
    return GameState(players, adversaries, level, round_num, current_player_id, level_num, status)

# player update object
def player_update_json_to_player_update(update_json, player_name):

    layoutjson = update_json["layout"]
    positionjson = update_json["position"]
    objectsjson = update_json["objects"]
    actorsjson = update_json["actors"]
    message = update_json["message"]

    layout = json_to_layout(layoutjson)

    position = tuple(positionjson)

    objects = json_to_objects(objectsjson)

    playersjson = []
    adversariesjson =[]
    for actorjson in actorsjson:
        if actorjson["type"] == "player":
            playersjson.append(actorjson)
        else:
            adversariesjson.append(actorjson)
    
    actors = json_to_players(playersjson) + json_to_adversaries(adversariesjson)

    return PlayerUpdate(layout, position, objects, actors, message)


# --------------------------------------------------------------------------------------------------

def layout_to_json(tiles):
    json_layout = []
    for row in tiles:
        json_row = []
        for tile in row:
            if not tile.is_walkable:
                json_row.append(0)
            elif tile.type == TileType.door:
                json_row.append(2)
            else:
                json_row.append(1)
        json_layout.append(json_row)
    return json_layout


def room_to_json(room):
    room_json = {"type": "room", "origin": room.origin, "bounds": {}}
    row, col = room.bounds
    room_json["bounds"]["rows"] = row
    room_json["bounds"]["columns"] = col
    
    room_json["layout"] = layout_to_json(room.tiles)
    return room_json


def hallway_to_json(hallway):
    return {"type": "hallway", "from": hallway.start, "to": hallway.end, "waypoints": hallway.waypoints}


def object_to_json(object):
    return {"type": object.name, "position": object.position}


def adversary_to_json(adv):
    return {"name": adv.name, "type": adv.type, "position": adv.position}


def player_to_json(player):
    return {"name": player.name, "type": "player", "position": player.position}


def level_to_json(level):
    rooms = [room_to_json(room) for room in level.rooms]
    hallways = [hallway_to_json(hallway) for hallway in level.hallways]
    objects = [object_to_json(obj) for obj in level.objects]
    
    return {"type": "level", "rooms": rooms, "hallways": hallways, "objects": objects}


def gamestate_to_json(gamestate):
    is_exit_locked = "key" in [obj.name for obj in gamestate.level.objects]
    players = [player_to_json(player) for player in gamestate.players if player.status is not PlayerStatus.isExpelled]
    adversaries = [adversary_to_json(adv) for adv in gamestate.adversaries]
    level = level_to_json(gamestate.level)
    return {"type": "state", "exit-locked": is_exit_locked,
            "players": players, "adversaries": adversaries, "level": level}


"""
Since our game_manager filters grids by returning the whole grid and voiding out
tiles that wouldn't be visible to the player, this returns a grid of that 5x5 
visible grid that a player would see
"""
def truncate_grid(level, position):
    pos_row, pos_col = position
    bound_row, bound_col = level.bounds
    truncated_grid = []
    for row in range(pos_row - 2, pos_row + 3):
        truncated_row = []
        for col in range(pos_col - 2, pos_col + 3):
            if col < 0 or col > bound_col - 1 or row < 0 or row > bound_row - 1:
                truncated_row.append(Tile())
            else:
                truncated_row.append(level.grid[row][col])
        truncated_grid.append(truncated_row)

    return truncated_grid


# player update object
def player_update_to_json(player_update, player_name):

    layout = layout_to_json(player_update.layout)

    position = player_update.position

    objects = [object_to_json(obj) for obj in player_update.objects]

    players = []
    adversaries = []
    for actor in player_update.actors:
        if type(actor) == Player:
            players.append(actor)
        else:
            adversaries.append(actor)

    player_positions = [player_to_json(p) for p in players if p.name != player_name]

    adv_positions = [adversary_to_json(a) for a in adversaries]

    actor_positions = player_positions + adv_positions

    message = player_update.message

    return {"type": "player-update", "layout": layout, "position": position, 
            "objects": objects, "actors": actor_positions, "message": message}


def gamestate_to_start_level(gamestate):

    level_num = gamestate.level_num
    player_names = [p.name for p in gamestate.players]
    start_level = {"type": "start-level", "level": level_num, "players": player_names}
    return start_level
