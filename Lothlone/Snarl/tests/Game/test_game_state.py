import pytest

from Snarl.src.Game.player import Player


@pytest.fixture
def player1():
    return Player(0, 'Ben', (0, 0), 'B', {'movementDistance': 2, 'visionDistance': 2})


def test_add_player(gamestate1, player1):
    gamestate1.add_player(player1)
    assert len(gamestate1.players) == 1
    assert gamestate1.players[0] == player1
    assert gamestate1.get_player(player1.id) == player1


def test_render(gamestate1):
    assert str(gamestate1) == (".   .   .   .   .                                   \n"
                               ".   .   .   .   .               .   .   .   .   .   \n"
                               ".   .   .   .   |   .   .       .   .   .   .   .   \n"
                               ".   .   .   .   .       .   .   |   .   .   .   .   \n"
                               ".   .   .   .   .               .   .   .   .   .   \n"
                               "                                .   .   .   .   .   ")


def test_render2(gamestate1, player1):
    gamestate1.add_player(player1)
    assert str(gamestate1) == ("B   .   .   .   .                                   \n"
                               ".   .   .   .   .               .   .   .   .   .   \n"
                               ".   .   .   .   |   .   .       .   .   .   .   .   \n"
                               ".   .   .   .   .       .   .   |   .   .   .   .   \n"
                               ".   .   .   .   .               .   .   .   .   .   \n"
                               "                                .   .   .   .   .   ")
