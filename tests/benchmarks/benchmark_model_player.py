import pytest
from schieber.player.challenge_player.challenge_player import ChallengePlayer

from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.model_player import ModelPlayer
from schieber.player.random_player import RandomPlayer
from tests.benchmarks.statistical_helper import run_statistics


@pytest.mark.statistical
def test_against_random():
    players = [ModelPlayer(name='ModelActor'), RandomPlayer(name='RandomOpponent1'),
               ModelPlayer(name='ModelPartner'), RandomPlayer(name='RandomOpponent2')]
    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_random():
    players = [ModelPlayer(name='ModelActor'), RandomPlayer(name='RandomOpponent1'),
               RandomPlayer(name='RandomPartner'), RandomPlayer(name='RandomOpponent2')]
    run_statistics(players=players)


@pytest.mark.statistical
def test_against_greedy():
    players = [ModelPlayer(name='ModelActor'), GreedyPlayer(name='GreedyOpponent1'),
               ModelPlayer(name='ModelPartner'), GreedyPlayer(name='GreedyOpponent2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_greedy():
    players = [ModelPlayer(name='ModelActor'), GreedyPlayer(name='GreedyOpponent1'),
               GreedyPlayer(name='GreedyPartner'), GreedyPlayer(name='GreedyOpponent2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_against_challenge():
    players = [ModelPlayer(name='ModelActor'), ChallengePlayer(name='ChallengeOpponent1'),
               ModelPlayer(name='ModelPartner'), ChallengePlayer(name='ChallengeOpponent2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_challenge():
    players = [ModelPlayer(name='ModelActor'), ChallengePlayer(name='ChallengeOpponent1'),
               ChallengePlayer(name='ChallengePartner'), ChallengePlayer(name='ChallengeOpponent2')]

    run_statistics(players=players)
