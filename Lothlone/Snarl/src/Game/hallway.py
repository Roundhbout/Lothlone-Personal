class Hallway:
    """
    Class to represent a hallway

    Parameters:
        start (tuple): Coordinate (row,col) to represent starting endpoint of the hallway.
            Must be the same as a door coordinate in a room
        end (tuple): Coordinate (row,col) to represent ending endpoint of the hallway.
            Must be the same as a door coordinate in a different room
        waypoints (List): List of Coordinates (row,col) representing waypoints (likely corners) throughout the hallway.
        start_room (Room): The Room object which has a door sharing the same coordinate as the start coordinate
        end_room (Room): The Room object which has a door sharing the same coordinate as the end coordinate

        Each subsequent pair of waypoints (starting with start and ending with end) must be horizontal or vertical.

        All points must be relative to the level
    """
    def __init__(self, start, end, waypoints, start_room, end_room):
        self.start = start
        self.end = end

        # list of start, waypoints, and end points
        self.points = [start] + waypoints + [end]

        # list of every coordinate point the hallway is made of
        self.all_points = []

        for idx in range(len(self.points) - 1):
            p1 = self.points[idx]
            p1row, p1col = p1
            p2 = self.points[idx + 1]
            p2row, p2col = p2

            # subsequent waypoints are not on the same x or y axis
            if p1row != p2row and p1col != p2col:
                raise ValueError("Improper line between waypoints: {} -> {}".format(p1, p2))

            # add to all_points all the points between p1 and p2
            elif p1row == p2row:
                for i in range(min(p1col, p2col), max(p1col, p2col) + 1):
                    if (p1row, i) not in self.all_points:
                        self.all_points.append((p1row, i))
            else:
                for j in range(min(p1row, p2row), max(p1row, p2row) + 1):
                    if (j, p1col) not in self.all_points:
                        self.all_points.append((j, p1col))

        # remove the start and end points
        self.all_points.remove(start)
        self.all_points.remove(end)

        self.waypoints = waypoints

        self.start_room = start_room
        self.end_room = end_room

    def get_connecting_room(self, room):
        if self.start_room == room:
            return self.end_room
        else:
            return self.start_room
