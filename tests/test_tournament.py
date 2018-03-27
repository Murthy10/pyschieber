import pytest
from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


@pytest.fixture(scope='module')
def random_players():
    return [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), RandomPlayer(name='Track'),
            RandomPlayer(name='Dagobert')]


def test_tournament_rounds(random_players):
    point_limit = 100
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player) for player in random_players]
    tournament.play(rounds=20)
    points = [tournament.teams[0].points, tournament.teams[1].points]
    assert 3 * point_limit < max(points)


def test_tournament(random_players):
    point_limit = 1000
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player) for player in random_players]
    tournament.play()
    points = [tournament.teams[0].points, tournament.teams[1].points]
    assert point_limit <= max(points) and point_limit > min(points)


def test_tournament_register(random_players):
    for _ in range(3):
        tournament = Tournament()
        [tournament.register_player(player=player) for player in random_players]
        tournament.play(rounds=1)
        assert tournament.teams[0].players[0].name == 'Tick'
        assert tournament.teams[0].players[1].name == 'Track'
        assert tournament.teams[1].players[0].name == 'Trick'
        assert tournament.teams[1].players[1].name == 'Dagobert'


def test_tournament_player_id(random_players):
    tournament = Tournament()
    [tournament.register_player(player=player) for player in random_players]
    assert tournament.players[0].name == 'Tick'
    assert tournament.players[1].name == 'Trick'
    assert tournament.players[2].name == 'Track'
    assert tournament.players[3].name == 'Dagobert'
