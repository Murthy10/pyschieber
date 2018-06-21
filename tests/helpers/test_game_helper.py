from pyschieber.suit import Suit

from build.lib.pyschieber.card import Card
from pyschieber.deck import Deck

from pyschieber.helpers.game_helper import split_card_values_by_suit, split_cards_by_suit


def test_split_card_values_by_suit():
    deck = Deck()
    suit_card_values = split_card_values_by_suit(deck.cards)
    assert len(suit_card_values) == 4
    assert 6 in suit_card_values[0][1]


def test_split_cards_by_suit():
    deck = Deck()
    suit_cards = split_cards_by_suit(deck.cards)
    assert len(suit_cards) == 4
    assert Card(suit=Suit.ROSE, value=6) in suit_cards[0][1]
