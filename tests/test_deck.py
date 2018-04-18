from pyschieber.card import Card
from pyschieber.deck import Deck


def test_deck_count():
    deck = Deck()
    assert len(deck.cards) == 36


def test_deck_unique():
    deck = Deck()
    deck_set = set(deck.cards)
    assert len(deck.cards) == len(deck_set)


def test_deck_max():
    deck = Deck()
    card = max(deck.cards)
    assert card.value == 14


def test_deck_min():
    deck = Deck()
    card = min(deck.cards)
    assert card.value == 6


def test_deck_sort():
    deck = Deck()
    sorted(deck.cards)
    assert Card.names[deck.cards[0].value] == '6'
    assert Card.names[deck.cards[-1].value] == 'Ass'
