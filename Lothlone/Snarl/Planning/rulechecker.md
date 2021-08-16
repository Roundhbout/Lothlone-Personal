# RuleChecker

#### isGameStateValid(gameState)  
Returns true if the given gameState is valid, checking all the underlying data
structure for validity wherever possible. Including but not limited to checking
validity of rooms and hallways, and locations of players, adversaries, and objects.
#### isLevelOver(gameState)  
Returns true if all players have been removed from the dungeon (via the exit or expulsion)
#### isGameOver(gameState)  
Returns true if all players have been expelled or any player has exited the final level
#### isPlayerMoveValid(gameState, playerId, coordinates)  
Determines if the player can make a valid move to the destination given their movementDistance stat
#### isAdversaryMoveValid(gameState, adversaryId, coordinates)  
Determines if the adversary can make a valid move to the destination based on their stats
#### isAdversaryInteractionValid(gameState, playerId, adversaryId, coordinates)  
Determines if the player can interact with the adversary at the specified position
#### isObjectInteractionValid(gameState, playerId, objectId, coordinates)  
Determines if the player can interact with the object at the specified position
