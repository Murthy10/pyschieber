import pytest

from pyschieber.team import Team


@pytest.mark.parametrize("points, point_limit, won", [
    (0, 100, False),
    (100, 100, True),
    (110, 100, True),
])
def test_team_points(points, point_limit, won):
    team = Team()
    team.points = points
    assert team.won(point_limit) == won
