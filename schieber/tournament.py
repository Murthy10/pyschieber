import logging

from schieber.game import Game
from schieber.team import Team

logger = logging.getLogger(__name__)


class Tournament:
    def __init__(self, point_limit=1500, seed=None):
        """
        Sets the point limit and initializes the players, teams and games arrays.
        :param point_limit:
        """
        self.point_limit = point_limit
        self.players = []
        self.teams = []
        self.games = []
        self.seed = seed

    def check_players(self):
        """
        Checks if there are really 4 players in the array
        :return:
        """
        player_numbers = []
        for index, player in enumerate(self.players):
            player_numbers.append(index)
        assert {0, 1, 2, 3} == set(player_numbers)

    def register_player(self, player):
        """
        Adds another player if there are still less than 4 players
        :param player:
        :return:
        """
        number_of_players = len(self.players)
        assert number_of_players < 4
        self.players.append(player)
        player.id = number_of_players

    def build_teams(self):
        """
        Builds the teams based on the players array
        :return: the team list
        """
        self.check_players()
        team_1 = Team(players=[self.players[0], self.players[2]])
        team_2 = Team(players=[self.players[1], self.players[3]])
        self.teams = [team_1, team_2]
        return self.teams

    def play(self, rounds=0, use_counting_factor=False):
        """
        Plays a tournament until one team reaches the point_limit.
        :param rounds:
        :param use_counting_factor: if True: Undenufe and Obenabe are counted 3-fold and Shield and Bell are counted 2-fold
        :return:
        """
        self.build_teams()
        logger.info('Tournament starts, the point limit is {}.'.format(self.point_limit))
        end = False
        whole_rounds = True if rounds > 0 else False
        round_counter = 0
        while not end:
            if self.seed is not None:
                # Increment seed by one so that each game is different.
                # But still the sequence of games is the same each time
                self.seed += 1
            game = Game(teams=self.teams, point_limit=self.point_limit, use_counting_factor=use_counting_factor, seed=self.seed)
            self.games.append(game)
            logger.info('-' * 200)
            logger.info('Round {} starts.'.format(len(self.games)))
            logger.info('-' * 200)
            end = game.play(start_player_index=((len(self.games) - 1) % 4), whole_rounds=whole_rounds)
            logger.info('Round {} is over.'.format(len(self.games)))
            logger.info('Points: Team 1: {0} , Team 2: {1}. \n'.format(self.teams[0].points, self.teams[1].points))
            round_counter += 1
            if whole_rounds and round_counter == rounds:
                end = True
        winning_team = 0 if self.teams[0].won(point_limit=self.point_limit) else 1
        logger.info('Team {0} won! \n'.format(winning_team))
        self.reset()

    def get_status(self):
        """
        Returns the status of the tournament
        :return:
        """
        return {
            'games': [game.get_status() for game in self.games],
            'players': [player.get_dict() for player in self.players]
        }

    def reset(self):
        """
        Resets the tournament. Deletes the games array and deletes the cards of the players.
        :return:
        """
        self.games = []
        for player in self.players:
            player.cards = []
