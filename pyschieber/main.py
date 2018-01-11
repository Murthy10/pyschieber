import argparse
import logging
import sys

from pyschieber.player.cli_player import CliPlayer
from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


def start_tournament(points):
    tournament = Tournament(points=points)
    cli_player = CliPlayer(name='CliPlayer')
    tournament.register_player(cli_player, 1)
    [tournament.register_player(RandomPlayer(), i) for i in range(2, 5)]
    tournament.play_game()


def set_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler)


if __name__ == "__main__":
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    set_logging()
    parser = argparse.ArgumentParser(description='CLI pyschieber', )
    parser.add_argument('-p', '--points', dest='points', type=int, help='Tournament points')
    parser.set_defaults(points=1500)
    args = parser.parse_args()
    start_tournament(args.points)