from schieber.card import Card as PyschieberCard
from schieber.player.server_player.helpers.parser.color_parser import suit_to_color, color_to_suit
from schieber.player.server_player.helpers.server_cards import ServerCard


def pyscheiber_card_to_challenge_card(pyschieber_card):
    color = suit_to_color(pyschieber_card.suit)
    return ServerCard(color=color.name, number=pyschieber_card.value)


def challenge_card_to_pyschieber_card(challenge_card):
    suit = color_to_suit(challenge_card.color)
    return PyschieberCard(suit=suit, value=challenge_card.number)
