import pytest
from timeit import default_timer as timer

from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament

from pyschieber.example.greedy_player import GreedyPlayer
from pyschieber.player.challenge_player.challenge_player import ChallengePlayer


@pytest.mark.statistical
def test_greedy():
    point_limit = 1000
    number_of_tournaments = 1000
    players = [GreedyPlayer(name='Greedy1'), RandomPlayer(name='Track'), GreedyPlayer(name='Greedy2'),
               RandomPlayer(name='Track')]
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player) for player in players]

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
    print("Team Greedy: ", team_1_won)
    print("Team Random: ", team_2_won)
    assert team_1_won > team_2_won


@pytest.mark.statistical
def test_challenge():
    point_limit = 1000
    number_of_tournaments = 1000
    players = [GreedyPlayer(name='Greedy1'), ChallengePlayer(name='Track'), GreedyPlayer(name='Greedy2'),
               ChallengePlayer(name='Track')]
    tournament = Tournament(point_limit=point_limit)
    [tournament.register_player(player=player) for player in players]

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
    print("Team Greedy: ", team_1_won)
    print("Team Challenge: ", team_2_won)
    assert team_1_won < team_2_won
