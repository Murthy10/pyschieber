import inspect

from pyschieber.trumpf import Trumpf


class BasePlayer:
    def __init__(self, name='unknown'):
        self.name = name
        self.cards = []
        self.trumpf_list = list(Trumpf)
        self.id = None

    def get_dict(self):
        return dict(name=self.name, type=type(self).__name__)

    def set_card(self, card):
        self.cards.append(card)

    def choose_trumpf(self, geschoben):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def choose_card(self, state=None):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def stich_over(self, state=None):
        pass

    def __str__(self):
        return '<Player:{}>'.format(self.name)