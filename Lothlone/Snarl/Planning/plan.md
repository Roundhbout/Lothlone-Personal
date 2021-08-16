##### Part 1

The Player class will have the following attributes: a unique ID, a name, a set of four coordinates representing the x,y of the room the player is in and the x,y of the tile the player is on, an appearance, a boolean indicating whether the player is expelled, and a list of stats, containing the player's movement distance (how many tiles they can move in a single turn) and their vision distance (how many tiles away they can see).

The Automated Adversary class will have a unique ID, a set of four coordinates (same structure as player), and a list of stats, currently only containing the adversary's movement distance.

The Game Software class will have a game state and a dungeon. The game state keeps track of the players, the round number (how many rounds have passed), the level number, the status of the whole game, and the state of the current level, which keeps track of the rooms, adversaries, and objects (key, door) currently in the level. The dungeon has a list of levels. Each level has a list of player starting locations and an initial levelState.

To make communication successful, the gamestate must be shared with the players and the adversaries. This is shared before and after every move that a player or adversary makes a move.

##### Part 2
1. implement levelstate with only rooms and objects, create test level
2. implement player with ID, name, position, appearance
3. implement gamestate with only players and levelstate, implement render in player class (given gamestate, renders full room with player in it)
4. implement player movement (stats[movementDistance], move(direction)), add user control
5. implement round number, level number, status, game logic(level advancement, object interaction), create test dungeon
6. implement visionDistance in player stats, adjust render to show only within visiondistance
7. implement stationary adversaries, update levelstate to include adversaries, update player to include isExpelled
8. implement movement for adversaries, add search functionality so adversaries can move towards players
