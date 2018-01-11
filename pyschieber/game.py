from random import shuffle
import logging

from pyschieber.deck import Deck
from pyschieber.rules.stich_rules import stich_rules, card_allowed
from pyschieber.stich import PlayedCard

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, players=None, ):
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
            logger.info('Stich: {0} \n'.format(stich.player))
            start_player_key = self.get_key(stich.player)
            self.stiche.append(stich)

    def get_key(self, player):
        for key, value in self.players.items():
            if player == value:
                return key

    def play_stich(self, start_player_key):
        first_card = self.play_card(first_card=None, player=self.players[start_player_key])
        played_cards = [PlayedCard(player=self.players[start_player_key], card=first_card)]
        for i in get_player_key(start_key=start_player_key):
            current_player = self.players[i]
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
            card = generator.send(is_allowed_card)
            chosen_card = chosen_card if card is None else card
        else:
            logger.info('{0}:{1}'.format(player, chosen_card))
            player.cards.remove(chosen_card)
        return chosen_card


def get_player_key(start_key):
    for i in range(3):
        yield (i + start_key) % 4 + 1
