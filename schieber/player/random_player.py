import random

from schieber.player.base_player import BasePlayer
from schieber.trumpf import Trumpf


class RandomPlayer(BasePlayer):
    def choose_trumpf(self, geschoben):
        return self.move(choices=[Trumpf.OBE_ABE])  # always choose obe abe for now
        # return self.move(choices=list(Trumpf))

    def choose_card(self, state=None):
        cards = self.allowed_cards(state=state)
        return self.move(choices=cards)

    def move(self, choices):
        allowed = False
        while not allowed:
            random.seed(self.seed)
            choice = random.choice(choices)
            allowed = yield choice
            if allowed:
                yield None
