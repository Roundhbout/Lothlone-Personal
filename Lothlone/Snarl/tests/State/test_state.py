#!/usr/bin/env python3
import sys
import json
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Snarl.src.json_utils import *
import Snarl.src.Game.rule_checker as checker

input = json.loads(''.join(sys.stdin.readlines()))
input_state = input[0]
input_name = input[1]
point = tuple(input[2])
point_row, point_col = point

newGameState = json_to_gamestate(input_state)

# ------------tests------------
output = []

# ------------check if player isn't in input state------------
player_names = [p.name for p in newGameState.players]

if input_name not in player_names:
    output = ["Failure", "Player ", input_name, " is not a part of the game."]

else:
    player = None
    for p in newGameState.players:
        if input_name == p.name:
            player = p
    
    # check if move is valid
    if checker.is_player_move_valid(newGameState, player.id, point):
        player.move(point)
        # have to untranslate new_gamestate
        output = []

        """
        our game manager will handle the validation/results of interactions, so we'll
        have to manually test these moves and manually operate the gamestate, since we're \
        testing the gamestate and not the game manager
        """
        adv_positions = [a.position for a in newGameState.adversaries]
        if player.position in adv_positions:
            # player landed on an adversary
            player.expel()
            newGameState.players.remove(player)
            output = ["Success", "Player ", player.name, " was ejected.", gamestate_to_json(newGameState)]
        else:
            for object in newGameState.level.objects:
                if object.name == "exit":
                    if player.position == object.position and not input_state["exit-locked"]:
                        # player landed on an open exit
                        player.exit()
                        newGameState.players.remove(player)
                        output = ["Success", "Player ", player.name, " exited.", gamestate_to_json(newGameState)]
                # we landed on the key, unlock the door
                elif object.name == "key":
                    if player.position == object.position:
                        newGameState.level.objects.remove(object)
        
        if not output:
            output = ["Success", gamestate_to_json(newGameState)]

    else:
        # player destination is invalid
        output = ["Failure", "The destination position ", point, " is invalid"]

print(json.dumps(output))
