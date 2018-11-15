from schieber.suit import Suit
from schieber.card import Card


class Deck:
    def __init__(self):
        """
        Initializes a deck of cards used for Jassen (from 6 to 10, Jack, Queen, King and Ace; each card in 4 suits)
        """
        self.cards = []
        for suit in Suit:
            self.cards += [Card(suit=suit, value=i) for i in range(6, 15)]

    def __str__(self):
        return str([str(card) for card in self.cards])
