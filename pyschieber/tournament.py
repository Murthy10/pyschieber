from pyschieber.player import Player
from pyschieber.team import Team


class Tournament:
    def __init__(self):
        self.player_1 = Player()
        self.player_2 = Player()
        self.player_3 = Player()
        self.player_4 = Player()
        self.team_1 = Team(self.player_1, self.player_3)
        self.team_2 = Team(self.player_2, self.player_4)
