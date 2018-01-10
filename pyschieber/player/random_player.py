import random

from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf


class RandomPlayer(BasePlayer):
    def choose_trumpf(self):
        return random.choice(list(Trumpf))

    def choose_card(self):
        allowed = False
        while not allowed:
            card = random.choice(self.cards)
            allowed = yield card
            if allowed:
                yield None