import pytest

from schieber.player.challenge_player.challenge_player import ChallengePlayer
from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.random_player import RandomPlayer
from tests.benchmarks.statistical_helper import run_statistics


@pytest.mark.statistical
def test_against_random():
    players = [ChallengePlayer(name='Challenge1'), RandomPlayer(name='Random1'), ChallengePlayer(name='Challenge2'),
               RandomPlayer(name='Random2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_against_greedy():
    players = [ChallengePlayer(name='Challenge1'), GreedyPlayer(name='Greedy1'), ChallengePlayer(name='Challenge2'),
               GreedyPlayer(name='Greedy2')]
    
    run_statistics(players=players)
