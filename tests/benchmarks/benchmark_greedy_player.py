import pytest

from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.random_player import RandomPlayer
from tests.benchmarks.statistical_helper import run_statistics


@pytest.mark.statistical
def test_against_random():
    players = [GreedyPlayer(name='GreedyActor'), RandomPlayer(name='RandomOpponent1'),
               GreedyPlayer(name='GreedyPartner'), RandomPlayer(name='RandomOpponent2')]
    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_random():
    players = [GreedyPlayer(name='GreedyActor'), RandomPlayer(name='RandomOpponent1'),
               RandomPlayer(name='RandomPartner'), RandomPlayer(name='RandomOpponent2')]
    run_statistics(players=players)
