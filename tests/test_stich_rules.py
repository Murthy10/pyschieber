import pytest

from pyschieber.card import Card
from pyschieber.rules.stich_rules import stich_rules, card_allowed
from pyschieber.suit import Suit
from pyschieber.trumpf import Trumpf


@pytest.mark.parametrize("trumpf, index,", [
    (Trumpf.OBE_ABE, 2),
    (Trumpf.UNDE_UFE, 3),
    (Trumpf.BELL, 3),
    (Trumpf.ACORN, 1),
])
def test_stich(trumpf, index, players, played_cards):
    stich = stich_rules[trumpf](played_cards=played_cards)
    assert stich.player is players[index]


@pytest.mark.parametrize("first_card, chosen_card, hand_cards, trumpf, result", [
    (Card(Suit.BELL, 12), Card(Suit.BELL, 12), [Card(Suit.BELL, 12), Card(Suit.BELL, 11)], Trumpf.BELL, True),
    (None, Card(Suit.BELL, 12), [Card(Suit.BELL, 12), Card(Suit.BELL, 11)], Trumpf.BELL, True),
    (Card(Suit.BELL, 12), Card(Suit.BELL, 12), [Card(Suit.BELL, 12), Card(Suit.BELL, 11)], Trumpf.OBE_ABE, True),
    (Card(Suit.ACORN, 12), Card(Suit.BELL, 12), [Card(Suit.BELL, 12), Card(Suit.BELL, 11)], Trumpf.OBE_ABE, True),
    (Card(Suit.ACORN, 12), Card(Suit.BELL, 12), [Card(Suit.ACORN, 11), Card(Suit.BELL, 12), Card(Suit.BELL, 11)],
     Trumpf.OBE_ABE, False),
    (Card(Suit.ACORN, 11), Card(Suit.BELL, 12), [Card(Suit.ACORN, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 12)],
     Trumpf.ACORN, True),
])
def test_card_allowed(first_card, chosen_card, hand_cards, trumpf, result):
    assert card_allowed(first_card, chosen_card, hand_cards, trumpf) == result
