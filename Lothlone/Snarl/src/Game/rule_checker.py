from .player_status import PlayerStatus


def is_gamestate_valid(state):
    """Returns true if the given gameState is valid, checking all the underlying data
    structure for validity wherever possible. Including but not limited to checking
    validity of rooms and hallways, and locations of players, adversaries, and objects."""
    max_row, max_col = state.level.bounds
    # check if all players are on traversable tiles
    for player in state.players:
        row, col = player.position
        if state.level.grid[row][col].is_walkable:
            return False
        if row >= max_row or col >= max_col:
            return False
    # check if all adversaries are on traversable tiles
    for adversary in state.adversaries:
        row, col = adversary.position
        if state.level.grid[row][col].is_walkable:
            return False
        if row >= max_row or col >= max_col:
            return False
    # check if all objects are on traversable tiles
    for obj in state.adversaries:
        row, col = obj.position
        if state.level.grid[row][col].is_walkable:
            return False
        if row >= max_row or col >= max_col:
            return False


def is_level_over(state):
    """Returns true if all players have been removed from the dungeon (via the exit or expulsion)"""
    for player in state.players:
        if player.status == PlayerStatus.isInLevel:
            return False
    return True


def is_game_over(state, num_levels):
    # Game can't be over if this isn't the final level
    if state.level_num != num_levels - 1:
        return False
    # Check if any player has exited
    for player in state.players:
        if player.status == PlayerStatus.isExited:
            return True
    return is_level_over(state)


def is_player_move_valid(state, player_id, coordinates):
    row, col = coordinates

    # get the player object with the given id
    for p in state.players:
        if p.id == player_id:
            player = p

    current_row, current_col = player.position
    movement_distance = player.stats['movementDistance']

    # Check that coordinates are within bounds of level
    max_row, max_col = state.level.bounds
    if row >= max_row or col >= max_col:
        return False

    # check if destination tile is traversable
    tile = state.level.grid[row][col]
    if not tile.is_walkable:
        return False

    # check if any other players are there (not including current player)
    for p in state.players:
        if p.status == PlayerStatus.isInLevel and p.position == coordinates and p != player:
            return False

    # check if it is within player's movable range
    movement_vector = (abs(row - current_row), abs(col - current_col))
    if sum(movement_vector) > movement_distance:
        return False
    else:
        return True


def is_adversary_move_valid(state, adversary_id, coordinates):
    row, col = coordinates

    # get the adversary object with the given id
    for a in state.adversaries:
        if a.id == adversary_id:
            adversary = a

    current_row, current_col = adversary.position
    movement_distance = adversary.stats['movementDistance']

    # Check that coordinates are within bounds of level
    max_row, max_col = state.level.bounds
    if row >= max_row or col >= max_col:
        return False

    # check if destination tile is traversable
    tile = state.level.grid[row][col]
    if not tile.is_walkable:
        return False

    # check if any other adversaries are there (not including current adversary)
    for a in state.adversaries:
        if a.position == coordinates and a.id != adversary_id:
            return False

    # check if it is within adversaries movable range
    movement_vector = (abs(row - current_row), abs(col - current_col))
    if sum(movement_vector) > movement_distance:
        return False
    else:
        return True


def is_adversary_interaction_valid(state, player_id, adversary_id, coordinates):
    # Check if player is at coordinates
    player_coordinates_valid = False
    for player in state.players:
        if player_id == player_id and player.position == coordinates:
            player_coordinates_valid = True
    adversary_coordinates_valid = False
    for adversary in state.adversaries:
        if adversary_id == adversary_id and adversary.position == coordinates:
            adversary_coordinates_valid = True
    return player_coordinates_valid and adversary_coordinates_valid


def is_object_interaction_valid(state, player_id, object_id, coordinates):
    # Check if player is at coordinates
    player_coordinates_valid = False
    for player in state.players:
        if player.position == coordinates:
            player_coordinates_valid = True
    object_coordinates_valid = False
    for obj in state.objects:
        if obj.position == coordinates:
            object_coordinates_valid = True
    return player_coordinates_valid and object_coordinates_valid
