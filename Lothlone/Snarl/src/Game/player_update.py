class PlayerUpdate:
    def __init__(self, layout, position, objects=[], actors=[], message=None):
        self.layout = layout
        self.position = position
        self.objects = objects
        self.actors = actors
        self.message = message

    def render(self):
        grid = []
        for row in range(len(self.layout)):
            new_row = []
            for col in range(len(self.layout[0])):
                new_row.append(str(self.layout[row][col]))
            grid.append(new_row)

        # Place objects
        for obj in self.objects:
            new_obj_pos = self.global_to_local_position(obj.position)
            grid[new_obj_pos[0]][new_obj_pos[1]] = obj.appearance
        # Place actors
        for actor in self.actors:
            new_actor_pos = self.global_to_local_position(actor.position)
            grid[new_actor_pos[0]][new_actor_pos[1]] = actor.appearance

        grid[2][2] = 'x'

        return grid
    
    # realigns an items global position to fit accordingly in the layout
    def global_to_local_position(self, global_position):
        my_row, my_col = self.position

        global_row, global_col = global_position

        return global_row - my_row + 2, global_col - my_col + 2

    def __str__(self):
        render = self.render()
        return '\n'.join([''.join(['{:4}'.format(str(item)) for item in row]) for row in render])