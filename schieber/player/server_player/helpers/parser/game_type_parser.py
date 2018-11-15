from schieber.player.server_player.helpers.messages import GameType
from schieber.player.server_player.helpers.parser.color_parser import suit_to_color, color_to_suit
from schieber.suit import Suit
from schieber.trumpf import Trumpf


def pyschieber_trumpf_to_game_type(pyschieber_trumpf):
    if pyschieber_trumpf == Trumpf.OBE_ABE:
        return GameType("OBEABE")

    if pyschieber_trumpf == Trumpf.UNDE_UFE:
        return GameType("UNDEUFE")

    if pyschieber_trumpf == Trumpf.SCHIEBEN:
        return GameType("SCHIEBE")

    suit = Suit[pyschieber_trumpf.name]
    color = suit_to_color(suit)
    return GameType("TRUMPF", color.name)


def game_type_to_pyschieber_trumpf(game_type):
    if hasattr(game_type, 'trumpf_color'):
        color = game_type.trumpf_color
        suit = color_to_suit(color)
        return Trumpf[suit.name]
    else:
        if game_type.mode == "OBEABE":
            return Trumpf.OBE_ABE
        if game_type.mode == "UNDEUFE":
            return Trumpf.UNDE_UFE
        if game_type.mode == "SCHIEBE":
            return Trumpf.SCHIEBEN
