import re

from pyschieber.suit import Suit


class Card:
    names = {6: '6', 7: '7', 8: '8', 9: '9', 10: 'Banner', 11: 'Under', 12: 'Ober', 13: 'Koennig', 14: 'Ass'}
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


def from_string_to_card(card_string):
    regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', Card.format_string)
    values = list(re.search(regex, card_string).groups())
    suit = Suit[values[0]]
    card_value = ''
    for key, value in Card.names.items():
        if value == values[1]:
            card_value = key
            break
    return Card(suit=suit, value=card_value)
