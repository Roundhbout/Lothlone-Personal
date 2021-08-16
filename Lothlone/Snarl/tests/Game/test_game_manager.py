import pytest

from Snarl.src.Game.game_manager import GameManager
from Snarl.src.Game.gamestate import GameState
from Snarl.src.User.local_user import LocalUser


def test_register_user(game_manager1, user1):
    game_manager1.register_user(user1)
    assert len(game_manager1.gamestate.players) == 1
    assert len(game_manager1.users) == 1
    assert game_manager1.gamestate.players[0].id == 0
    assert game_manager1.users.get(0).get_id() == 0


def test_register_observer(game_manager1, observer1):
    game_manager1.register_observer(observer1)
    assert len(game_manager1.observers) == 1
    assert game_manager1.observers.get(0).get_id() == 0
