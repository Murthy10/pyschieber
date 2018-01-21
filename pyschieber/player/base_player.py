import inspect
from itertools import count


class BasePlayer:
    class_counter = count(0)

    def __init__(self, name='unknown'):
        self.id = next(self.class_counter)
        self.name = name
        self.cards = []

    def get_dict(self):
        return dict(id=self.id, name=self.name, type=type(self).__name__)

    def set_card(self, card):
        self.cards.append(card)

    def choose_trumpf(self):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def choose_card(self):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def __str__(self):
        return '<Player:{}>'.format(self.name)
