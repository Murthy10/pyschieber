import random

from pyschieber.trumpf import Trumpf


class Player:
    def __init__(self):
        self.cards = []

    def set_card(self, card):
        self.cards.append(card)

    # TODO away from random
    def choose_trumpf(self):
        return random.choice(list(Trumpf))

    # TODO away from random
    def choose_card(self):
        return self.cards.pop()
