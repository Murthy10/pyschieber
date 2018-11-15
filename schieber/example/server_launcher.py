import argparse
import logging
from multiprocessing import Process

from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.server_player.server_player import ServerPlayer

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', )


def launch(server_address, session_name):
    opponents = [
        ServerPlayer(pyschieber_bot=GreedyPlayer(name='Greedy1'), server_address=server_address,
                     chosen_team_index=1, session_name=session_name),
        ServerPlayer(pyschieber_bot=GreedyPlayer(name='Greedy2'), server_address=server_address,
                     chosen_team_index=1, session_name=session_name)
    ]

    for opponent in opponents:
        process = Process(target=opponent.start)
        process.start()

    teammate = GreedyPlayer(name='Greedy Teammate')
    server_player = ServerPlayer(pyschieber_bot=teammate, server_address=server_address,
                                 session_name=session_name)
    server_player.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SchieberJassBot', )
    parser.add_argument('-a', '--server_address', dest='server_address', help='Default: ws://127.0.0.1:3000')
    parser.add_argument('-s', '--session_name', dest='session_name', help='Default: test')
    parser.set_defaults(server_address="ws://127.0.0.1:3000", session_name="test")
    args = parser.parse_args()
    launch(args.server_address, args.session_name)
