import logging

from pyschieber.dealer import Dealer
from pyschieber.rules.stich_rules import stich_rules, card_allowed
from pyschieber.rules.trumpf_rules import trumpf_allowed
from pyschieber.rules.count_rules import count_stich, counting_factor
from pyschieber.stich import PlayedCard, stich_dict, played_cards_dict
from pyschieber.trumpf import Trumpf

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, teams=None, point_limit=2500):
        self.teams = teams
        self.point_limit = point_limit
        self.players = teams[0].players + teams[1].players
        self.dealer = Dealer(players=self.players)
        self.geschoben = False
        self.trumpf = None
        self.stiche = []
        self.cards_on_table = []

    def play(self, start_player_index=0):
        self.dealer.shuffle_cards()
        self.dealer.deal_cards()
        self.define_trumpf(start_player_index=start_player_index)
        logger.info('Chosen Trumpf: {0} \n'.format(self.trumpf.name))
        for i in range(9):
            stich = self.play_stich(start_player_index)
            self.count_points(stich, last=(i == 8))
            self.stich_over_information()
            logger.info('\nStich: {0} \n'.format(stich.player))
            logger.info('{}{}\n'.format('-' * 180, self.trumpf))
            start_player_index = self.players.index(stich.player)
            self.stiche.append(stich)
            if self.teams[0].won(self.point_limit) or self.teams[1].won(self.point_limit):
                return True
        return False

    def define_trumpf(self, start_player_index):
        is_allowed_trumpf = False
        generator = self.players[start_player_index].choose_trumpf(geschoben=self.geschoben)
        chosen_trumpf = next(generator)
        if chosen_trumpf == Trumpf.SCHIEBEN:
            self.geschoben = True
            generator = self.players[(start_player_index + 2) % 4].choose_trumpf(geschoben=self.geschoben)
            chosen_trumpf = next(generator)
            while not is_allowed_trumpf:
                is_allowed_trumpf = trumpf_allowed(chosen_trumpf=chosen_trumpf, geschoben=self.geschoben)
                trumpf = generator.send(is_allowed_trumpf)
                chosen_trumpf = chosen_trumpf if trumpf is None else trumpf
        self.trumpf = chosen_trumpf

    def play_stich(self, start_player_index):
        self.cards_on_table = []
        first_card = self.play_card(first_card=None, player=self.players[start_player_index])
        self.cards_on_table = [PlayedCard(player=self.players[start_player_index], card=first_card)]
        for i in get_player_index(start_index=start_player_index):
            current_player = self.players[i]
            card = self.play_card(first_card=first_card, player=current_player)
            self.cards_on_table.append(PlayedCard(player=current_player, card=card))
        stich = stich_rules[self.trumpf](played_cards=self.cards_on_table)
        return stich

    def play_card(self, first_card, player):
        is_allowed_card = False
        generator = player.choose_card(state=self.get_status())
        chosen_card = next(generator)
        while not is_allowed_card:
            is_allowed_card = card_allowed(first_card=first_card, chosen_card=chosen_card, hand_cards=player.cards,
                                           trumpf=self.trumpf)
            card = generator.send(is_allowed_card)
            chosen_card = chosen_card if card is None else card
        else:
            logger.info('Table: {0}:{1}'.format(player, chosen_card))
            player.cards.remove(chosen_card)
        return chosen_card

    def stich_over_information(self):
        [player.stich_over(state=self.get_status()) for player in self.players]

    def count_points(self, stich, last):
        stich_player_index = self.players.index(stich.player)
        cards = [played_card.card for played_card in stich.played_cards]
        self.add_points(team_index=(stich_player_index % 2), cards=cards, last=last)

    def add_points(self, team_index, cards, last):
        self.teams[team_index].points += count_stich(cards, self.trumpf, last=last) * counting_factor[self.trumpf]

    def get_status(self):
        return dict(stiche=[stich_dict(stich) for stich in self.stiche], trumpf=self.trumpf.name,
                    geschoben=self.geschoben, point_limit=self.point_limit,
                    table=[played_cards_dict(played_card) for played_card in self.cards_on_table],
                    teams=[dict(points=team.points) for team in self.teams])


def get_player_index(start_index):
    for i in range(1, 4):
        yield (i + start_index) % 4
