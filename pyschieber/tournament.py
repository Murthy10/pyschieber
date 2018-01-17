import logging

from pyschieber.game import Game
from pyschieber.player.base_player import BasePlayer
from pyschieber.team import Team

logger = logging.getLogger(__name__)


class Tournament:
    def __init__(self, point_limit=1500):
        self.point_limit = point_limit
        self.players = []
        self.teams = []
        self.round = 1

    def check_players(self):
        player_numbers = []
        for index, player in enumerate(self.players):
            assert isinstance(player, BasePlayer)
            player_numbers.append(index)
        assert {0, 1, 2, 3} == set(player_numbers)

    def register_player(self, player):
        assert len(self.players) < 4
        self.players.append(player)

    def build_teams(self):
        self.check_players()
        team_1 = Team(players=[self.players[0], self.players[2]])
        team_2 = Team(players=[self.players[1], self.players[2]])
        self.teams += [team_1, team_2]

    def play(self):
        self.build_teams()
        logger.info('Tournament starts, the goal are {} points.'.format(self.point_limit))
        end = False
        while not end:
            game = Game(teams=self.teams, point_limit=self.point_limit)
            logger.info('-' * 200)
            logger.info('Round {} starts.'.format(self.round))
            logger.info('-' * 200)
            end = game.play()
            logger.info('Round {} is over.'.format(self.round))
            logger.info('Points: Team 1: {0} , Team 2: {1}. \n'.format(self.teams[0].points, self.teams[1].points))
            self.round += 1
