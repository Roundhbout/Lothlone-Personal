import sys
import json

# from spec:
# addNewEdge takes two town names (string), creates new edge in network
# addNewCharacter takes character name (string) and town to add to (string)
# query takes destination town name (string) and character name (string), returns boolean

# read JSON from stdin
input = json.load(sys.stdin)
command = input['command']
params = input['params']

if command == 'roads':
    for road in params:
        addNewEdge(road['from'], road['to'])
elif command == 'place':
    addNewCharacter(params['character'], params['town'])
elif command == 'passage-safe?':
    result = query(params['town'], params['character'])
    answer = 'can' if result else 'cannot'
    print('{} {} travel to {} without running into anyone.'.format(params['character'], answer, params['town']))
else:
    raise ValueError('invalid command: ' + command)
