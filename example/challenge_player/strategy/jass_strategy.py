from example.challenge_player.strategy.mode.trumpf_color_mode import *
from example.challenge_player.strategy.mode.top_down_mode import *
from example.challenge_player.strategy.mode.bottom_up_mode import *
from example.challenge_player.strategy.card_counter import CardCounter
from pyschieber.trumpf import Trumpf


class JassStrategy:
    def __init__(self, player):
        self.me = player
        self.card_counter = CardCounter(player)

    def chose_trumpf(self, cards, geschoben):
        scores = []

        if not geschoben:
            scores.append((Trumpf.SCHIEBEN, 54))

        tdm = TopDownMode()
        scores.append((Trumpf.OBE_ABE, tdm.calculate_mode_score(cards, geschoben)))

        bum = BottomUpMode()
        scores.append((Trumpf.UNDE_UFE, bum.calculate_mode_score(cards, geschoben)))

        for suit in Suit:
            tcm = TrumpfColorMode(suit)
            scores.append((Trumpf[suit.name], tcm.calculate_mode_score(cards, geschoben)))

        return max(scores, key=lambda x: x[1])[0]

    def move_made(self, player_id, card, state):
        self.card_counter.card_played(player_id, card, state)
