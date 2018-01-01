import pytest

from pyschieber.tournament import Tournament


def test_tournament():
    tournament = Tournament()
    tournament.play_game()