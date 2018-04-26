from example.challenge_player.strategy.mode.trumpf_color_mode import *
from example.challenge_player.strategy.mode.top_down_mode import *
from example.challenge_player.strategy.mode.bottom_up_mode import *
from example.challenge_player.strategy.flags.doesnt_habe_card_flag import DoesntHaveCardFlag
from pyschieber.deck import Deck
from pyschieber.card import from_string_to_card
from pyschieber.rules.stich_rules import stich_rules
from pyschieber.trumpf import Trumpf
from pyschieber.stich import PlayedCard


class CardCounter:
    def __init__(self, my_id):
        self.played_cards = [[],[],[],[]]
        self.flags = [[],[],[],[]]
        self.played_count = 0
        self.current_stich = {}
        self.stiche = []
        self.my_id = my_id
        self.partner_id = (my_id + 2) % 4

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

        #print('1contiume here... (CardCounter.java:103)')

    def round_leader(self, state):
        return stich_rules[get_trumpf(state['trumpf'])](played_cards=self.get_table_cards()).player

    def get_table_cards(self):
        cards_on_table = []
        for player_id in self.current_stich:
            cards_on_table.append(PlayedCard(player=player_id, card=self.current_stich[player_id]))
        return cards_on_table

    def remaining_cards(self, gone):
        d = Deck()
        return [x for x in d.cards if x not in gone]

    def dead_cards(self):
        dead = []
        current_round = int(self.played_count/4)
        for player_id in range(0, 4):
            dead.extend(self.played_cards[player_id][0:current_round])
        return dead

    def filter_not_dead_cards_of_same_suit(self, card, predicate):
        remaining_of_same_suit = list(filter(lambda x: x.suit == card.suit, self.remaining_cards(self.dead_cards())))
        return list(filter(predicate, remaining_of_same_suit))




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
