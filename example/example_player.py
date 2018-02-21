import random

from pyschieber.player.base_player import BasePlayer

from example.example_trumpf import choose_trumpf


class ExamplePlayer(BasePlayer):
    bad_trumpf_reward = -100
    bad_card_reward = -10

    @classmethod
    def with_tournament(cls, name, tournament):
        player = cls(name=name)
        player.tournament = tournament
        player.reward = 0
        player.points_team_1 = 0
        player.points_team_2 = 0
        return player

    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            trumpf, _ = choose_trumpf(cards=self.cards, geschoben=geschoben)
            allowed = yield trumpf
            if allowed:
                yield None
            else:
                self.reward += self.bad_trumpf_reward

    def choose_card(self):
        allowed = False
        while not allowed:
            card = random.choice(self.cards)
            allowed = yield card
            if allowed:
                yield None
            else:
                self.reward += self.bad_card_reward

    def stich_over(self):
        self.calculate_reward()

    def calculate_reward(self):
        teams = self.tournament.teams
        current_points_team_1 = teams[0].points
        current_points_team_2 = teams[2].points
        diff_1 = current_points_team_1 - self.points_team_1
        diff_2 = current_points_team_2 - self.points_team_2
        self.points_team_1, self.points_team_2 = current_points_team_1, current_points_team_2
        reward = diff_1 - diff_2
        self.reward += reward
