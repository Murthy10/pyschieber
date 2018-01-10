from pyschieber.game import Game
from pyschieber.player.base_player import BasePlayer


class Tournament:
    def __init__(self):
        self.players = {}
        self.teams = {1: [], 2: []}

    def start(self):
        self.check_players()
        self.init_teams()

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
                self.teams[1].append(self.players[key])
            else:
                self.teams[2].append(self.players[key])

    def play_game(self):
        game = Game(players=self.players)
        game.start()
        return self.players[1].cards
