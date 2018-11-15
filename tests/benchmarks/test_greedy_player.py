import pytest

from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.random_player import RandomPlayer
from tests.benchmarks.statistical_helper import run_statistics


@pytest.mark.statistical
def test_against_random():
    players = [GreedyPlayer(name='Greedy1'), RandomPlayer(name='Random1'), GreedyPlayer(name='Greedy2'),
               RandomPlayer(name='Random2')]
    run_statistics(players=players)
