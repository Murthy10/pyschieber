from pyschieber.suit import Suit
from pyschieber.card import Card


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            self.cards += [Card(suit=suit, value=i) for i in range(6, 15)]

    def __str__(self):
        return str([str(card) for card in self.cards])
