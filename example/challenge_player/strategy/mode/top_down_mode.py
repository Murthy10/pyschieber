from example.challenge_player.strategy.mode.uncolored_trumpf import UncoloredTrumpf
from example.helpers.game_helper import *


class TopDownMode(UncoloredTrumpf):
    def calculate_mode_score(self, cards, geschoben):
        score = 0

        cards_by_suit = split_cards_by_suit(cards)

        for suit, suit_cards in cards_by_suit:
            sorted_cards = sorted(suit_cards, reverse=True)
            best_remaining_rank = 14

            for card in sorted_cards:
                if card == best_remaining_rank:
                    best_remaining_rank -= 1
                    score += 13
                else:
                    if best_remaining_rank < 12:
                        score += 10

        return score
