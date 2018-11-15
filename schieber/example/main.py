from schieber.player.challenge_player.challenge_player import ChallengePlayer
from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.random_player import RandomPlayer
from schieber.tournament import Tournament


def start_tournament(points):
    tournament = Tournament(point_limit=points)

    players = [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), ChallengePlayer(name='Track'),
               GreedyPlayer(name='Dagobert')]

    [tournament.register_player(player) for player in players]

    tournament.play()


if __name__ == "__main__":
    start_tournament(points=1500)
