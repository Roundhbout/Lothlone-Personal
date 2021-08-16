#!/usr/bin/env python3
import sys
import json
import os
from io import StringIO
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Snarl.src.User.local_user import LocalUser
from Snarl.src.json_utils import *

input = json.loads(''.join(sys.stdin.readlines()))

name_list = input[0]
json_level = input[1]
max_num_turns = input[2]
starting_positions = input[3]
player_moves = input[4]

player_starting_positions = starting_positions[:len(name_list)]
adversary_starting_positions = starting_positions[len(name_list):]

level = json_to_level(json_level)
gamestate = GameState([], [], level)
manager = GameManager(gamestate)

# create users with simulated input
for idx in range(len(name_list)):
    username = name_list[idx]
    moves = player_moves[idx]
    user_input = ''
    for move in moves:
        point = move['to']
        if point is not None:
            user_input += str(point[0]) + ', ' + str(point[1])
        user_input += '\n'
    user = LocalUser(username, StringIO(user_input), StringIO())
    user_id = manager.register_user(user)
    # place player at appropriate starting location
    gamestate.get_player(user_id).move(starting_positions[idx])

# add adversaries
for i, start_pos in enumerate(adversary_starting_positions):
    adv = Adversary(i, 'ghost' + str(i + 1), 'ghost', tuple(start_pos))
    gamestate.adversaries.append(adv)

# maintain a list of active users from which we will generate our manager-trace
active_users = copy.copy(manager.users)

manager_trace = []


def record_update(user):
    player = gamestate.get_player(user.get_id())
    update = gamestate_to_player_update_json(user.gamestate, player)
    manager_trace.append([player.name, update])


# update users with gamestate
for user in active_users.values():
    user.update_gamestate(manager.filter_game_state(gamestate, user.id))
    record_update(user)

# TODO fix logic so we only iterate over players still in game
for turn in range(max_num_turns):
    id = 0
    while id < len(gamestate.players):
        player = gamestate.get_player(id)
        if player.status is PlayerStatus.isInLevel:
            manager.player_turn(id)
            user = manager.users.get(id)
            manager_trace.append([player.name, {"to": user.last_move, "type": "move"}, user.result])
            if user.result is "Eject":
                del active_users[id]
            if user.result is not "Invalid":
                # update state for all users
                for i in range(len(active_users)):
                    active_users.get(i).gamestate = manager.filter_game_state(gamestate, i)
                    record_update(active_users.get(i))
                id += 1


# convert final game state, return it with manager trace
gamestate_json = gamestate_to_json(gamestate)
output = [gamestate_json, manager_trace]
print(json.dumps(output, indent=2, sort_keys=False))
