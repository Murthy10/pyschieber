from random import shuffle

from pyschieber.deck import Deck
from pyschieber.rules.stich_rules import stich_rules, card_allowed
from pyschieber.stich import Stich, PlayedCard


class Game:
    def __init__(self, players=None):
        self.players = players
        self.trumpf = None
        self.deck = Deck()
        self.stiche = []
        shuffle(self.deck.cards)

    def start(self):
        self.deal_cards()
        self.play()

    def deal_cards(self):
        for i, card in enumerate(self.deck.cards):
            self.players[i % 4 + 1].set_card(card=card)

    def play(self):
        start_player_key = 1
        self.trumpf = self.players[start_player_key].choose_trumpf()
        for _ in range(9):
            stich = self.play_stich(start_player_key)
            print(stich)
            self.stiche.append(stich)

    def play_stich(self, start_player_key):
        first_card = self.play_card(first_card=None, player=self.players[start_player_key])
        played_cards = []
        for i in range(start_player_key + 1, start_player_key + 3):
            player_key = i % 4
            current_player = self.players[player_key]
            card = self.play_card(first_card=first_card, player=current_player)
            played_cards.append(PlayedCard(player=current_player, card=card))
        return stich_rules[self.trumpf](played_cards=played_cards)

    def play_card(self, first_card, player):
        is_allowed_card = False
        generator = player.choose_card()
        chosen_card = next(generator)
        while not is_allowed_card:
            is_allowed_card = card_allowed(first_card=first_card, chosen_card=chosen_card, hand_cards=player.cards,
                                           trumpf=self.trumpf)
            print("Chosen card {}".format(chosen_card))
            card = generator.send(is_allowed_card)
            chosen_card = chosen_card if card is None else card
        else:
            player.cards.remove(chosen_card)
        return chosen_card
