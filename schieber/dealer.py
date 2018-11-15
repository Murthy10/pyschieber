import random

from schieber.deck import Deck


class Dealer:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()

    def shuffle_cards(self, seed=None):
        """
        Shuffles the cards to a random ordering.
        :param seed
        :return:
        """
        random.seed(seed)
        random.shuffle(self.deck.cards)

    def deal_cards(self):
        """
        Deals 9 cards for every one of the 4 players participating in the game.
        :return:
        """
        for i, card in enumerate(self.deck.cards):
            self.players[i % 4].set_card(card=card)
