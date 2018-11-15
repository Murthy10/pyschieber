from schieber.suit import Suit
from schieber.player.server_player.helpers.server_cards import Color

suit_to_color_dict = {Suit.ROSE: Color.HEARTS, Suit.ACORN: Color.DIAMONDS, Suit.BELL: Color.CLUBS,
                      Suit.SHIELD: Color.SPADES}
color_to_suit_dict = dict((v, k) for k, v in suit_to_color_dict.items())


def suit_to_color(suit):
    return suit_to_color_dict[suit]


def color_to_suit(color):
    return color_to_suit_dict[color]
