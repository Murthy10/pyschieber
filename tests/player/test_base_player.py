from schieber.player.base_player import BasePlayer
from itertools import count


def test_base_player_counter():
    BasePlayer.class_counter = count(0)
    base_player = [BasePlayer(name=i) for i in range(4)]

    for i, player in enumerate(base_player):
        assert player.name == i
