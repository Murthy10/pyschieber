from pyschieber.game import Game
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
        self.players = [self.player_1, self.player_2, self.player_3, self.player_4]

    def play_game(self):
        start_player = self.player_1
        game = Game(start_player=start_player, players=self.players)
        game.start()
        game.play()
