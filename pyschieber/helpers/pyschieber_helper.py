from pyschieber.example.greedy_player import GreedyPlayer
from pyschieber.player.challenge_player.challenge_player import ChallengePlayer
from pyschieber.player.random_player import RandomPlayer


def parse_player_choice(player_choice=1, name_suffix=''):
    player_choices = {1: RandomPlayer(name='RandomPlayer ' + name_suffix),
                      2: GreedyPlayer(name='GreedyPlayer ' + name_suffix),
                      3: ChallengePlayer(name='ChallengePlayer ' + name_suffix)}
    choice = player_choice if player_choice in player_choices else 1
    return player_choices[choice]
