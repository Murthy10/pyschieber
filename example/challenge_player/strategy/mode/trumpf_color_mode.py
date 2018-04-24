from example.challenge_player.strategy.mode.mode import Mode
from example.helpers.game_helper import *


class TrumpfColorMode(Mode):
    def __init__(self, suit):
        self.suit = suit

    def calculate_mode_score(self, cards, geschoben):
        score = 0

        cards_by_suit = split_cards_by_suit(cards)

        for suit, suit_cards in cards_by_suit:
            if suit == self.suit:
                for card in suit_cards:
                    if card == 11:
                        if geschoben:
                            score += 20
                        else:
                            score += 30
                    elif card == 9:
                        score += 15
                    elif card == 14:
                        score += 12
                    else:
                        score += 10
            else:
                sorted_cards = sorted(suit_cards, reverse=True)
                best_remaining_rank = 14

                for card in sorted_cards:
                    if card == best_remaining_rank:
                        best_remaining_rank -= 1
                        score += 4
                    else:
                        break

        return score
