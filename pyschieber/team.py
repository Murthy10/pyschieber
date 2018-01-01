class Team:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

    def get_players(self):
        return [self.player_1, self.player_2]
