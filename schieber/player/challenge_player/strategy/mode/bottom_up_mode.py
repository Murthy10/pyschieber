from schieber.player.challenge_player.strategy.mode.uncolored_trumpf import UncoloredTrumpf
from schieber.helpers.game_helper import *
from schieber.trumpf import Trumpf
from schieber.card import from_string_to_card


class BottomUpMode(UncoloredTrumpf):
    def trumpf_name(self):
        return Trumpf.UNDE_UFE

    def calculate_mode_score(self, cards, geschoben):
        score = 0

        cards_by_suit = split_card_values_by_suit(cards)

        for suit, suit_cards in cards_by_suit:
            sorted_cards = self.sort_by_rank(suit_cards)
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

    def get_stich_card(self, cards_by_suit, card_counter, state):
        if len(state['table']) > 0:
            current_stich_color = from_string_to_card(state['table'][0]['card']).suit
            current_color_cards = [x[1] for x in cards_by_suit if x[0] == current_stich_color][0]
            cards = self.cards_beating_current_stich(current_color_cards, card_counter, state)
            stich_cards = []
            if len(state['table']) == 3:
                stich_cards.extend(cards)

            if len(cards) > 0 and len(state['table']) < 3:
                for card in cards:
                    stronger = self.stronger_cards_unknown(card, card_counter)
                    if len(stronger) != 0:
                        #may use has_cards_likelihood (plural)
                        if card_counter.has_cards_likelihood(card_counter.opponent_1_id, stronger, state) == 0:
                            if len(state['table']) > 0 or card_counter.has_cards_likelihood(card_counter.opponent_2_id, stronger, state) == 0:
                                stich_cards.append(card)
                    else:
                        stich_cards.append(card)

            if len(stich_cards) > 0:
                s_cards = self.sort_by_rank(stich_cards)
                for card in s_cards:
                    if card.value == 10:
                        return card
                return s_cards[0]
        return None

    def get_tossable_card(self, available_cards, card_counter, state):
        cards_by_suit = split_cards_by_suit(available_cards)
        eligible = self.available_suits(available_cards)
        round_color = None
        if len(state['table']) != 0:
            round_color = from_string_to_card(state['table'][0]['card']).suit

        if self.have_to_serve(eligible, round_color):
            weak_cards = self.sort_by_rank([x[1] for x in cards_by_suit if x[0] == round_color][0])
            beatable = card_counter.has_cards_likelihood(card_counter.opponent_1_id, self.cards_beating_current_stich(card_counter.unknown_cards(), card_counter, state), state) != 0
            if card_counter.round_leader(state) == card_counter.partner_id and (len(state['table']) == 3 or not beatable):
                for card in weak_cards:
                    if card.value == 10:
                        return card
            return weak_cards[len(weak_cards) - 1]

        else:
            suit_to_toss = self.get_suit_to_toss(available_cards, card_counter, state)
            weak_suit = None

            if suit_to_toss is not None:
                weak_suit = [x[1] for x in cards_by_suit if x[0] == suit_to_toss]
            else:
                unknown_by_suit = split_cards_by_suit(card_counter.unknown_cards())
                count = 10

                for suit, suit_cards in unknown_by_suit:
                    if len(suit_cards) < count:
                        if len([x[1] for x in cards_by_suit if x[0] == suit]) == 0:
                            continue
                        count = len(suit_cards)
                        weak_suit = [x[1] for x in cards_by_suit if x[0] == suit]

            weak_cards = self.sort_by_rank(weak_suit[0])
            if len(weak_cards) == 0:
                return None

            beatable = card_counter.has_cards_likelihood(card_counter.opponent_1_id, self.cards_beating_current_stich(card_counter.unknown_cards(), card_counter, state), state) != 0

            if card_counter.round_leader(state) == card_counter.partner_id and (len(state['table']) == 3 or not beatable):
                for card in weak_cards:
                    if card.value == 10:
                        return card
                return weak_cards[len(weak_cards) - 1]
            else:
                return weak_cards[len(weak_cards) - 1]



    def bock_distance(self, card, card_counter, state):
        stronger = card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.value < card.value)
        stronger = [x for x in stronger if x not in card_counter.get_hand()]
        table_cards = [from_string_to_card(x['card']) for x in state['table']]
        stronger = [x for x in stronger if x not in table_cards]
        return len(stronger)

    def stronger_cards_unknown(self, card, card_counter):
        return card_counter.filter_cards_of_same_suit(card, lambda x: x.value < card.value)

    def sort_by_rank(self, cards):
        return sorted(cards)
