import random

import itertools

from pyschieber.trumpf import Trumpf


class Player:
    number_generator = itertools.count(0)

    def __init__(self):
        self.number = next(self.number_generator)
        self.cards = []

    def set_card(self, card):
        self.cards.append(card)

    # TODO away from random
    def choose_trumpf(self):
        return random.choice(list(Trumpf))

    # TODO away from random
    def choose_card(self):
        return self.cards.pop()

    def __str__(self):
        return '<Player:{}>'.format(self.number)
