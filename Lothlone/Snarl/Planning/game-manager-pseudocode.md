```
def start_game():
    initialize, set game status to started
    run_game()
    
def state_update():
    //update state
    while(round is going on)
        // keep asking until move is valid
        move = players[currentplayerid].get_move(gamestate)
        // mutate game state correctly based on move
        update currentPlayerId
    while(adversaries)
        adversaries will move
        // mutate game state
    roundNum++

def run_game():
    while(game status is not end):
        state_update()
```