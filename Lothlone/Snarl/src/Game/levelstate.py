from .level import Level


class LevelState:
    def __init__(self, rooms, hallways, adversaries, objects):
        self.level = Level(rooms, hallways)
        self.adversaries = adversaries
        self.objects = objects

    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, object_id):
        self.objects = [obj for obj in self.objects if obj.id != object_id]
