import pytest

from pyschieber.example.greedy_player import GreedyPlayer
from pyschieber.helpers.pyschieber_helper import parse_player_choice
from pyschieber.player.challenge_player.challenge_player import ChallengePlayer
from pyschieber.player.random_player import RandomPlayer


@pytest.mark.parametrize("choice, player_type", [
    (1, RandomPlayer),
    (2, GreedyPlayer),
    (3, ChallengePlayer),
    (100, RandomPlayer),
    (0, RandomPlayer),
])
def test_parse_player_choice(choice, player_type):
    assert type(parse_player_choice(choice)) == player_type
