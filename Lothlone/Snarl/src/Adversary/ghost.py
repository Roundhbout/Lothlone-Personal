import random

from ..Common.adversary import Adversary
from ..Game.level import get_neighbors
from ..Game.rule_checker import is_adversary_move_valid
from ..Game.tiletype import TileType


class Ghost(Adversary):
    def __init__(self, username, teleport_cooldown=5):
        super().__init__(username)
        self.teleport_cooldown = teleport_cooldown

    def get_id(self):
        return self.id


    def get_username(self):
        return self.username


    def get_move(self, gamestate):
        # get relevant information about our adversary agent and environment
        ghost = gamestate.get_adversary(self.id)
        level = gamestate.level
        gposition = ghost.position
        grow, gcol = gposition
        current_tile = level.grid[grow][gcol]

        RADIUS = 10

        # since we can only move once, get cardinal neighbor positions in the grid 
        successors = get_neighbors(level.grid, gposition, True)

        # check if the move is valid according to game rules
        valid_successors = []
        for pos in successors:
            posrow, poscol = pos
            # ghosts can walk into room walls (unwalkable from room), so we need to create an extra check to allow that
            if is_adversary_move_valid(gamestate, self.id, pos) or (not level.grid[posrow][poscol].is_walkable and
                (current_tile.type == TileType.room or current_tile.type == TileType.door)):
                valid_successors.append(pos)

        # cannot move, stand still
        if len(valid_successors) == 0:
            return gposition

        # only one valid move, we need to take it
        elif len(valid_successors) == 1:
            return valid_successors[0]

        # there are more than one move, let's do some greedy search!
        else:
            # this is a dict that will contain {position: manhattan distance}
            man_dists = {}

            """
            Need to check for any players in the radius so we're looping over all players.
            We might need to compare distances to multiple players as well.
            """
            for p in gamestate.players:
                # get player's position
                player_position = p.position
                prow, pcol = player_position

                # check if the player is in our radius (currently 10)
                if (abs(grow - prow) + abs(gcol - pcol)) <= RADIUS:
                    # for all still valid successors (there will be >= 2)
                    for pos in valid_successors:
                        new_row, new_col = pos
                        # get manhattan distance from successor to player position
                        dist = abs(new_row - prow) + abs(new_col - pcol)
                        # if we haven't checked this successor yet, add it to the dict
                        if pos not in man_dists:
                            man_dists[pos] = dist
                        # if we've checked this successor but found a shorter manhattan distance, overwrite that distance
                        elif man_dists[pos] > dist:
                            man_dists[pos] = dist

            # if there's a player within range, we'll go towards it
            if len(man_dists) > 0:
                # get the coordinates (key) for the moves with the smallest manhattan distnce
                best_moves = [key for key, val in man_dists if val == min(man_dists.values())]

                # filter valid_successors by if the coordinate is in best_moves
                valid_successors = [pos for pos in valid_successors if pos in best_moves]

                # we'll want to be able to teleport if the player gets away
                self.teleport_cooldown = 0

                # choose randomly among remaining actions
                return random.choice(valid_successors)

            else:
                # if we can teleport, we should be open to doing it
                if self.teleport_cooldown == 0:
                    for new_pos in valid_successors:
                        new_row, new_col = new_pos

                        # if this passes, we're going to take this action (teleport)
                        if level.grid[new_row][new_col].type == TileType.void and current_tile.type == TileType.room:
                            self.teleport_cooldown = 5
                            return self.get_teleport_location(gamestate)
                        # no walls adjacent, let's roam
                        else:
                            return random.choice(valid_successors)

                # we recently teleported, let's roam
                else:
                    self.teleport_cooldown -= 1
                    return random.choice(valid_successors)




    def set_id(self, id):
        self.id = id


    def update_gamestate(self, gamestate):
        self.gamestate = gamestate


    def set_response(self, move, result):
        self.last_move = move
        self.result = result

    def get_teleport_location(self, gamestate):
        return gamestate.find_placement_location()

