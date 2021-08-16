import pytest

from Snarl.src.Game.hallway import Hallway


def test_get_connecting_room1(hallway1, room1, room2):
    assert (hallway1.get_connecting_room(room1) is room2)
    assert (hallway1.get_connecting_room(room2) is room1)
