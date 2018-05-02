import random

from pyschieber.player.base_player import BasePlayer
from pyschieber.player.challenge_player.strategy.jass_strategy import JassStrategy
from pyschieber.card import Card


class ChallengePlayer(BasePlayer):
    def __init__(self, name='unknown'):
        BasePlayer.__init__(self, name)

    def game_started(self):
        self.strategy = JassStrategy(self)

    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            trumpf = self.strategy.chose_trumpf(self.cards, geschoben)
            allowed = yield trumpf
            if allowed:
                yield None

    def choose_card(self, state=None):
        if len(state['stiche']) == 0:
            if len(state['table']) == 0:
                if state['geschoben']:
                    self.role = 'Partner'
                else:
                    self.role = 'Trumpf'

            elif len(state['table']) == 2:
                if state['geschoben']:
                    self.role = 'Trumpf'
                else:
                    self.role = 'Partner'

            else:
                self.role = 'Off'

        cards = self.allowed_cards(state=state)

        allowed = False
        while not allowed:
            card = self.strategy.choose_card(cards, state, self.role)
            if not isinstance(card, Card):
                card = random.choice(cards)
            allowed = yield card
            if allowed:
                yield None

    def move_made(self, player_id, card, state):
        self.strategy.move_made(player_id, card, state)
