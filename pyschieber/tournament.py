import logging

from pyschieber.game import Game
from pyschieber.player.base_player import BasePlayer

logger = logging.getLogger(__name__)


class Tournament:
    def __init__(self, point_limit=1500):
        self.point_limit = point_limit
        self.players = {}
        self.team_1 = dict(points=0, number=1)
        self.team_2 = dict(points=0, number=2)
        self.round = 1

    def start(self):
        self.check_players()
        self.init_teams()
        logger.info('Tournament starts, the goal are {} points.'.format(self.point_limit))

    def check_players(self):
        player_numbers = []
        for key, player in self.players.items():
            assert isinstance(player, BasePlayer)
            player_numbers.append(key)
        assert {1, 2, 3, 4} == set(player_numbers)

    def register_player(self, player, number):
        assert number in {1, 2, 3, 4}
        self.players[number] = player

    def init_teams(self):
        for key in self.players:
            if key % 2 == 1:
                self.team_1[str(key)] = self.players[key]
            else:
                self.team_2[str(key)] = self.players[key]

    def play_game(self):
        end = False
        while not end:
            game = Game(teams={1: self.team_1, 2: self.team_2}, point_limit=self.point_limit, players=self.players)
            logger.info('-' * 200)
            logger.info('Round {} starts.'.format(self.round))
            logger.info('-' * 200)
            end = game.start()
            logger.info('Round {} is over.'.format(self.round))
            logger.info('Points: Team 1: {0} , Team 2: {1}. \n'.format(self.team_1['points'], self.team_2['points']))
            self.round += 1
