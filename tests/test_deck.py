from pyschieber.deck import Deck


def test_deck_count():
    deck = Deck()
    assert len(deck.cards) == 36
