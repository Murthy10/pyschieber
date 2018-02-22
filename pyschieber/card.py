class Card:
    names = {6: '6', 7: '7', 8: '8', 9: '9', 10: 'Banner', 11: 'Under', 12: 'Ober', 13: 'Koennig', 14: 'Ass'}

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
        return '<{0}:{1}>'.format(self.suit.name, name)
