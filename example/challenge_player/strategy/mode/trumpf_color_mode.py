from example.challenge_player.strategy.mode.mode import Mode
from example.helpers.game_helper import *
from pyschieber.trumpf import Trumpf


class TrumpfColorMode(Mode):
    def __init__(self, suit):
        self.suit = suit

    def trumpf_name(self):
        return Trumpf[self.suit]

    def calculate_mode_score(self, cards, geschoben):
        score = 0

        cards_by_suit = split_card_values_by_suit(cards)

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

    def stronger_cards_remaining(self, card, card_counter):
        stronger_cards = []

        if card.suit.name == self.suit:
            stronger_cards.extend(card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.get_trumpf_rank() > card.get_trumpf_rank()))
        else:
            for suit_cards in split_cards_by_suit(card_counter.remaining_cards(card_counter.dead_cards())):
                if suit_cards[0].name == self.suit:
                    stronger_cards.extend(suit_cards[1])
            stronger_cards.extend(card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.value > card.value))

        return stronger_cards

    def is_trumpf(self, card):
        return card.suit == self.suit
