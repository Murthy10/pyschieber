from random import shuffle

from pyschieber.deck import Deck


class Dealer:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()

    def shuffle_cards(self):
        shuffle(self.deck.cards)

    def deal_cards(self):
        for i, card in enumerate(self.deck.cards):
            self.players[i % 4].set_card(card=card)
