from random import shuffle

from pyschieber.deck import Deck


class Game:
    def __init__(self, start_player=None, players=None):
        self.start_player = start_player
        self.players = players
        self.trumpf = None
        self.deck = Deck()
        self.stiche = []
        shuffle(self.deck.cards)

    def start(self):
        self.deal_cards()
        self.set_trumpf()

    def deal_cards(self):
        for i, card in enumerate(self.deck.cards):
            self.players[i % 4].set_card(card=card)

    def set_trumpf(self):
        self.trumpf = self.start_player.choose_trumpf()

    def play(self):
        i = self.players.index(self.start_player)
        for _ in self.deck.cards:
            player_index = i % 4
            card = self.players[player_index].choose_card()
            print('Player {0}: Card {1}'.format(player_index + 1, card))
            i += 1
