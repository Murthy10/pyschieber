from example.greedy_player import GreedyPlayer
from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


def test_example_player():
    tournament = Tournament(point_limit=1500)
    example_player = GreedyPlayer.with_tournament(name='ExamplePlayer', tournament=tournament)
    tournament.register_player(example_player)
    [tournament.register_player(RandomPlayer(name=str(i))) for i in range(2, 5)]
    tournament.play()
    assert example_player.reward != 0

