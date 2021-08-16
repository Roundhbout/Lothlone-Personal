# Adversary
This serves as the interface that the Game Manager will use to interact with the
Adversary component.   

Adversary objects will be passed into the server, which is considered "registration" (see Game Manager for more details), and the Game Manager will set the Adversary's `id` to a unique value.

This `id` value is not unique among all agents (i.e. an adversary can have the same id as a player), but it is unique among all adversaries. 

Adversaries themselves do not keep a gamestate as a field, as they only need it when it is passed to their `get_move` method as an argument. Adversaries receive the entire, unfiltered gamestate.

Adversaries should always know where the players are so that they can path to them and create actual challenge in the game. 

If the Game Manager calls the `get_move` method, which must include a gamestate update, the adversary will return a move based on the latest state.

## fields
`id` - adversary's unique id assigned by the Game Manager

## methods
`(row, col) get_move(gamestate)` - given an updated gamestate, the adversary will return the move they choose to make