import logging
import sys
import time
from threading import Thread

import pytest
from timeit import default_timer as timer
from math import sqrt, floor

from schieber.suit import Suit

from schieber.card import Card

from schieber.game import Game

from schieber.team import Team

from schieber.player.external_player import ExternalPlayer

from schieber.player.random_player import RandomPlayer
from schieber.tournament import Tournament


def test_control():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')

    players = [RandomPlayer(name='Tick', ), RandomPlayer(name='Trick'),
               RandomPlayer(name='Track'), ExternalPlayer(name='Dagobert')]

    team_1 = Team(players=[players[0], players[2]])
    team_2 = Team(players=[players[1], players[3]])
    teams = [team_1, team_2]
    game = Game(teams, point_limit=1000, use_counting_factor=False, seed=1)

    thread = Thread(target=game.play_endless)
    thread.start()

    player = players[3]
    action = Card(Suit.ROSE, 9)

    print("Test starts")

    assert not game.stop_playing

    player.get_observation()
    assert player.before_first_stich()
    print(len(player.cards))
    player.set_action(action)

    for i in range(7):
        print(f"Round {i}")
        player.get_observation()
        print(len(player.cards))
        assert not player.before_first_stich()
        player.set_action(action)
        print(len(player.cards))

    print(len(player.cards))
    assert player.at_last_stich()

    game.endless_play_control.acquire()
    game.stop_playing = True
    game.endless_play_control.notify_all()
    game.endless_play_control.release()

    assert game.stop_playing
