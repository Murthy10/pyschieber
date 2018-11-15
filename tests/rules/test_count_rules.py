import pytest

from schieber.deck import Deck
from schieber.trumpf import Trumpf
from schieber.rules.count_rules import count_stich


@pytest.mark.parametrize("trumpf", list(Trumpf)[:6])
def test_count_rules_with_last(trumpf):
    deck = Deck()
    points = count_stich(cards=deck.cards, trumpf=trumpf, last=True)
    assert points == 157


@pytest.mark.parametrize("trumpf", list(Trumpf)[:6])
def test_count_rules(trumpf):
    deck = Deck()
    points = count_stich(cards=deck.cards, trumpf=trumpf, last=False)
    assert points == 152
