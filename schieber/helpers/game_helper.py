from schieber.suit import Suit


def split_card_values_by_suit(cards):
    suit_card_values = []
    for suit in Suit:
        suit_cards = [card.value for card in cards if card.suit.name == suit.name]
        suit_card_values.append((suit, suit_cards))
    return suit_card_values


def split_cards_by_suit(cards):
    suit_cards = []
    for suit in Suit:
        cards_per_suit = [card for card in cards if card.suit.name == suit.name]
        suit_cards.append((suit, cards_per_suit))
    return suit_cards
