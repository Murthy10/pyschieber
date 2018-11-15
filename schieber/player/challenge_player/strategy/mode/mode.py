from schieber.helpers.game_helper import *
from schieber.card import from_string_to_card
from schieber.trumpf import get_trumpf

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

    def cards_beating_current_stich(self, available_cards, card_counter, state):
        curr_pos = len(state['table'])
        if curr_pos != 0:
            for card_played in state['table']:
                if card_played['player_id'] == card_counter.round_leader(state):
                    current_stich_winner = from_string_to_card(card_played['card'])
                    break
            cards_beating_winner = self.stronger_cards_remaining(current_stich_winner, card_counter)
            beating_cards = []
            for card in available_cards:
                if card in cards_beating_winner:
                    beating_cards.append(card)
        else:
            beating_cards = available_cards

        return sorted(beating_cards, key=lambda card: card.get_score(get_trumpf(state['trumpf'])))

    def bock_distance(self, card, card_counter, state):
        stronger = card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.value > card.value)
        stronger = [x for x in stronger if x not in card_counter.get_hand()]
        table_cards = [from_string_to_card(x['card']) for x in state['table']]
        stronger = [x for x in stronger if x not in table_cards]
        return len(stronger)

    def create_rank_comparator(self, card1, card2):
        pass

    def stronger_cards_remaining(self, card, card_counter):
        return []

    def available_suits(self, available_cards):
        cards_per_suit = split_cards_by_suit(available_cards)
        return [x[0] for x in cards_per_suit if len(x[1]) > 0]

    def is_nth_nut(self, n, card, card_counter):
        return len(self.stronger_cards_remaining(card, card_counter)) == 0

    def have_to_serve(self, available_suits, round_color):
        return round_color is not None and round_color in available_suits