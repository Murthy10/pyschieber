from example.challenge_player.strategy.mode.trumpf_color_mode import *
from example.challenge_player.strategy.mode.top_down_mode import *
from example.challenge_player.strategy.mode.bottom_up_mode import *
from example.challenge_player.strategy.flags.doesnt_habe_card_flag import DoesntHaveCardFlag
from example.challenge_player.strategy.flags.previously_had_stich_flag import PreviouslyHadStichFlag
from example.challenge_player.strategy.flags.falied_to_serve_suit_flag import FailedToServeSuitFlag
from example.challenge_player.strategy.flags.suit_verworfen_flag import SuitVerworfenFlag
from pyschieber.deck import Deck
from pyschieber.card import from_string_to_card
from pyschieber.rules.stich_rules import stich_rules
from pyschieber.trumpf import Trumpf
from pyschieber.stich import PlayedCard
from pyschieber.suit import Suit


class CardCounter:
    def __init__(self, me):
        self.played_cards = [[],[],[],[]]
        self.flags = [[],[],[],[]]
        self.played_count = 0
        self.current_stich = {}
        self.stiche = []
        self.my_id = me.id
        self.me = me
        self.partner_id = (self.my_id + 2) % 4

    def card_played(self, player_id, card, state):
        self.played_cards[player_id].append(card)
        self.played_count += 1
        self.current_stich[player_id] = card

        self.update_flags(player_id, card, state)

        if self.played_count % 4 == 0:
            self.current_stich = {}

    def current_round(self):
        return self.played_count/4

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

    def filter_not_dead_cards_of_same_suit(self, card, predicate):
        remaining_of_same_suit = list(filter(lambda x: x.suit == card.suit, self.remaining_cards(self.dead_cards())))
        return list(filter(predicate, remaining_of_same_suit))

    def had_stich_previously(self, p_id):
        for flag in self.flags[p_id]:
            if isinstance(flag, PreviouslyHadStichFlag):
                return True
        return False




def get_mode(trumpf):
    return {
        'OBE_ABE': TopDownMode(),
        'UNDE_UFE': BottomUpMode(),
        'ROSE': TrumpfColorMode('ROSE'),
        'BELL': TrumpfColorMode('BELL'),
        'ACORN': TrumpfColorMode('ACORN'),
        'SHIELD': TrumpfColorMode('SHIELD'),
    }[trumpf]

def get_trumpf(trumpf):
    return {
        'OBE_ABE': Trumpf.OBE_ABE,
        'UNDE_UFE': Trumpf.UNDE_UFE,
        'ROSE': Trumpf.ROSE,
        'BELL': Trumpf.BELL,
        'ACORN': Trumpf.ACORN,
        'SHIELD': Trumpf.SHIELD,
    }[trumpf]
