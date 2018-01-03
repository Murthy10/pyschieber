import operator

from collections import namedtuple
from functools import partial

from pyschieber.trumpf import Trumpf

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])

Stich = namedtuple('Stich', ['player', 'played_cards', 'trumpf'])


def ordered(played_cards, operation, trumpf):
    suit = played_cards[0].card.suit
    (_, index) = operation([(played_card.card.value, i) for i, played_card in enumerate(played_cards) if played_card.card.suit == suit])
    stich = Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)
    return stich


stich_rules = {
    Trumpf.OBE_ABE: partial(ordered, operation=max, trumpf=Trumpf.OBE_ABE),
    Trumpf.UNDE_UFE: partial(ordered, operation=min, trumpf=Trumpf.UNDE_UFE),
}
