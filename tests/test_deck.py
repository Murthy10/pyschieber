from pyschieber.deck import Deck


def test_deck_count():
    deck = Deck()
    assert len(deck.cards) == 36


def test_deck_unique():
    deck = Deck()
    deck_set = set(deck.cards)
    assert len(deck.cards) == len(deck_set)
