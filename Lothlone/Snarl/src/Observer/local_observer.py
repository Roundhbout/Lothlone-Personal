import sys

from ..Common.observer import Observer


class LocalObserver(Observer):
    def __init__(self, output_stream=sys.stdout):
        super().__init__()
        self.output_stream = output_stream

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def update_gamestate(self, gamestate):
        self.gamestate = gamestate
        self.output_stream.write(str(self.gamestate) + '\n\n')
