#!/usr/bin/env python3

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Snarl.src import json_utils
from Snarl.src.Remote.Server import Server

# Use argparse to read arguments
parser = argparse.ArgumentParser()

parser.add_argument('--levels', action='store', nargs='?', type=str, default='snarl.levels')
parser.add_argument('--clients', action='store', type=int, nargs='?', default=4)
parser.add_argument('--wait', action='store', type=int, nargs='?', default=60)
parser.add_argument('--observe', action='store_const', const='observe')
parser.add_argument('--address', action='store', nargs='?', type=str, default='127.0.0.1')
parser.add_argument('--port', action='store', type=int, nargs='?', default=45678)

args = vars(parser.parse_args())
levels_filename = args['levels']
max_num_clients = args['clients']
reg_timeout = args['wait']
should_create_observer = args['observe'] is not None
host_addr = args['address']
port = args['port']

# Read levels file
with open(levels_filename) as f:
    levels_json = json.load(f)

# Convert jsons into objects
levels = [json_utils.json_to_level(level_json) for level_json in levels_json]

server = Server(levels, max_num_clients, reg_timeout, should_create_observer, host_addr, port)
server.start()
