from timeit import default_timer as timer

from schieber.tournament import Tournament


def run_statistics(players, number_of_tournaments=10):
    point_limit = 1000

    tournament = Tournament(point_limit=point_limit, seed=42)
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
    print("Team 1: ", team_1_won)
    print("Team 2: ", team_2_won)
    assert team_1_won > team_2_won
