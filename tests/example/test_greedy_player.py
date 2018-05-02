import pytest

from pyschieber.example.greedy_player import GreedyPlayer
from pyschieber.player.random_player import RandomPlayer

from tests.example.statistical_helper import run_statistics


@pytest.mark.statistical
def test_greedy():
    players = [GreedyPlayer(name='Greedy1'), RandomPlayer(name='Track'), GreedyPlayer(name='Greedy2'),
               RandomPlayer(name='Track')]
    run_statistics(players=players)
