class Adversary:
    def __init__(self, id, name, type, position, stats={'movementDistance': 1}):
        self.id = id
        self.name = name
        self.type = type
        self.position = position
        self.stats = stats
        self.appearance = str(self.type)[0].lower()

    def move(self, position):
        self.position = position
