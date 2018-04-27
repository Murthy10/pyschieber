from example.challenge_player.strategy.mode.uncolored_trumpf import UncoloredTrumpf
from example.helpers.game_helper import *
from pyschieber.trumpf import Trumpf


class BottomUpMode(UncoloredTrumpf):
    def trumpf_name(self):
        return Trumpf.UNDE_UFE

    def calculate_mode_score(self, cards, geschoben):
        score = 0

        cards_by_suit = split_card_values_by_suit(cards)

        for suit, suit_cards in cards_by_suit:
            sorted_cards = sorted(suit_cards)
            best_remaining_rank = 6

            for card in sorted_cards:
                if card == best_remaining_rank:
                    best_remaining_rank += 1
                    score += 13
                else:
                    if best_remaining_rank > 8:
                        score += 10

        return score

    def stronger_cards_remaining(self, card, card_counter):
        return card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.value < card.value)
