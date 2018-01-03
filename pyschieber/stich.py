import operator

from collections import namedtuple
from functools import partial

from pyschieber.trumpf import Trumpf

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])

Stich = namedtuple('Stich', ['player', 'played_cards', 'trumpf'])


def ordered(played_cards, op, trumpf):
    suit = played_cards[0].card.suit
    value = played_cards[0].card.value
    stich = Stich(player=played_cards[0].player, played_cards=played_cards, trumpf=trumpf)
    for i in range(1, len(played_cards)):
        current_suit = played_cards[i].card.suit
        current_value = played_cards[i].card.value
        if suit == current_suit and op(current_value, value):
            stich = Stich(player=played_cards[i].player, played_cards=played_cards, trumpf=trumpf)
            value = current_value
    return stich


stich_rules = {
    Trumpf.OBE_ABE: partial(ordered, op=operator.gt, trumpf=Trumpf.OBE_ABE),
    Trumpf.UNDE_UFE: partial(ordered, op=operator.le, trumpf=Trumpf.UNDE_UFE),
}
