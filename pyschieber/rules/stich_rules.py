from functools import partial

from pyschieber.stich import Stich
from pyschieber.trumpf import Trumpf


def stich_obe_unde(played_cards, operation, trumpf):
    suit = played_cards[0].card.suit
    (_, index) = operation(
        [(played_card.card.value, i) for i, played_card in enumerate(played_cards) if played_card.card.suit == suit])
    return Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)


def stich_trumpf(played_cards, trumpf):
    trumpfs = [(played_card.card.value, i) for i, played_card in enumerate(played_cards) if
               played_card.card.suit.name == trumpf.name]
    if trumpfs:
        values = [trumpf[0] for trumpf in trumpfs]
        if 12 in values:  # Under
            index = trumpfs[values.index(12)][1]
            return Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)
        if 9 in values:  # Näll
            index = trumpfs[values.index(9)][1]
            return Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)
        index = max(trumpfs)[1]
        return Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)
    else:
        return stich_obe_unde(played_cards=played_cards, operation=max, trumpf=trumpf)


stich_rules = {
    Trumpf.OBE_ABE: partial(stich_obe_unde, operation=max, trumpf=Trumpf.OBE_ABE),
    Trumpf.UNDE_UFE: partial(stich_obe_unde, operation=min, trumpf=Trumpf.UNDE_UFE),
}

for trumpf in filter(lambda x: x != Trumpf.OBE_ABE and x != Trumpf.UNDE_UFE and x != Trumpf.SCHIEBEN, Trumpf):
    stich_rules[trumpf] = partial(stich_trumpf, trumpf=trumpf)


def card_allowed(first_card, chosen_card, hand_cards, trumpf):
    chosen_suit = chosen_card.suit
    if chosen_card not in hand_cards:
        return False
    if first_card is None:
        return True
    first_suit = first_card.suit
    if first_suit == chosen_suit or chosen_suit.name == trumpf.name:
        return True
    else:
        hand_suits = [hand_card.suit for hand_card in hand_cards if
                      hand_card.suit.name != trumpf.name and hand_card.value != 12]
        if first_suit in hand_suits:
            return False
        else:
            return True
