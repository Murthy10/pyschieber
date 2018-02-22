from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament
from example.example_player import ExamplePlayer


def start_tournament(points):
    tournament = Tournament(point_limit=points)
    example_player = ExamplePlayer.with_tournament(name='ExamplePlayer', tournament=tournament)
    tournament.register_player(example_player)
    [tournament.register_player(RandomPlayer(name=str(i))) for i in range(2, 5)]
    tournament.play()


if __name__ == "__main__":
    start_tournament(points=1500)
