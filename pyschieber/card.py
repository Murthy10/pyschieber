from pyschieber.suit import Suit


class Card:
    names = {6: '6', 7: '7', 8: '8', 9: '9', 10: 'Banner', 11: 'Under', 12: 'Ober', 13: 'Koennig', 14: 'Ass'}
    values = {v: k for k, v in names.items()}
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


def from_string_to_card(card_string: str):
    # Remove surrounding "<" and ">"
    card_string = card_string[1:-1]

    # Split into suit and value part
    suit_name, value_name = card_string.split(':')

    # Convert strings to actual types
    card_suit = Suit[suit_name]
    card_value = Card.values[value_name]

    return Card(suit=card_suit, value=card_value)
