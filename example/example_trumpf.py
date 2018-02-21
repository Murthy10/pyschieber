from pyschieber.suit import Suit
from pyschieber.trumpf import Trumpf


# https://www.jassverzeichnis.ch/index.php/blog/95-jass-tipps-trumpfansagen-schieber
def choose_trumpf(cards, geschoben):
    candidates = []
    for trumpf in filter(lambda x: x != Trumpf.OBE_ABE and x != Trumpf.UNDE_UFE and x != Trumpf.SCHIEBEN, Trumpf):
        if evalute_stich_trumpf(cards, trumpf):
            candidates.append(trumpf)
    if evalute_obe_abe(cards):
        candidates.append(Trumpf.OBE_ABE)
    if evalute_obe_abe(cards):
        candidates.append(Trumpf.UNDE_UFE)
    if len(candidates) >= 1:
        return candidates[0]
    return Trumpf.SCHIEBEN


def evalute_stich_trumpf(cards, trumpf):
    trumpf_card_values = [card.value for card in cards if card.suit.name == trumpf.name]
    non_trumpf_card_values = [card for card in cards if card.suit.name != trumpf.name]
    nell = bool(9 in trumpf_card_values)
    under = bool(12 in trumpf_card_values)
    ass = bool(14 in trumpf_card_values)
    if under and len(trumpf_card_values) == 4:
        return True
    if ass and nell and len(trumpf_card_values) == 5:
        return True
    if ass and nell and under and non_trumpf_card_values.count(14) >= 2:
        return True


def evalute_unde_ufe(cards):
    suits = split_cards_by_suit(cards)
    stiche = []
    for suit, suit_cards in suits:
        best_card = 6
        suit_card_copy = list(suit_cards)
        for _ in suit_cards:
            if best_card in suit_cards:
                stiche.append((suit, best_card))
                suit_card_copy.remove(best_card)
                best_card += 1
            else:
                break
        if best_card >= 8:
            for card in suit_card_copy:
                stiche.append((suit, card))
    return len(stiche) > 5


def evalute_obe_abe(cards):
    suits = split_cards_by_suit(cards)
    stiche = []
    for suit, suit_cards in suits:
        best_card = 14
        suit_card_copy = list(suit_cards)
        for _ in suit_cards:
            if best_card in suit_cards:
                stiche.append((suit, best_card))
                suit_card_copy.remove(best_card)
                best_card -= 1
            else:
                break
        if best_card >= 12:
            for card in suit_card_copy:
                stiche.append((suit, card))
    return len(stiche) > 5


def split_cards_by_suit(cards):
    suits = []
    for suit in Suit:
        suit_cards = [card.value for card in cards if card.suit.name == suit.name]
        suits.append((suit, suit_cards))
    return suits
