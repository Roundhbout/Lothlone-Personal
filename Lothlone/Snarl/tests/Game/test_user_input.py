import pytest
import sys

from Snarl.src.User.local_user import LocalUser


def test_run(capsys, game_manager1):
    with capsys.disabled():
        user = LocalUser('Fred', sys.stdin, sys.stdout)
        game_manager1.register_user(user)
        game_manager1.start_game()
