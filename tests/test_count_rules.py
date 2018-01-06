import pytest

from pyschieber.deck import Deck
from pyschieber.trumpf import Trumpf
from pyschieber.rules.count_rules import count_stich


@pytest.mark.parametrize("trumpf", list(Trumpf))
def test_count_rules(trumpf):
    deck = Deck()
    points = count_stich(cards=deck.cards, trumpf=trumpf)
    assert points == 152
