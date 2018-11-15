from schieber.player.challenge_player.strategy.mode.trumpf_color_mode import *
from schieber.player.challenge_player.strategy.mode.top_down_mode import *
from schieber.player.challenge_player.strategy.mode.bottom_up_mode import *
from schieber.player.challenge_player.strategy.flags.doesnt_habe_card_flag import DoesntHaveCardFlag
from schieber.player.challenge_player.strategy.flags.previously_had_stich_flag import PreviouslyHadStichFlag
from schieber.player.challenge_player.strategy.flags.falied_to_serve_suit_flag import FailedToServeSuitFlag
from schieber.player.challenge_player.strategy.flags.suit_verworfen_flag import SuitVerworfenFlag
from schieber.deck import Deck
from schieber.card import from_string_to_card
from schieber.rules.stich_rules import stich_rules
from schieber.trumpf import get_trumpf
from schieber.stich import PlayedCard
from schieber.suit import Suit
from math import floor


class CardCounter:
    def __init__(self, me):
        self.played_cards = [[],[],[],[]]
        self.flags = [[],[],[],[]]
        self.played_count = 0
        self.current_stich = {}
        self.my_id = me.id
        self.me = me
        self.partner_id = (self.my_id + 2) % 4
        self.opponent_1_id = (self.my_id+1)%4
        self.opponent_2_id = (self.my_id+3)%4

    def card_played(self, player_id, card, state):
        self.played_cards[player_id].append(card)
        self.played_count += 1
        self.current_stich[player_id] = card

        self.update_flags(player_id, card, state)

        if self.played_count % 4 == 0:
            self.current_stich = {}

    def current_round(self):
        return floor(self.played_count/4)

    def update_flags(self, player_id, card, state):
        current_stich_color = None
        if len(state['table']) > 0:
            current_stich_color = from_string_to_card(state['table'][0]['card']).suit

        mode = get_mode(state['trumpf'])

        if len(self.current_stich) == 4:
            if player_id == self.partner_id and self.round_leader(state) != self.my_id and self.round_leader(state) != self.partner_id:
                #neither of us wins, A2 played last card -> A2 doesn't have anything beating current stich
                for stronger_card in mode.stronger_cards_remaining(self.current_stich[self.round_leader(state)], self):
                    self.flags[player_id].append(DoesntHaveCardFlag(stronger_card))

        if len(self.current_stich) == 1:
            if mode.trumpf_name().name not in [x.name for x in Suit]:
                if player_id == self.partner_id and not mode.is_bock(card, self):
                    for suit in Suit:
                        self.flags[player_id].append(DoesntHaveCardFlag(mode.get_current_bock(suit, self)))

            if not self.had_stich_previously(player_id):
                if not (self.current_round() == 0 and state['geschoben'] and (mode.trumpf_name().name in [x.name for x in Suit])):
                    self.flags[player_id].append(PreviouslyHadStichFlag())

            if self.round_leader(state) == self.partner_id:
                if mode.trumpf_name().name in [x.name for x in Suit]:
                    if self.current_round() == 0:
                        if state['geschoben']:
                            if card.suit == mode.trumpf_name().name:
                                for stronger_card in mode.stronger_cards_remaining(card, self):
                                    if stronger_card.value != 11:
                                        self.flags[player_id].append(DoesntHaveCardFlag(stronger_card))

                    if card == mode.get_current_bock(card.suit, self) and card.suit != mode.trumpf_name().name:
                        for suit_cards in split_cards_by_suit(self.unknown_cards()):
                            if suit_cards[0].name == mode.trumpf_name().name:
                                for trumpf_card in suit_cards[1]:
                                    self.flags[(self.my_id + 1)%4].append(DoesntHaveCardFlag(trumpf_card))
                                    self.flags[(self.my_id + 3)%4].append(DoesntHaveCardFlag(trumpf_card))

        if len(self.current_stich) > 1:
            if card.suit != current_stich_color:
                if (mode.trumpf_name().name in [x.name for x in Suit] and card.suit != mode.trumpf_name().name) or mode.trumpf_name().name not in [x.name for x in Suit]:
                    self.flags[player_id].append(FailedToServeSuitFlag(current_stich_color))
                    self.flags[player_id].append(SuitVerworfenFlag(card.suit))

    def round_leader(self, state):
        if len(self.get_table_cards()) == 0:
            return None
        return stich_rules[get_trumpf(state['trumpf'])](played_cards=self.get_table_cards()).player

    def get_hand(self):
        return self.me.cards

    def get_table_cards(self):
        cards_on_table = []
        for player_id in self.current_stich:
            cards_on_table.append(PlayedCard(player=player_id, card=self.current_stich[player_id]))
        return cards_on_table

    def cards_played(self):
        played = []
        for x in range(0,4):
            played.extend(self.played_cards[x])
        return played

    def seen_cards(self):
        seen = []
        seen.extend(self.cards_played())
        seen.extend(self.me.cards)
        return seen

    def remaining_cards(self, gone):
        d = Deck()
        return [x for x in d.cards if x not in gone]

    def remaining_by_suit(self, suit):
        return [x for x in self.unknown_cards() if x.suit == suit]

    def unknown_cards(self):
        return self.remaining_cards(self.seen_cards())

    def dead_cards(self):
        dead = []
        current_round = int(self.played_count/4)
        for player_id in range(0, 4):
            dead.extend(self.played_cards[player_id][0:current_round])
        return dead

    def filter_cards_of_same_suit(self, card, predicate):
        unknown_of_same_suit = list(filter(lambda x: x.suit == card.suit, self.unknown_cards()))
        return list(filter(predicate, unknown_of_same_suit))

    def filter_not_dead_cards_of_same_suit(self, card, predicate):
        remaining_cards = self.remaining_cards(self.dead_cards())
        remaining_of_same_suit = list(filter(lambda x: (x.suit == card.suit), remaining_cards))
        return list(filter(predicate, remaining_of_same_suit))

    def had_stich_previously(self, p_id):
        for flag in self.flags[p_id]:
            if isinstance(flag, PreviouslyHadStichFlag):
                return True
        return False

    def has_suit_likelihood(self, player_id, suit, state):
        return self.has_cards_likelihood(player_id, self.remaining_by_suit(suit), state)

    def has_cards_likelihood(self, player_id, cards, state):
        likelihood = 1
        for card in cards:
            likelihood = likelihood * (1 - self.has_card_likelihood(player_id, card, state))
        return 1 - likelihood

    def has_card_likelihood(self, player_id, card, state):
        if card in self.get_hand() or card in [x[0] for x in self.played_cards if len(x) != 0]:
            return 0

        if state['trumpf'] == card.suit and card.value == 11:
            return 1/3

        for flag in self.flags[player_id]:
            if isinstance(flag, FailedToServeSuitFlag):
                if card.suit == flag.color:
                    return 0
            elif isinstance(flag, DoesntHaveCardFlag):
                if flag.card == card:
                    return 0

        potential_holders = 3
        for p_id in range(0, 4):
            if p_id != self.my_id and p_id != player_id:
                for flag in self.flags[p_id]:
                    if isinstance(flag, FailedToServeSuitFlag):
                        if card.suit == flag.color:
                            potential_holders -= 1
                            break
                        elif isinstance(flag, DoesntHaveCardFlag):
                            if card == flag.card:
                                potential_holders -= 1
                                break

        if potential_holders > 0:
            return 1 / potential_holders
        else:
            return 0

    def get_suits_by_strength(self, player_id):
        flags_of_player = self.flags[player_id]
        weak = []

        for flag in flags_of_player:
            if isinstance(flag, FailedToServeSuitFlag):
                if flag.color not in weak:
                    weak.append(flag.color)

        for flag in flags_of_player:
            if isinstance(flag, SuitVerworfenFlag):
                if flag.color not in weak:
                    weak.append(flag.color)

        for color in Suit:
            if color.name not in weak:
                weak.append(color.name)

        return list(reversed(weak))

    def tossed_suits(self, player_id):
        return list(map(lambda y: y.color, filter(lambda x: isinstance(x, SuitVerworfenFlag), self.flags[player_id])))

def get_mode(trumpf):
    return {
        'OBE_ABE': TopDownMode(),
        'UNDE_UFE': BottomUpMode(),
        'ROSE': TrumpfColorMode(Suit['ROSE']),
        'BELL': TrumpfColorMode(Suit['BELL']),
        'ACORN': TrumpfColorMode(Suit['ACORN']),
        'SHIELD': TrumpfColorMode(Suit['SHIELD']),
    }[trumpf]
