from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament
from example.example_player import GreedyPlayer


def start_tournament(points):
    tournament = Tournament(point_limit=points)

    players = [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), RandomPlayer(name='Track'),
               GreedyPlayer.with_tournament(name='Dagobert', tournament=tournament)]
    map(tournament.register_player, players)

    tournament.play()


if __name__ == "__main__":
    start_tournament(points=1500)
