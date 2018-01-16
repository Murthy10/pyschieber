class Team:
    def __init__(self, number, players):
        assert number in [1, 2]
        self.points = 0
        self.number = number
        self.players = players

    def player_by_number(self, number):
        for player in self.players:
            if player.number == number:
                return player
        return None

    def won(self, point_limit):
        return self.points >= point_limit
