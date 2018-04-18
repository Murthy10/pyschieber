import pytest
from pyschieber.rules.count_rules import counting_factor

from pyschieber.deck import Deck

from pyschieber.trumpf import Trumpf

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
    game.play()

    for player in random_players:
        assert len(player.cards) == 0


@pytest.mark.parametrize("start_key, next_key", [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
])
def test_get_player_index(start_key, next_key):
    generator = get_player_index(start_index=start_key)
    current_key = next(generator)
    assert current_key == next_key


@pytest.mark.parametrize("trumpf", list(Trumpf)[:6])
def test_add_points(trumpf):
    round_points = 152
    deck = Deck()
    random_players = [RandomPlayer(name=i) for i in range(4)]
    team_1 = Team(players=[random_players[0], random_players[1]])
    team_2 = Team(players=[random_players[1], random_players[2]])
    teams = [team_1, team_2]
    game = Game(teams=teams, use_counting_factor=True)
    game.trumpf = trumpf
    game.add_points(team_index=0, cards=deck.cards, last=False)
    assert team_1.points == round_points * counting_factor[trumpf]
    game.use_counting_factor = False
    game.add_points(team_index=1, cards=deck.cards, last=False)
    assert team_2.points == round_points
