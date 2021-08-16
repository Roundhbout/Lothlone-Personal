import random

from ..Common.adversary import Adversary
from ..Game.level import get_neighbors
from ..Game.rule_checker import is_adversary_move_valid
from ..Game.tiletype import TileType


class Zombie(Adversary):
    def __init__(self, username):
        super().__init__(username)

   
    def get_id(self):
        return self.id

    
    def get_username(self):
        return self.username

    
    def get_move(self, gamestate):
        # get relevant information about our adversary agent and environment
        zombie = gamestate.get_adversary(self.id)
        level = gamestate.level
        zposition = zombie.position
        zrow, zcol = zposition
        current_room = level.grid[zrow][zcol].origin

        # since we can only move once, get cardinal neighbor positions in the grid 
        successors = get_neighbors(level.grid, zposition, True)

        # check if the move is valid according to game rules (and zombies can't walk through doors)
        valid_successors = []
        for pos in successors:
            prow, pcol = pos
            if is_adversary_move_valid(gamestate, self.id, pos) and level.grid[prow][pcol].type != TileType.door:
                valid_successors.append(pos)
        
        # cannot move, stand still
        if len(valid_successors) == 0:
            return zposition
        
        # only one valid move, we need to take it
        elif len(valid_successors) == 1:
            return valid_successors[0]
        
        # there are more than one move, let's do some greedy search!
        else:
            # this is a dict that will contain {position: manhattan distance}
            man_dists = {}

            """
            Need to check for any players in the same room, so we're looping over all players.
            We might need to compare distances to multiple players as well.
            """
            for p in gamestate.players:
                # get player's position and room they're in
                player_position = p.position
                prow, pcol = player_position
                player_room = level.grid[prow][pcol].origin

                # check if the player is in our room
                if player_room == current_room:
                    # for all still valid successors (there will be >= 2)
                    for pos in valid_successors:
                        new_row, new_col = pos
                        
                        # if this is a wall tile, don't go to it since we can sense a player nearby
                        if level.grid[new_row][new_col].type == TileType.void:
                            dist = float('inf')
                        # get manhattan distance from successor to player position
                        else:
                            dist = abs(new_row - prow) + abs(new_col - pcol)
                        # if we haven't checked this successor yet, add it to the dict
                        if pos not in list(man_dists.keys()):
                            man_dists[pos] = dist
                        # if we've checked this successor but found a shorter manhattan distance, overwrite that distance
                        elif man_dists[pos] > dist:
                            man_dists[pos] = dist

            # get the coordinates (key) for the moves with the smallest manhattan distance
            if len(man_dists) > 0:
                best_moves = [key for key, val in man_dists.items() if val == min(man_dists.values())]

                # filter valid_successors by if the coordinate is in best_moves
                valid_successors = [pos for pos in valid_successors if pos in best_moves]

                
            
            
            # choose randomly among remaining valid successors
            return random.choice(valid_successors)
            


    
    def set_id(self, id):
        self.id = id

    
    def update_gamestate(self, gamestate):
        self.gamestate = gamestate

    
    def set_response(self, move, result):
        self.last_move = move
        self.result = result