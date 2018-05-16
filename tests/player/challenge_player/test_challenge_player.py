import pytest

from pyschieber.player.challenge_player.challenge_player import ChallengePlayer
from pyschieber.player.greedy_player.greedy_player import GreedyPlayer
from pyschieber.player.random_player import RandomPlayer
from tests.example.statistical_helper import run_statistics


@pytest.mark.statistical
def test_greedy():
    players = [GreedyPlayer(name='Greedy1'), RandomPlayer(name='Track1'), GreedyPlayer(name='Greedy2'),
               RandomPlayer(name='Track2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_challenge():
    players = [ChallengePlayer(name='Trick1'), GreedyPlayer(name='Greedy1'), ChallengePlayer(name='Trick2'),
               GreedyPlayer(name='Greedy2')]
    
    run_statistics(players=players)
