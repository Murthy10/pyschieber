import inspect

from pyschieber.card import from_string_to_card
from pyschieber.trumpf import Trumpf
from pyschieber.rules.stich_rules import allowed_cards


class BasePlayer:
    def __init__(self, name='unknown', seed=None):
        self.name = name
        self.cards = []
        self.trumpf_list = list(Trumpf)
        self.id = None
        self.seed = seed

    def get_dict(self):
        """
        Returns a dictionary containing:
        - the name
        - the type (RandomPlayer, GreedyPlayer, etc.)
        :return:
        """
        return dict(name=self.name, type=type(self).__name__)

    def set_card(self, card):
        self.cards.append(card)

    def choose_trumpf(self, geschoben):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def choose_card(self, state=None):
        raise NotImplementedError(str(inspect.stack()[1][3]))

    def move_made(self, player_id, card, state):
        pass

    def stich_over(self, state=None):
        pass

    def game_started(self):
        pass

    def allowed_cards(self, state):
        """
        Returns the cards on the hand of the player which he/she is allowed to play in the current state
        :param state:
        :return:
        """
        table_cards = [from_string_to_card(entry['card']) for entry in state['table']]
        trumpf = Trumpf[state['trumpf']]
        return allowed_cards(hand_cards=self.cards, table_cards=table_cards, trumpf=trumpf)

    def __str__(self):
        return '<Player:{}>'.format(self.name)
