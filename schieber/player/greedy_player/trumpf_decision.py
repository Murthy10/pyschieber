from enum import Enum
from operator import itemgetter

from schieber.helpers.game_helper import *
from schieber.trumpf import Trumpf
from schieber.rules.count_rules import counting_factor

# https://www.jassverzeichnis.ch/index.php/blog/95-jass-tipps-trumpfansagen-schieber
TrumpfType = Enum('TrumpfType',
                  ['UNDER_4', 'NELL_ASS_5', 'UNDER_NELL_ASS', 'UNDER_NELL_3_2_ASS', 'STICHE_5', 'NO_TRUMPF',
                   'HAVE_TO_DECIDE'])


def choose_trumpf(cards, geschoben):
    candidates = []
    for trumpf in filter(lambda x: x != Trumpf.OBE_ABE and x != Trumpf.UNDE_UFE and x != Trumpf.SCHIEBEN, Trumpf):
        trumpf_type = evalute_stich_trumpf(cards, trumpf.name)
        if not trumpf_type == TrumpfType.NO_TRUMPF:
            candidates.append((trumpf, trumpf_type))
    trumpf_type = evalute_unde_ufe(cards)
    if not trumpf_type == TrumpfType.NO_TRUMPF:
        candidates.append((Trumpf.UNDE_UFE, trumpf_type))
    trumpf_type = evalute_obe_abe(cards)
    if not trumpf_type == TrumpfType.NO_TRUMPF:
        candidates.append((Trumpf.OBE_ABE, trumpf_type))
    if len(candidates) >= 1:
        return choose_candidate(candidates)
    elif geschoben:
        return have_to_decide(cards)
    return Trumpf.SCHIEBEN, TrumpfType.NO_TRUMPF


def choose_candidate(candidates):
    max_index = 0
    max_factor = 0
    for i in range(0, len(candidates)):
        trumpf, _ = candidates[i]
        current_factor = counting_factor[trumpf]
        if max_factor < current_factor:
            max_factor = current_factor
            max_index = i
    return candidates[max_index]


def have_to_decide(cards):
    number_of_stiche = count_stiche_per_trumpf(cards)
    number_of_stiche.append((Trumpf.OBE_ABE, len(count_stiche(cards=cards, best_card=14, step=-1))))
    number_of_stiche.append((Trumpf.UNDE_UFE, len(count_stiche(cards=cards, best_card=6, step=1))))
    trumpf, count = max(number_of_stiche, key=itemgetter(1))
    return trumpf, TrumpfType.HAVE_TO_DECIDE


def evalute_stich_trumpf(cards, suit_name):
    trumpf_card_values = [card.value for card in cards if card.suit.name == suit_name]
    non_trumpf_card_values = [card.value for card in cards if card.suit.name != suit_name]
    nell = bool(9 in trumpf_card_values)
    under = bool(11 in trumpf_card_values)
    ass = bool(14 in trumpf_card_values)
    if under and len(trumpf_card_values) == 4:
        return TrumpfType.UNDER_4
    if ass and nell and len(trumpf_card_values) == 5:
        return TrumpfType.NELL_ASS_5
    if ass and nell and under:
        return TrumpfType.UNDER_NELL_ASS
    if nell and under and non_trumpf_card_values.count(14) >= 2:
        return TrumpfType.UNDER_NELL_3_2_ASS
    return TrumpfType.NO_TRUMPF


def evalute_unde_ufe(cards):
    stiche = count_stiche(cards=cards, best_card=6, step=1)
    return TrumpfType.STICHE_5 if len(stiche) > 5 else TrumpfType.NO_TRUMPF


def evalute_obe_abe(cards):
    stiche = count_stiche(cards=cards, best_card=14, step=-1)
    return TrumpfType.STICHE_5 if len(stiche) > 5 else TrumpfType.NO_TRUMPF


def count_stiche_per_trumpf(cards):
    stiche = []
    suits = split_card_values_by_suit(cards)
    for suit, suit_cards in suits:
        nell = bool(9 in suit_cards)
        under = bool(11 in suit_cards)
        stich_counter = 0
        if under:
            stich_counter += 1
            if nell:
                stich_counter += 1
        stiche.append((Trumpf[suit.name], stich_counter))
    return stiche


def count_stiche(cards, best_card, step=1):
    init_best_card = best_card
    suits = split_card_values_by_suit(cards)
    stiche = []
    for suit, suit_cards in suits:
        suit_card_copy = list(suit_cards)
        for _ in suit_cards:
            if best_card in suit_cards:
                stiche.append((suit, best_card))
                suit_card_copy.remove(best_card)
                best_card += step
            else:
                break
        if abs(init_best_card - best_card) >= 3:
            for card in suit_card_copy:
                stiche.append((suit, card))
        best_card = init_best_card
    return stiche
