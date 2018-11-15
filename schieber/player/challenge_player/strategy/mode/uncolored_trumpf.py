from schieber.player.challenge_player.strategy.mode.mode import Mode
from schieber.helpers.game_helper import *
from schieber.card import from_string_to_card


class UncoloredTrumpf(Mode):
    def get_card_to_play(self, available_cards, card_counter, state, role):
        current_position = len(state['table'])
        cards_by_suit = split_cards_by_suit(available_cards)

        bocks = list(filter(lambda x: self.is_bock(x, card_counter), available_cards))
        beating_current_stich = self.cards_beating_current_stich(available_cards, card_counter, state)

        if current_position == 0:
            if len(bocks) > 0:
                return bocks[0]
            elif not card_counter.had_stich_previously(card_counter.partner_id):
                return self.get_passing_card(cards_by_suit, card_counter, state)
            else:
                return self.get_value_card(cards_by_suit, card_counter, state)
        elif current_position == 1:
            stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
            if stich_card is None:
                return self.get_tossable_card(available_cards, card_counter, state)
            return stich_card
        elif current_position == 2:
            if role == 'Trumpf':
                if not card_counter.had_stich_previously(card_counter.my_id):
                    stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
                    if stich_card is None:
                        return self.get_tossable_card(available_cards, card_counter, state)
                    return stich_card
                else:
                    if not self.want_stich(cards_by_suit, card_counter, True, state):
                        return self.get_tossable_card(available_cards, card_counter, state)
                    else:
                        stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
                        if stich_card is None:
                            return self.get_tossable_card(available_cards, card_counter, state)
                        return stich_card

            elif role == 'Off':
                if self.want_stich(cards_by_suit, card_counter, True, state):
                    stich_card = self.get_stich_card(cards_by_suit, card_counter, state)
                    if stich_card is None:
                        return self.get_tossable_card(available_cards, card_counter, state)
                    return stich_card

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

    def get_passing_card(self, cards_by_suit, card_counter, state):
        for suit_cards in cards_by_suit:
            suit = suit_cards[0]
            cards = suit_cards[1]
            if len(cards) != 0:
                current_bock = self.get_current_bock(suit, card_counter)
                if current_bock is None:
                    continue

                if (card_counter.has_card_likelihood(card_counter.partner_id, current_bock, state) == 1) or \
                    (card_counter.has_suit_likelihood(card_counter.opponent_1_id, suit, state) == 0 and card_counter.has_suit_likelihood(card_counter.opponent_2_id, suit, state) == 0):
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



    def sort_by_rank(self, cards): pass

