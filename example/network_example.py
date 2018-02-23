import logging, sys

from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament
from pyschieber.player.network_player import NetworkPlayer


def start_tournament(points):
    tournament = Tournament(point_limit=points)

    network_player = NetworkPlayer.with_parameters(name='Dagobert', tournament=tournament, port=3000)
    players = [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), RandomPlayer(name='Track'), network_player]
    [tournament.register_player(player) for player in players]

    network_player.run()
    tournament.play()


def set_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler)


if __name__ == "__main__":
    set_logging()
    start_tournament(points=1500)
