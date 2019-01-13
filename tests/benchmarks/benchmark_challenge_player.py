import pytest

from schieber.player.challenge_player.challenge_player import ChallengePlayer
from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.random_player import RandomPlayer
from tests.benchmarks.statistical_helper import run_statistics


@pytest.mark.statistical
def test_against_random():
    players = [ChallengePlayer(name='ChallengeActor'), RandomPlayer(name='RandomOpponent1'),
               ChallengePlayer(name='ChallengePartner'), RandomPlayer(name='RandomOpponent2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_random():
    players = [ChallengePlayer(name='ChallengeActor'), RandomPlayer(name='RandomOpponent1'),
               RandomPlayer(name='RandomPartner'), RandomPlayer(name='RandomOpponent2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_against_greedy():
    players = [ChallengePlayer(name='ChallengeActor'), GreedyPlayer(name='GreedyOpponent1'),
               ChallengePlayer(name='ChallengePartner'), GreedyPlayer(name='GreedyOpponent2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_greedy():
    players = [ChallengePlayer(name='ChallengeActor'), GreedyPlayer(name='GreedyOpponent1'),
               GreedyPlayer(name='GreedyPartner'), GreedyPlayer(name='GreedyOpponent2')]

    run_statistics(players=players)
