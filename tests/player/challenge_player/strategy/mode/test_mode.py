import pytest

from schieber.card import Card
from schieber.suit import Suit
from schieber.player.challenge_player.strategy.mode.mode import Mode


@pytest.fixture
def mode():
    return Mode()

@pytest.mark.parametrize("cards, suits", [
    ([Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], [Suit.BELL, Suit.ACORN, Suit.SHIELD, Suit.ROSE]),
    ([Card(Suit.BELL, 14), Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     [Suit.BELL, Suit.ACORN, Suit.SHIELD, Suit.ROSE]),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     [Suit.BELL, Suit.SHIELD, Suit.ROSE]),
    ([Card(Suit.ACORN, 13), Card(Suit.ACORN, 12), Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7)],
     [Suit.ACORN, Suit.SHIELD]),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6)],
     [Suit.BELL]),
    ([Card(Suit.SHIELD, 7)],
     [Suit.SHIELD]),
    ([], []),
])
def test_available_suits(mode, cards, suits):
    available_suits = mode.available_suits(cards)
    assert set(available_suits) == set(suits)


@pytest.mark.parametrize("round_color, cards, have_to_serve", [
    (Suit.ROSE,
     [Suit.BELL, Suit.ACORN, Suit.SHIELD, Suit.ROSE],
     True),
    (Suit.ROSE,
     [Suit.BELL, Suit.ACORN],
     False),
    (Suit.SHIELD,
     [Suit.BELL],
     False),
    (Suit.BELL,
     [Suit.BELL, Suit.ACORN, Suit.SHIELD, Suit.ROSE],
     True),
    (Suit.ACORN,
     [Suit.BELL, Suit.SHIELD, Suit.ROSE],
     False),
    (None,
     [Suit.BELL, Suit.ACORN, Suit.SHIELD, Suit.ROSE],
     False),
])
def test_have_to_serve(mode, cards, round_color, have_to_serve):
    assert have_to_serve == mode.have_to_serve(cards, round_color)