import pytest

from pyschieber.deck import Deck


def test_deck_count():
    deck = Deck()
    print(deck)
    assert len(deck.cards) == 36
