from pyschieber.suit import Suit


def split_cards_by_suit(cards):
    suits = []
    for suit in Suit:
        suit_cards = [card.value for card in cards if card.suit.name == suit.name]
        suits.append((suit, suit_cards))
    return suits