from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


def test_tournament():
    random_players = [RandomPlayer(name=i) for i in range(4)]
    point_limit = 1000
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player) for player in random_players]
    tournament.play()
    points = [tournament.teams[0].points, tournament.teams[1].points]
    assert point_limit <= max(points) and point_limit > min(points)
