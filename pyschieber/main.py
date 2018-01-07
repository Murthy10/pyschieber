from pyschieber.player.cli_player import CliPlayer
from pyschieber.player.random_player import RandomPlayer
from pyschieber.tournament import Tournament


def start_tournament():
    tournament = Tournament()
    cli_player = CliPlayer(name='CliPlayer')
    tournament.register_player(cli_player, 1)
    [tournament.register_player(RandomPlayer(), i) for i in range(2, 5)]
    tournament.play_game()


def print_table(played_cards):
    table = 'Table: '
    for played_card in played_cards:
        table += '{0}: {1} | '.format(played_card.player, played_card.card)
    print(table)


if __name__ == "__main__":
    start_tournament()
