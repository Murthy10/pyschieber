from pyschieber.suit import Suit


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return '<{0}:{1}>'.format(self.suit.value, self.value)


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            self.cards += [Card(suit=suit, value=i) for i in range(6, 15)]

    def __str__(self):
        return str([str(card) for card in self.cards])
