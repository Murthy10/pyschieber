import math
import re

from schieber.suit import Suit


class Card:
    """
    Defines a card used in the game of Jassen.
    """
    names = {6: '6', 7: '7', 8: '8', 9: '9', 10: 'Banner', 11: 'Under', 12: 'Ober', 13: 'Koennig', 14: 'Ass'}
    trumpf_rank = {6: 6, 7: 7, 8: 8, 10: 10, 12: 12, 13: 13, 14: 14, 9: 15, 11: 16}
    format_string = '<{0}:{1}>'

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        name = str(self.value)
        if self.value > 9:
            name = Card.names[self.value]
        return self.format_string.format(self.suit.name, name)

    def __repr__(self):
        return str(self)

    def get_trumpf_rank(self):
        return self.trumpf_rank[self.value]

    def is_higher_trumpf_than(self, other):
        return self.trumpf_rank > other.trumpf_rank

    def is_higher_than(self, other):
        return self.suit == other.suit and self.value > other.value

    def get_score(self, trumpf):
        if trumpf.name == self.suit.name:
            return 50 + self.get_trumpf_rank()
        else:
            return self.value


def from_card_to_string(card):
    return str(card)


def from_string_to_card(card_string):
    """
    Converts a string representation of a card back to a card object.
    :param card_string:
    :return:
    """
    regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', Card.format_string)
    values = list(re.search(regex, card_string).groups())
    suit = Suit[values[0]]
    card_value = ''
    for key, value in Card.names.items():
        if value == values[1]:
            card_value = key
            break
    return Card(suit=suit, value=card_value)


def from_card_to_tuple(card):
    return card.suit.value, card.value - 6


def from_tuple_to_card(card_tuple):
    return Card(suit=Suit(card_tuple[0]), value=card_tuple[1] + 6)


def from_string_to_tuple(card_string):
    card = from_string_to_card(card_string)
    return from_card_to_tuple(card)


def from_tuple_to_string(card_tuple):
    card = from_tuple_to_card(card_tuple)
    return from_card_to_string(card)


def from_string_to_index(card_string):
    card = from_string_to_card(card_string)
    return from_card_to_index(card)


def from_index_to_string(card_index):
    card = from_index_to_card(card_index)
    return from_card_to_string(card)


def from_index_to_card(card_index):
    """
        The index is a number between 1 and 36 representing a card in the following way:
        SUIT    6   7   8   9   Banner  Under   Ober    Koennig Ass
        ROSE    1   2   3   4   5       6       7       8       9
        BELL    10  11  12  13  14      15      16      17      18
        ACORN   19  20  21  22  23      24      25      26      27
        SHIELD  28  29  30  31  32      33      34      35      36
        An index of 0 denotes an empty Card --> None
        :param card_index:
        :return:
        """
    assert 0 <= card_index <= 36
    if card_index == 0:
        return None
    return Card(suit=Suit(_get_suit(card_index)), value=_get_value(card_index))


def from_card_to_index(card):
    if card is None:
        return 0
    return card.value + card.suit.value * 9 - 5


def _get_suit(card_index):
    return int(math.floor(card_index / 9.1))


def _get_value(card_index):
    return card_index - _get_suit(card_index) * 9 + 5
