from example.helpers.game_helper import *

class Mode:
    def is_bock(self, c, c_counter):
        return len(self.stronger_cards_remaining(c, c_counter)) == 0

    def get_current_bock(self, suit, card_counter):
        remaining = []
        remaining.extend(card_counter.remaining_by_suit(suit))
        for suit_cards in split_cards_by_suit(card_counter.get_hand()):
            if suit_cards[0] == suit:
                remaining.extend(suit_cards[1])
        remaining.extend(card_counter.current_stich.values())

        if len(remaining) == 0:
            return None

        trumpf = self.trumpf_name()
        remaining_sorted = sorted(remaining, key=lambda card: card.get_score(trumpf))
        return remaining_sorted[0]

    def create_rank_comparator(self, card1, card2):
        pass

    def stronger_cards_remaining(self, card, card_counter):
        return []
