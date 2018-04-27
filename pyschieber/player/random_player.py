import random

from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf


class RandomPlayer(BasePlayer):
    def choose_trumpf(self, geschoben):
        return move(choices=list(Trumpf))

    def choose_card(self, state=None):
        cards = self.allowed_cards(state=state)
        return move(choices=cards)


def move(choices):
    allowed = False
    while not allowed:
        choice = random.choice(choices)
        allowed = yield choice
        if allowed:
            yield None
