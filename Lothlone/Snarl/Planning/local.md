```
             Adversaries   Game Software       Player                      User
                     +         +                 +                           +
          Startup +------------------------------------------------------------+
                     |         |                 |                           |
                     |         |                 | <------------------------ | Create
                     |         |                 |                           | Player
    Join [adversary] | ------> | <-------------- | Join [player]             |
                     |         |                 |                           |
        AckJoin [id] | <------ | --------------> | AckJoin [id, gameState]   |
                     |         |                 |                           |
                     |         |                 | +-----------------------> | Render
                     +         +                 +                           +  Game
      (Waiting for  ...       ...               ...                         ...
       Other Players)+         +                 +                           +
                     |         |   After Each    |                           |
                     |         | --------------> | UpdateGS [gameState]      |
                     |         |  Player Joins   |                           |
                     |         |                 | +-----------------------> | Render
                     |         |                 |                           |  Game
     Player Moves +------------------------------------------------------------+   <----+
                     |         |                 |                           |          |
                     |         | +-------------> | StartTurn [gameState]     |          |
                     |         |                 |                           |          |
                     |         |                 | +-----------------------> | Render   |
                     |         |                 |                           |  Game    |
                     |         |                 | <-----------------------+ | Move     |
                     |         |                 |                           |          |
                     |         | <-------------- | MakeMove [position]       |          |
                     |         |                 |                           |          |
                     |         | +-------------> | UpdateGS [gameState]      |          |
                     |         |                 |                           |          |
                     |         |                 | +-----------------------> | Render   |
                     |         |                 |                           |  Game    |
      (Waiting for  ...       ...               ...                         ...         |
       Other Players)+         +                 +                           +          |
                     |         |   After Each    |                           |          |
                     |         | +-------------> | UpdateGS [gameState]      |          |
                     |         |  Player Moves   |                           |          |
                     |         |                 | +-----------------------> | Render   |
                     |         |                 |                           |  Game    |
  Adversary Moves +-------------------------------------------------------------+       |
                     |         |                 |                           |          |
UpdateGS [gameState] | <-----+ |                 |                           |          |
                     |         |                 |                           |          |
 MakeMove [position] | ------> |                 |                           |          |
                     |         |                 |                           |          |
                     |         | +-------------> | UpdateGS [gameState]      |          |
                     |         |                 |                           |          |
                     |         |                 | +-----------------------> | Render   |
                     |         |                 |                           |  Game    |
                     +         +                 +                           +       ---+
   Game End can occur at either final UpdateGS in                       Go back to start
   the Player Moves phase (one player exits, win)                       of Player Moves
   or the Adversary Moves phase (all expelled, lose)
```