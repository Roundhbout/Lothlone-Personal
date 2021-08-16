# Game Manager
##fields
gamestate - object representing gamestate, defined in state.md
players - dict where key=player_id and value=Player  

##methods
id register_player(name) - creates and adds a new player to the gamestate with unique
id and appearance and starting location, and returns the id of the newly created player  
start_game() - starts the game  
gamestate filter_game_state(gamestate, id) - creates a copy of the gamestate that is
specific to what that player will be able to see based on their surroundings and
vision distance stat  
player_turn(id) - ask player for turn, validate it, update gamestate based on movements and
order of interactions with any encountered objects
