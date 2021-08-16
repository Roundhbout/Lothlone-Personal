#!/usr/bin/env python3

import json
import sys
import argparse

# Use argparse to read arguments

parser = argparse.ArgumentParser(description='Read in a well-formed JSON input and a single argument: --sum or --product')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--sum', action='store_const', const='sum')
group.add_argument('--product', action='store_const', const='product')

args = vars(parser.parse_args())
if(args['sum']):
    operation = 'sum'
elif(args['product']):
    operation = 'product'
else:
    print('No operation specified')
    exit(1)

print("Args: {}".format(args))


# Use built-in JSON module to parse input, catch error if not well-formed
print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
contents = ''
while True:
    try:
        line = input()
    except EOFError:
        break
    contents += line

# decodes first well-formed json input from string, ignores rest
decoder = json.JSONDecoder()
jsons = []
contentsIdx = 0
while(contentsIdx < len(contents)):
    try:
        # ignore leading whitespace
        contentsIdx += len(contents[contentsIdx:]) - len(contents[contentsIdx:].lstrip())
        # decode next json object
        nextJson = contents[contentsIdx:]
        newJson, length = decoder.raw_decode(nextJson)
        jsons.append(newJson)
        # advance to next json
        contentsIdx += length        
    except ValueError:
        print('Malformed JSON, please try again')
        exit(1)


def calculate(numjson, op):
    if(op == 'sum'):
        total = 0
    else:
        total = 1

    if(type(numjson) is int):
        return numjson
    elif(type(numjson) is str):
        return total
    elif(type(numjson) is list):
        for n in numjson:
            if(op == 'sum'):
                total += calculate(n, op)
            else:
                total *= calculate(n, op)
        return total
    elif(type(numjson) is dict):
        if(numjson.get('payload') is None):
            print('Malformed input: JSON object missing payload field')
            exit(1)
        return calculate(numjson.get('payload'), op)
    else:
        print('{} is not a numJSON, please try again'.format(numjson))
        exit(1)
        
output = []
for j in jsons:
    obj = {}
    obj["object"] = j
    obj["total"] = calculate(j, operation)
    output.append(obj)

print('\n')
print(json.dumps(output))
