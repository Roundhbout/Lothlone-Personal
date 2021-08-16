# Snarl Instructions

Run `./local_snarl` on a command line to run the game, with the following (optional) arguments:

`--levels FILENAME` to specify a `.levels` file to be used. Default is `snarl.levels`

`--players N` to specify 1-4 players. Default is `1`

`--start N` to specify which level in the .levels file to start from

`--observe` to observe the game. Must have `--players 1`.

The game will prompt each player for their username. After the specified number of players have entered their username, the game will begin, and the first player to register will take their turn. The player will be provided the level rendering what they can see, and will be provided their absolute position in the level in the form of a `(row, column)` pair. `(Row, Column)` coordinates have the origin at the top left of the level, so the larger `Row` is, the further 'down' the player will be, and the larger `Column` is, the further 'right' the player will be.  Players will then be prompted to make a move to a tile at most two tiles away (manhattan distance <=2). The input for this is of form: `<row>, <column>`, using absolute coordinate system (i.e. if the player is at `(2, 3)` and wants to move down two tiles, the player should input `4, 3`). After typing in the desired destination coordinates, the player must press enter to submit the move to the game. If nothing is input, then the game will make the player stand still for that turn. If the player makes an invalid move (i.e. into the void), then the game will indicate so and prompt the player to make a move again.