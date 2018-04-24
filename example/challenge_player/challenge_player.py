import random

from pyschieber.player.base_player import BasePlayer
from example.challenge_player.strategy.jass_strategy import JassStrategy


class ChallengePlayer(BasePlayer):
    def __init__(self, name='unknown'):
        BasePlayer.__init__(self, name)
        self.strategy = JassStrategy()

    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            trumpf = self.strategy.chose_trumpf(self.cards, geschoben)
            allowed = yield trumpf
            if allowed:
                yield None

    def choose_card(self, state=None):
        cards = self.allowed_cards(state=state)
        return move(choices=cards)

    def stich_over(self, state=None):
        print(state)


def move(choices):
    allowed = False
    while not allowed:
        choice = random.choice(choices)
        allowed = yield choice
        if allowed:
            yield None
