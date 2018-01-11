import inspect


class BasePlayer:
    def __init__(self, name='unknown'):
        self.name = name
        self.cards = []
        self.card_allowed = False

    def set_card(self, card):
        self.cards.append(card)

    def choose_trumpf(self):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def choose_card(self):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def __str__(self):
        return '<Player:{}>'.format(self.name)
