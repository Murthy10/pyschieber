from pyschieber.player.base_player import BasePlayer

from example.trumpf_decision import choose_trumpf


class GreedyPlayer(BasePlayer):
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

    def choose_card(self, state=None):
        self.cards.sort()
        allowed = False
        last = -1
        while not allowed:
            card = self.cards[last]
            allowed = yield card
            if allowed:
                yield None
            else:
                last -= 1
                self.reward += self.bad_card_reward

    def stich_over(self, state=None):
        self.calculate_reward()

    def calculate_reward(self):
        teams = self.tournament.teams
        current_points_team_1 = teams[0].points
        current_points_team_2 = teams[1].points
        diff_1 = current_points_team_1 - self.points_team_1
        diff_2 = current_points_team_2 - self.points_team_2
        self.points_team_1, self.points_team_2 = current_points_team_1, current_points_team_2
        reward = diff_1 - diff_2
        self.reward += reward
