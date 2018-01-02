from collections import namedtuple

from pyschieber.trumpf import Trumpf

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])

Stich = namedtuple('Stich', ['player', 'played_cards', 'trumpf'])


def obe_abe(played_cards):
    suit = played_cards[0].card.suit
    value = played_cards[0].card.value
    stich = Stich(player=played_cards[0].player, played_cards=played_cards, trumpf=Trumpf.OBE_ABE)
    for i in range(1, len(played_cards)):
        current_suit = played_cards[i].card.suit
        current_value = played_cards[i].card.value
        if suit == current_suit and current_value > value:
            stich = Stich(player=played_cards[i].player, played_cards=played_cards, trumpf=Trumpf.OBE_ABE)
            value = current_value
    return stich


stich_rules = {Trumpf.OBE_ABE: obe_abe}
