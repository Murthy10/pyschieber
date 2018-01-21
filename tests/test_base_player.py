from pyschieber.player.base_player import BasePlayer


def test_base_player_counter():
    base_player = [BasePlayer(name=i) for i in range(4)]

    for i, player in enumerate(base_player):
        assert player.id == i
