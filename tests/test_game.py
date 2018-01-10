import pytest

from pyschieber.player.random_player import RandomPlayer

from pyschieber.game import Game, get_player_key


@pytest.mark.parametrize("start_key, last_key", [
    (1, 4),
    (2, 1),
    (3, 2),
    (4, 3),
])
def test_get_player_key(start_key, last_key):
    key = 0
    count = 0
    for i in get_player_key(start_key):
        key = i
        count += 1
    assert count == 3
    assert last_key == key


def test_game():
    players = {}
    random_players = [RandomPlayer(name=i) for i in range(1, 5)]
    players[1] = random_players[0]
    players[2] = random_players[1]
    players[3] = random_players[2]
    players[4] = random_players[3]

    game = Game(players=players)

    game.start()
