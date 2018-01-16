import pytest

from pyschieber.player.random_player import RandomPlayer

from pyschieber.game import Game, get_player_index
from pyschieber.team import Team


@pytest.mark.parametrize("start_key, last_key", [
    (0, 3),
    (1, 0),
    (2, 1),
    (3, 2),
])
def test_get_player_key(start_key, last_key):
    key = 0
    count = 0
    for i in get_player_index(start_key):
        key = i
        count += 1
    assert count == 3
    assert last_key == key


def test_game():
    random_players = [RandomPlayer(name=i) for i in range(4)]
    team_1 = Team(players=[random_players[0], random_players[1]])
    team_2 = Team(players=[random_players[1], random_players[2]])
    teams = [team_1, team_2]
    game = Game(teams=teams, point_limit=1500)
    game.start()

    for player in random_players:
        assert len(player.cards) == 0
