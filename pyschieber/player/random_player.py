import random

from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf


class RandomPlayer(BasePlayer):
    def choose_trumpf(self):
        return random.choice(list(Trumpf))

    def choose_card(self):
        return self.cards.pop()
