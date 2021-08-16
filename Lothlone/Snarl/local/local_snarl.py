#!/usr/bin/env python3

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Snarl.src.Observer.local_observer import LocalObserver
from Snarl.src.User.local_user import LocalUser
from Snarl.src.Game.game_manager import GameManager
from Snarl.src import json_utils

# Use argparse to read arguments
parser = argparse.ArgumentParser()

parser.add_argument('--levels', action='store', nargs='?', type=str, default='snarl.levels')
parser.add_argument('--players', action='store', type=int, nargs='?', default=1)
parser.add_argument('--start', action='store', type=int, nargs='?', default=1)
parser.add_argument('--observe', action='store_const', const='observe')

args = vars(parser.parse_args())
levels_filename = args['levels']
num_players = args['players']
start_level_num = args['start'] - 1
should_create_observer = args['observe']

if should_create_observer and num_players != 1:
    raise ValueError('Observer can only be used when there is 1 player')

# Read levels file
with open(levels_filename) as f:
    levels_json = json.load(f)

# Convert jsons into objects
levels = [json_utils.json_to_level(level_json) for level_json in levels_json]

# Create game manager
manager = GameManager(levels, start_level_num)

# Create and register users and observers
users = []
for i in range(num_players):
    print("Enter username: ")
    name = input()
    user = LocalUser(name)
    users.append(user)
    manager.register_user(user)
if should_create_observer:
    observer = LocalObserver()
    manager.register_observer(observer)

manager.start_game()
