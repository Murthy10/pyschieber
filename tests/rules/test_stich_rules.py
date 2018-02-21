import pytest

from pyschieber.rules.stich_rules import stich_rules, card_allowed
from pyschieber.trumpf import Trumpf
from pyschieber.card import Card
from pyschieber.player.random_player import RandomPlayer
from pyschieber.stich import PlayedCard
from pyschieber.suit import Suit


@pytest.fixture(scope="module", autouse=True)
def players():
    return [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]


@pytest.fixture(scope="module", autouse=True)
def played_cards(players):
    return [PlayedCard(player=players[0], card=Card(Suit.BELL, 10)),
            PlayedCard(player=players[1], card=Card(Suit.ACORN, 6)),
            PlayedCard(player=players[2], card=Card(Suit.BELL, 13)),
            PlayedCard(player=players[3], card=Card(Suit.BELL, 9))]


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
