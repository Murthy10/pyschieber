import pytest
from timeit import default_timer as timer
from math import sqrt, floor

from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


@pytest.mark.statistical
def test_is_random():
    point_limit = 1000
    number_of_tournaments = 1000
    mean = number_of_tournaments * 0.5  # assume that a RandomPlayer has a 50% chance to win
    variance = mean * (1 - 0.5)
    standard_deviation = int(floor(sqrt(variance)))

    random_players = [RandomPlayer(name=i) for i in range(4)]
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player) for player in random_players]

    team_1_won = 0
    team_2_won = 0

    start = timer()

    for _ in range(number_of_tournaments):
        tournament.play()
        if tournament.teams[0].won(point_limit=point_limit):
            team_1_won += 1
        else:
            team_2_won += 1

    end = timer()
    print("\nTo run {0} tournaments it took {1:.2f} seconds.".format(number_of_tournaments, end - start))

    difference = abs(team_1_won - team_2_won)
    print("Difference: ", difference)
    print("Team 1: ", team_1_won)
    print("Team 2: ", team_2_won)
    assert difference in range(0, 2 * standard_deviation)
