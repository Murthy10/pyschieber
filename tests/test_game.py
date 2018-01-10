from pyschieber.player.random_player import RandomPlayer

from pyschieber.game import Game


def test_game():
    players = {}
    random_players = [RandomPlayer() for _ in range(1, 5)]
    players[1] = random_players[0]
    players[2] = random_players[1]
    players[3] = random_players[2]
    players[4] = random_players[3]

    game = Game(players=players)

    game.start()
