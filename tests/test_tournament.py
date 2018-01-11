from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


def test_tournament():
    random_players = [RandomPlayer(name=i) for i in range(1, 5)]
    point_limit = 1000
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player, number=index + 1) for index, player in enumerate(random_players)]
    tournament.start()
    tournament.play_game()
    points = [tournament.team_1['points'], tournament.team_2['points']]
    assert point_limit <= max(points) and point_limit > min(points)
