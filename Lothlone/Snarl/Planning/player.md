# Player
This serves as the interface that the Game Manager will use to interact with the
Player component. Player objects will be passed into the server, which is considered
"registration" (see Game Manager for more details), and the Game Manager will set
the Player's id to a unique value. The Game Manager can update the Player's gamestate field,
which contains all the information currently available to them (limited layout
view based on their site, their location, and nearby objects, adversaries, and other players).
If the Game Manager calls the get_move method, which must include a gamestate update, the
player will update its own gamestate field and return a move based on the latest state.

##fields
gamestate - the gamestate from the limited perspective of the player  
id - player's unique id assigned by the Game Manager

##methods
(row, col) get_move(gamestate) - given an updated gamestate, the player will return
the move they choose to make