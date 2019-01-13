import pytest
from schieber.player.challenge_player.challenge_player import ChallengePlayer

from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.player.model_player import ModelPlayer
from schieber.player.random_player import RandomPlayer
from tests.benchmarks.statistical_helper import run_statistics


@pytest.mark.statistical
def test_against_random():
    players = [ModelPlayer(name='Model1'), RandomPlayer(name='Random1'), ModelPlayer(name='Model2'),
               RandomPlayer(name='Random2')]
    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_random():
    players = [ModelPlayer(name='Model1'), RandomPlayer(name='Random1'), RandomPlayer(name='RandomPartner'),
               RandomPlayer(name='Random2')]
    run_statistics(players=players)


@pytest.mark.statistical
def test_against_greedy():
    players = [ModelPlayer(name='Model1'), GreedyPlayer(name='Greedy1'), ModelPlayer(name='Model2'),
               GreedyPlayer(name='Greedy2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_greedy():
    players = [ModelPlayer(name='Model1'), GreedyPlayer(name='Greedy1'), GreedyPlayer(name='GreedyPartner'),
               GreedyPlayer(name='Greedy2')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_against_challenge():
    players = [ModelPlayer(name='Model1'), ChallengePlayer(name='Challenge2'), ModelPlayer(name='Model2'),
               ChallengePlayer(name='Challenge1')]

    run_statistics(players=players)


@pytest.mark.statistical
def test_with_and_against_challenge():
    players = [ModelPlayer(name='Model1'), ChallengePlayer(name='Challenge1'), ChallengePlayer(name='ChallengePartner'),
               ChallengePlayer(name='Challenge2')]

    run_statistics(players=players)
