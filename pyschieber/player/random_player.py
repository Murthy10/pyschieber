import random

from pyschieber.card import from_string_to_card
from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf
from pyschieber.rules.stich_rules import card_allowed


class RandomPlayer(BasePlayer):
    def choose_trumpf(self, geschoben):
        return move(choices=list(Trumpf))

    def choose_card(self, state=None):
        table_cards = [from_string_to_card(entry['card']) for entry in state['table']]
        trumpf = Trumpf[state['trumpf']]
        return move(choices=self.allowed_cards(table_cards=table_cards, trumpf=trumpf))

    def allowed_cards(self, table_cards, trumpf):
        cards = []
        if len(table_cards) > 0:
            for card in self.cards:
                if card_allowed(table_cards[0], card, self.cards, trumpf):
                    cards.append(card)
        else:
            cards = self.cards
        return cards


def move(choices):
    allowed = False
    while not allowed:
        choice = random.choice(choices)
        allowed = yield choice
        if allowed:
            yield None
