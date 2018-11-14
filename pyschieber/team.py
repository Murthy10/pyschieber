class Team:
    def __init__(self, players=None):
        self.points = 0
        self.players = players

    def player_by_number(self, number):
        """
        Returns the player by the number in the team. The number should be either 0 or 1.
        :param number:
        :return:
        """
        for player in self.players:
            if player.number == number:
                return player
        return None

    def won(self, point_limit):
        """
        Checks if the team already won
        :param point_limit:
        :return: true if the points of the team are larger than the point limit and false otherwise
        """
        return self.points >= point_limit
