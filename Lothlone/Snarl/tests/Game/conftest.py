import sys
import os
import pytest
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Snarl.src.User.local_user import LocalUser
from Snarl.src.Observer.local_observer import LocalObserver
from Snarl.src.Game.game_manager import GameManager
from Snarl.src.Game.gamestate import GameState
from Snarl.src.Game.room import Room
from Snarl.src.Game.level import Level
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.tile import Tile


@pytest.fixture
def layout():
    return [[Tile(True) for i in range(5)] for j in range(5)]


@pytest.fixture
def layout2():
    return [[Tile(True) for i in range(5)] for j in range(5)]


@pytest.fixture
def room1(layout):
    origin = (0, 0)
    size = (5, 5)
    doors = [(2, 4)]
    return Room(origin, size, layout, doors)


@pytest.fixture
def room2(layout2):
    origin2 = (1, 8)
    size2 = (5, 5)
    doors2 = [(2, 0)]
    return Room(origin2, size2, layout2, doors2)


@pytest.fixture()
def room3():
    return Room((1, 8),
                (5, 6),
                [[Tile(True) for i in range(6)] for j in range(5)],
                [(2, 0)])


@pytest.fixture
def hallway1(room1, room2):
    hall_start1 = (2, 4)
    hall_end1 = (3, 8)
    hall_waypoints1 = [(2, 6), (3, 6)]
    return Hallway(hall_start1, hall_end1, hall_waypoints1, room1, room2)


@pytest.fixture
def level1(room1, room2, hallway1):
    return Level([room1, room2], [hallway1], [])


@pytest.fixture
def gamestate1(level1):
    return GameState([], [], level1)


@pytest.fixture
def game_manager1(gamestate1):
    return GameManager(gamestate1)


@pytest.fixture
def user1():
    return LocalUser('Fred', io.StringIO(), io.StringIO())


@pytest.fixture
def observer1():
    return LocalObserver(io.StringIO())
