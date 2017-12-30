from random import shuffle

from pyschieber.deck import Deck


class Game:
    def __init__(self):
        self.trumpf = ''
        self.deck = Deck()
        shuffle(self.deck)

