class User:
    def __init__(self, username):
        self.gamestate = None
        self.id = 0

    def get_move(self, gamestate):
        # move to player's current location (dummy move)
        self.gamestate = gamestate
        for player in gamestate:
            if player.id == self.id:
                return player.position
        # TODO better exception
        raise Exception('Player not in gamestate')
