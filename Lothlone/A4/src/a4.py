#!/usr/bin/env python3

import argparse
import json
import socket
import sys

# ----------------------------Startup Phase----------------------------------------------
# Use argparse to read arguments
parser = argparse.ArgumentParser(description='Read in an IP address, a port, and a username. Defaults are as follows: '
                                             '\n IP: 127.0.0.1 (localhost)\n Port: 8000\n Username: Glorifrir '
                                             'Flintshoulder')

parser.add_argument('address', action='store', nargs='?', type=str, default='127.0.0.1')
parser.add_argument('Port', action='store', type=int, nargs='?', default=8000)
parser.add_argument('User', action='store', type=str, nargs='?', default='Glorifrir Flintshoulder')

args = vars(parser.parse_args())

addr = args['address']
port = args['Port']
user = args['User']


def printInvalidRequest(jsonObj):
    print(json.dumps({'error': 'not a request', 'object': jsonObj}))


# Create socket to communicate with server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # connect to server using IP an port arguments
    sock.connect((addr, port))

    # send username to server
    sock.sendall(user.encode())

    # get session ID from server
    sessionID = ''
    while True:
        d = sock.recv(1024)
        sessionID += d.decode()
        if not d or '\n' in sessionID:
            break

    print(json.dumps(['the server will call me', user]))

    # User inputs a create request (road network creation), shutdown if input is invalid, continue if input is valid
    print('Enter/Paste road network now. Ctrl-D to input it.')

    # Try to parse json and verify that it is a valid create request, create towns list and send
    try:
        createReq = json.loads(input())
        cmd = createReq['command']
        towns = []
        roads = createReq['params']
        # check if input command is 'roads'
        if cmd != 'roads':
            raise Exception()
        # input command is roads, create list of towns
        else:
            for r in roads:
                if r['from'] not in towns:
                    towns.append(r['from'])
                if r['to'] not in towns:
                    towns.append(r['to'])

        # assemble json to be sent to server
        goodJson = {'towns': towns, 'roads': roads}
        goodJson = json.dumps(goodJson)

        # send roads request
        sock.sendall(goodJson.encode())

    # except on jsondecode error or invalid create request ('command' isn't 'roads')
    except Exception as e:
        printInvalidRequest(createReq)
        exit(1)

    # ----------------------------Processing Phase--------------------------------------------------
    # start accepting character/query inputs, create batch requests, and look for EOF (Ctrl+D)
    while True:
        try:
            # This inner loop is to assemble individual batch requests
            batch = {'characters': [], 'query': {}}
            # once the query field is populated we will exit the loop
            while not batch['query']:
                line = json.loads(input())
                cmd = line['command']
                params = line['params']

                charName = params['character']
                townName = params['town']

                # current input is a 'place' command
                if cmd == 'place':
                    charInput = {'name': charName, 'town': townName}
                    batch['characters'].append(charInput)

                # current input is a 'passage-safe?' command
                elif cmd == 'passage-safe?':
                    batch['query'] = {'character': charName, 'destination': townName}

                # current input is not a valid command
                else:
                    raise Exception()

            batch = json.dumps(batch)
            sock.sendall(batch.encode())

            serverOutput = ''
            while True:
                d = sock.recv(1024)
                serverOutput += d.decode()

                # TODO: this assumes that newline indicates the message is over, check piazza @227
                if not d or '\n' in serverOutput:
                    break

            serverOutput = json.loads(serverOutput)

            for i in serverOutput['invalid']:
                print(json.dumps(['invalid placement', {'name': i['name'], 'town': i['town']}]))

            print(json.dumps(
                ['the response for', {'character': charName, 'destination': townName}, 'is', serverOutput['response']]))

        except EOFError:
            break

        except Exception as e:
            printInvalidRequest(line)
            

def printInvalidRequest(jsonObj):
    print(json.dumps({"error" : "not a request", "object" : jsonObj}))
    exit(1)
