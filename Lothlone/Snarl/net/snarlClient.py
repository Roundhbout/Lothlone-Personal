#!/usr/bin/env python3

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Snarl.src.Remote.Client import Client

# Use argparse to read arguments
parser = argparse.ArgumentParser()

parser.add_argument('--address', action='store', nargs='?', type=str, default='127.0.0.1')
parser.add_argument('--port', action='store', type=int, nargs='?', default=45678)

args = vars(parser.parse_args())
host_addr = args['address']
port = args['port']

print("Enter username: ")
name = input()
client = Client(name, host_addr, port)
client.start()
