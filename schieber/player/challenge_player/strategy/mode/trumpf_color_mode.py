from schieber.player.challenge_player.strategy.mode.mode import Mode
from schieber.helpers.game_helper import *
from schieber.trumpf import Trumpf
from schieber.card import from_string_to_card


class TrumpfColorMode(Mode):
    def __init__(self, suit):
        self.suit = suit

    def trumpf_name(self):
        return Trumpf[self.suit.name]

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

        if card.suit == self.suit:
            stronger_cards.extend(card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.get_trumpf_rank() > card.get_trumpf_rank()))
        else:
            for suit_cards in split_cards_by_suit(card_counter.remaining_cards(card_counter.dead_cards())):
                if suit_cards[0] == self.suit:
                    stronger_cards.extend(suit_cards[1])
            stronger_cards.extend(card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.value > card.value))

        return stronger_cards

    def stronger_cards_unknown(self, card, card_counter):
        stronger_cards = []

        if card.suit == self.suit:
            stronger_cards.extend(card_counter.filter_cards_of_same_suit(card, lambda x: x.get_trumpf_rank() > card.get_trumpf_rank()))
        else:
            for suit_cards in split_cards_by_suit(card_counter.unknown_cards()):
                if suit_cards[0]== self.suit:
                    stronger_cards.extend(suit_cards[1])

            stronger_cards.extend(card_counter.filter_cards_of_same_suit(card, lambda x: x.value > card.value))

        return stronger_cards

    def is_non_trumpf_bock(self, card, card_counter):
        return len(card_counter.filter_not_dead_cards_of_same_suit(card, lambda x: x.value > card.value)) == 0

    def get_passing_card(self, cards_by_suit, card_counter, state):
        for suit_cards in cards_by_suit:
            suit = suit_cards[0]
            cards = suit_cards[1]
            if len(cards) != 0:
                current_bock = self.get_current_bock(suit, card_counter)
                if current_bock is not None:
                    if (card_counter.has_card_likelihood(card_counter.partner_id, current_bock, state) == 1):
                        play = self.sort_by_rank(cards)
                        return play[len(play) - 1]

        possible_suits = card_counter.get_suits_by_strength(card_counter.partner_id)
        for suit in possible_suits:
            for suit_cards in cards_by_suit:
                if suit_cards[0] == suit:
                    cards = suit_cards[1]
                    if len(cards) != 0:
                        playable = self.sort_by_rank(cards)
                        return playable[len(playable) - 1]

        return None

    def want_stich(self, cards_by_suit, card_counter, player_acting_behind, state):
        we_can_make_all_stich = True
        we_lose_stich_if_we_dont = False

        for suit, suit_cards in cards_by_suit:
            for card in suit_cards:
                if not self.is_bock(card, card_counter) and \
                    card_counter.has_card_likelihood(card_counter.opponent_1_id, card, state) > 0 or \
                    card_counter.has_card_likelihood(card_counter.opponent_2_id, card, state) > 0:
                    we_can_make_all_stich = False

        color = from_string_to_card(state['table'][0]['card']).suit
        if color != self.suit:
            if not player_acting_behind:
                if len([x[1] for x in split_cards_by_suit(card_counter.unknown_cards()) if x[0] == color]) == 0 and \
                        len([x[1] for x in cards_by_suit if x[0] == color]) > 1:
                    we_lose_stich_if_we_dont = True
            elif card_counter.has_suit_likelihood(card_counter.opponent_1_id, color, state) == 1:
                if len([x[1] for x in split_cards_by_suit(card_counter.unknown_cards()) if x[0] == color]) == 1 and \
                        len([x[1] for x in cards_by_suit if x[0] == color]) > 1:
                    we_lose_stich_if_we_dont = True

        if card_counter.round_leader(state) == card_counter.partner_id and ( not player_acting_behind or \
                card_counter.has_cards_likelihood(card_counter.opponent_1_id, self.cards_beating_current_stich(card_counter.unknown_cards(), card_counter, state), state) == 0):
            partner_is_not_certain_to_win = False
        else:
            partner_is_not_certain_to_win = True

        return (we_can_make_all_stich or we_lose_stich_if_we_dont or partner_is_not_certain_to_win)

    def get_value_card(self, cards_by_suit, card_counter, state):
        if len(state['table']) == 0:
            opponents_beating_card = {}
            for suit, suit_cards in cards_by_suit:
                for card in suit_cards:
                    stronger = self.stronger_cards_remaining(card, card_counter)
                    if len(stronger) == 0:
                        opponents_beating_card[card] = 0
                    else:
                        d1 = card_counter.has_card_likelihood(card_counter.opponent_1_id, card, state)
                        d2 = card_counter.has_card_likelihood(card_counter.opponent_2_id, card, state)
                        opponents_beating_card[card] = (d1+((1-d1)*d2))

            return min(opponents_beating_card, key=opponents_beating_card.get)
        return None

    def get_tossable_card(self, available_cards, card_counter, state):
        cards_by_suit = split_cards_by_suit(available_cards)
        eligible = self.available_suits(available_cards)
        round_color = None
        if len(state['table']) != 0:
            round_color = from_string_to_card(state['table'][0]['card']).suit

        if len(state['table']) > 0 and self.have_to_serve(eligible, round_color) and (round_color != self.suit or not self.has_only_jack_of_trumpf(available_cards)):
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

    def get_suit_to_toss(self, available_cards, card_counter, state):
        cards_by_suit = split_cards_by_suit(available_cards)

        tossed_suits = card_counter.tossed_suits(card_counter.my_id)
        for suit, suit_cards in cards_by_suit:
            if suit in tossed_suits:
                for card in suit_cards:
                    if self.bock_distance(card, card_counter, state) != 0:
                        return suit

        bd_suits = []
        for suit, suit_cards in cards_by_suit:
            if suit == self.suit:
                continue
            if suit not in tossed_suits:
                bock_distances = []
                for card in suit_cards:
                    bock_distances.append(self.bock_distance(card, card_counter, state))
                if len(bock_distances) == 0:
                    bd_suits.append((suit, 0))
                else:
                    bd_suits.append((suit, min(bock_distances)))

        if len(bd_suits) == 0:
            return None
        else:
            return max(bd_suits,key=lambda item:item[1])[0]

    def get_stich_card(self, cards_by_suit, card_counter, state):
        if len(state['table']) > 0:
            current_stich_color = from_string_to_card(state['table'][0]['card']).suit
            tmp_list = [x[1] for x in cards_by_suit if (x[0] == current_stich_color or x[0] == self.suit)]
            current_color_cards = [item for sublist in tmp_list for item in sublist]
            cards = self.cards_beating_current_stich(current_color_cards, card_counter, state)
            stich_cards = []
            if len(state['table']) == 3:
                stich_cards.extend(cards)

            if len(cards) > 0 and len(state['table']) < 3:
                for card in cards:
                    stronger = self.stronger_cards_unknown(card, card_counter)
                    if len(stronger) != 0:
                        # may use has_cards_likelihood (plural)
                        if card_counter.has_cards_likelihood(card_counter.opponent_1_id, stronger, state) == 0:
                            if len(state['table']) > 0 or card_counter.has_cards_likelihood(
                                    card_counter.opponent_2_id, stronger, state) == 0:
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

    def sort_by_rank(self, cards):
        return sorted(cards, key=lambda card: card.get_score(self.trumpf_name()), reverse=True)

    def has_only_jack_of_trumpf(self, player_cards):
        has_only_jack = False
        for card in player_cards:
            if card.suit == self.suit and card.value != 11:
                return False

            if card.suit == self.suit and card.value == 11:
                has_only_jack = True
        return has_only_jack

    def get_card_to_play(self, available_cards, card_counter, state, role):
        current_position = len(state['table'])

        cards_by_suit = split_cards_by_suit(available_cards)
        sorted_trumpf_cards = self.sort_by_rank([x[1] for x in cards_by_suit if x[0] == self.suit][0])

        non_trumpf_bocks = []
        bocks = []
        for card in available_cards:
            if self.is_non_trumpf_bock(card, card_counter) and card.suit != self.suit:
                non_trumpf_bocks.append(card)

            if self.is_bock(card ,card_counter):
                bocks.append(card)

        opponents_out_of_trumpf = card_counter.has_suit_likelihood(card_counter.opponent_1_id, self.suit, state) == 0 \
                and card_counter.has_suit_likelihood(card_counter.opponent_2_id, self.suit, state) == 0

        if current_position == 0:
            if role == 'Trumpf' or role == 'Off':
                pulling_trumpfs = (not opponents_out_of_trumpf and len(sorted_trumpf_cards) > 0)
                if pulling_trumpfs:
                    return sorted_trumpf_cards[0]
                elif len(non_trumpf_bocks) > 0 and opponents_out_of_trumpf:
                    return non_trumpf_bocks[0]
                else:
                    if not opponents_out_of_trumpf and len(sorted_trumpf_cards) == 0:
                        return self.get_tossable_card(available_cards, card_counter, state)

                    if not card_counter.had_stich_previously(card_counter.partner_id):
                        return self.get_passing_card(cards_by_suit, card_counter, state)
                    else:
                        return self.get_value_card(cards_by_suit, card_counter, state)
            elif role == 'Partner':
                if not card_counter.had_stich_previously(card_counter.partner_id):
                    sorted_trumpf_cards = list(filter(lambda card: card.value != 11, sorted_trumpf_cards))

                    if len(sorted_trumpf_cards) != 0:
                        return sorted_trumpf_cards[0]
                    else:
                        return self.get_passing_card(cards_by_suit, card_counter, state)
                else:
                    pulling_trumpfs = not opponents_out_of_trumpf and len(sorted_trumpf_cards) > 0
                    if pulling_trumpfs:
                        return sorted_trumpf_cards[0]
                    elif len(non_trumpf_bocks) > 0:
                        return non_trumpf_bocks[0]
                    else:
                        self.get_value_card(cards_by_suit, card_counter, state)

        elif current_position == 1:
            stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
            if stich_card is None:
                return self.get_tossable_card(available_cards, card_counter, state)
            return stich_card

        elif current_position == 2:
            if role == 'Trumpf':
                if not card_counter.had_stich_previously(card_counter.my_id):
                    ret = self.get_stich_card(cards_by_suit, card_counter, state)
                    if ret is not None:
                        return ret
                    else:
                        return self.get_tossable_card(available_cards, card_counter, state)
                else:
                    if not self.want_stich(cards_by_suit, card_counter, True, state):
                        return self.get_tossable_card(available_cards, card_counter, state)
                    else:
                        return self.get_stich_card(cards_by_suit, card_counter, state)

            elif role == 'Off':
                if self.want_stich(cards_by_suit, card_counter, True, state):
                    stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
                    if stich_card is not None:
                        return stich_card
                    return self.get_tossable_card(available_cards, card_counter, state)

            elif role == 'Partner':
                if card_counter.current_round() == 0 and card_counter.round_leader(state) == card_counter.partner_id:
                    a2card = card_counter.current_stich[card_counter.partner_id]
                    if self.is_nth_nut(1, a2card, card_counter):
                        round_color = from_string_to_card(state['table'][0]['card']).suit
                        for card in [x[1] for x in cards_by_suit if x[0] == round_color][0]:
                            if self.is_nth_nut(2, card, card_counter):
                                play_2nd_nut = True
                                for card2 in [x[1] for x in cards_by_suit if x[0] == round_color][0]:
                                    if self.is_nth_nut(3, card2, card_counter):
                                        play_2nd_nut = False

                                if play_2nd_nut:
                                    return card

                if self.want_stich(cards_by_suit, card_counter, True, state):
                    stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
                    if stich_card is not None:
                        return stich_card

                return self.get_tossable_card(available_cards, card_counter, state)

        elif current_position == 3:
            if self.want_stich(cards_by_suit, card_counter, False, state):
                stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
                if stich_card is not None:
                    return stich_card

            return self.get_tossable_card(available_cards, card_counter, state)

        return None
