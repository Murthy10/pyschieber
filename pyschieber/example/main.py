from pyschieber.example.greedy_player import GreedyPlayer
from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


def start_tournament(points):
    tournament = Tournament(point_limit=points)

    players = [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), RandomPlayer(name='Track'),
               GreedyPlayer(name='Dagobert')]

    [tournament.register_player(player) for player in players]

    tournament.play()


if __name__ == "__main__":
    start_tournament(points=1500)
