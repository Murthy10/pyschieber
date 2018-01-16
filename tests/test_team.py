import pytest

from pyschieber.player.random_player import RandomPlayer
from pyschieber.team import Team


@pytest.mark.parametrize("points, point_limit, won", [
    (0, 100, False),
    (100, 100, True),
    (110, 100, True),
])
def test_team_points(points, point_limit, won):
    random_players = [RandomPlayer(name=i) for i in range(2)]
    team = Team(players=random_players)
    team.points = points
    assert team.won(point_limit) == won
