from functools import partial

from schieber.stich import Stich
from schieber.trumpf import Trumpf

UNDER = 11
NAELL = 9


def stich_obe_unde(played_cards, operation, trumpf):
    suit = played_cards[0].card.suit
    (_, index) = operation(
        [(played_card.card.value, i) for i, played_card in enumerate(played_cards) if played_card.card.suit == suit])
    return Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)


def stich_trumpf(played_cards, trumpf):
    trumpfs = [(played_card.card.value, i) for i, played_card in enumerate(played_cards) if
               played_card.card.suit.name == trumpf.name]
    if trumpfs:
        index = _stich_trumpf_cards(trumpfs=trumpfs)
        return Stich(player=played_cards[index].player, played_cards=played_cards, trumpf=trumpf)
    else:
        return stich_obe_unde(played_cards=played_cards, operation=max, trumpf=trumpf)


def _stich_trumpf_cards(trumpfs):
    values = [trumpf[0] for trumpf in trumpfs]
    if UNDER in values:  # Under
        return trumpfs[values.index(UNDER)][1]
    if NAELL in values:
        return trumpfs[values.index(NAELL)][1]
    return max(trumpfs)[1]

    #return values.index(max(values))


stich_rules = {
    Trumpf.OBE_ABE: partial(stich_obe_unde, operation=max, trumpf=Trumpf.OBE_ABE),
    Trumpf.UNDE_UFE: partial(stich_obe_unde, operation=min, trumpf=Trumpf.UNDE_UFE),
}

for trumpf in filter(lambda x: x != Trumpf.OBE_ABE and x != Trumpf.UNDE_UFE and x != Trumpf.SCHIEBEN, Trumpf):
    stich_rules[trumpf] = partial(stich_trumpf, trumpf=trumpf)


def card_allowed(table_cards, chosen_card, hand_cards, trumpf):
    chosen_suit = chosen_card.suit

    if chosen_card not in hand_cards:
        return False

    if not table_cards or len(hand_cards) == 1:
        return True

    first_card = table_cards[0]
    first_suit = first_card.suit

    if first_suit == chosen_suit:
        return True

    if trumpf in [Trumpf.OBE_ABE, Trumpf.UNDE_UFE]:
        hand_suits = set([hand_card.suit for hand_card in hand_cards])
    else:
        if chosen_suit.name == trumpf.name:
            return not does_under_trumpf(table_cards=table_cards, chosen_card=chosen_card, hand_cards=hand_cards,
                                         trumpf=trumpf)
        hand_suits = set([card.suit for card in hand_cards if not is_trumpf_under(trumpf=trumpf, card=card)])
    return not (first_suit in hand_suits)


def is_trumpf_under(trumpf, card):
    return card.suit.name == trumpf.name and card.value == UNDER


def does_under_trumpf(table_cards, chosen_card, hand_cards, trumpf):
    if is_chosen_card_best_trumpf(table_cards=table_cards, chosen_card=chosen_card, trumpf=trumpf):
        return False

    trumpf_cards_on_hand = [card for card in hand_cards if card.suit.name == trumpf.name]
    if len(trumpf_cards_on_hand) < len(hand_cards):
        return True

    for trumpf_card in trumpf_cards_on_hand:
        if is_chosen_card_best_trumpf(table_cards=table_cards, chosen_card=trumpf_card, trumpf=trumpf):
            return True
    return False


def is_chosen_card_best_trumpf(table_cards, chosen_card, trumpf):
    trumpfs = [(card.value, i) for i, card in enumerate(table_cards) if card.suit.name == trumpf.name]
    chosen_card_index = len(table_cards)
    trumpfs.append((chosen_card.value, chosen_card_index))
    winner_index = _stich_trumpf_cards(trumpfs=trumpfs)
    return winner_index == chosen_card_index


def allowed_cards(hand_cards, table_cards, trumpf):
    cards = []
    if len(table_cards) > 0 or len(hand_cards) > 1:
        for card in hand_cards:
            if card_allowed(table_cards, card, hand_cards, trumpf):
                cards.append(card)
    else:
        cards += hand_cards
    return cards
