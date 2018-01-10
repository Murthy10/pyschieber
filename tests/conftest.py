import pytest

from pyschieber.card import Card
from pyschieber.player.random_player import RandomPlayer
from pyschieber.stich import PlayedCard
from pyschieber.suit import Suit


@pytest.fixture(scope="session", autouse=True)
def players():
    return [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]


@pytest.fixture(scope="session", autouse=True)
def played_cards(players):
    return [PlayedCard(player=players[0], card=Card(Suit.BELL, 10)),
            PlayedCard(player=players[1], card=Card(Suit.ACORN, 6)),
            PlayedCard(player=players[2], card=Card(Suit.BELL, 13)),
            PlayedCard(player=players[3], card=Card(Suit.BELL, 9))]
