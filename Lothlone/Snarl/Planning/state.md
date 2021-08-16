### Player
#### fields
- id: unique player ID assigned based on order players join
- name: username chosen by user
- position: coordinates representing the player's currently location in the level
- appearance: an object indicating how the player should appear when rendered
- status: enum indicating whether the player is in the level, has exited, or has been expelled
- stats: a list of integer stats, currently how far player can move and how far they can see
#### interface
- move(position) updates position
- exit(): exits the player from the dungeon, setting their status to isExited
- expel(): expels the player from the dungeon, setting their status to expelled

### Adversary
#### fields
- id: unique adversary ID
- position: coordinates representing adversary's current location
- appearance: an object indicating how the adversary should appear when rendered
- stats: a list of integer stats, currently how far the adversary can move
#### interface
- move(position) updates adversary's position

### Object
#### fields
- id: unique object ID
- position: coordinates representing object's current location
- appearance: an object indicating how the object should appear when rendered

### LevelState
#### fields
- A 2D list of tiles representing the level
- List of Adversaries
- List of Objects
#### interface
- addObject(Object)
- removeObject(id)

### GameState:
#### fields
- List of Players: contains all objects representing players in the dungeon
- A LevelState: state information of the current level being played
- roundNum: current round (a round passes after every player makes a move)
- currentPlayerId: id of the player's whose turn it currently is
- levelNum: the current level in the dungeon
- status: an enum regarding the current state of the game (not started, in progress, finished, etc)
#### interface
- addPlayer(string username): adds a new player to the dungeon
