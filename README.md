[![Build Status](https://travis-ci.org/Murthy10/pyschieber.svg?branch=master)](https://travis-ci.org/Murthy10/pyschieber)
<a href="url"><img src="/docs/images/jasskarten.gif" align="right" width="300" ></a>
# pyschieber
Pyschieber is an implementation of the well known Swiss Schieber Jass game.

As OpenAI Gym provides APIs for several popular games to learn your algorithms master these games.
Pyschieber aims to offer an API in the same manner.



## Usage
To install pyschieber, simply:
```bash
pip install pyschieber

```
pyschieber officially supports Python 3.4, 3.5, 3.6, 3.7, 3.5-dev, 3.6-dev, 3.7-dev, nightly and PyPy3.

### CLI :computer:
Beside of the API, pyschieber provides a CLI client to play the funny Scheiber Jass game.
Currently your opponent will be a bot choosing a random card.

After the pip installation you could run the ```pyschieber``` command on the console to play a game:
```bash
$ pyschieber
Tournament starts, the goal are 1500 points.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Round 1 starts.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Hand cards: 

0 : <BELL:Koennig>
1 : <ACORN:9>
2 : <ROSE:9>
3 : <ACORN:Ober>
4 : <ROSE:Banner>
5 : <SHIELD:8>
6 : <ACORN:Ass>
7 : <ROSE:Ass>
8 : <ROSE:Under>


Trumpf:
0 : Trumpf.OBE_ABE
1 : Trumpf.UNDE_UFE
2 : Trumpf.ROSE
3 : Trumpf.BELL
4 : Trumpf.ACORN
5 : Trumpf.SHIELD
6 : Trumpf.SCHIEBEN

Geschoben: False

Please chose the trumpf by the number from 0 to 6: 
```

## API :clipboard:
The idea of pyschieber is to extend the game with your own implemented player.
Henc schieber provides entry points to fulfill this requirement.

## Environemnt introduction
To get a first feeling for the pyschieber playground let's have a look at a runable example.


1. The first thing you have to do, is to instantiate a new Tournament.
```python
from pyschieber.tournament import Tournament  

tournament = Tournament(point_limit=1500)
```

2. Add the players to your tournament. In our example we use the erratic RandomPlayers Tick, Trick, Track and the GreedyPlayer Dagobert.
```python
from pyschieber.player.random_player import RandomPlayer
from example.greedy_player import GreedyPlayer


players = [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), RandomPlayer(name='Track'),
           GreedyPlayer.with_tournament(name='Dagobert', tournament=tournament)]

[tournament.register_player(player) for player in players]
```

3. Now we are ready to play, let the games begin!
```python
tournament.play()
```

## Build your own Player :runner:
As you might have noticed we registered two different types of players on our tournament.
Thus the idea is to implement your own Player to beat Trick, Trick and Track.

Basically the Player has to provide the methods:
 * set_card(card)
   * called by the dealer to get your cards at the start of every round
 * choose_trumpf(geschoben)
   * called when it's your turn to choose a trumpf, this has to be a generator and is recalled until the chosen trumpf is allowed
 * choose_card()
   * called when it's your turn to choose a card, this has to be a generator and is recalled until the chosen card is allowed

Additionally there is the stich_over() method, that is called after all players had chosen their cards.  

The easiest way to implement your own player is to inherit from the BasePlayer class (due to the fact that Python uses duck typing it is not absolutely necessary), which provieds some basic functionality like store your cards.

To get more familiar with this concept let's have a look at the already mentioned Random Player.
```python
import random

from pyschieber.player.base_player import BasePlayer
from pyschieber.trumpf import Trumpf


class RandomPlayer(BasePlayer):
    def choose_trumpf(self, geschoben):
        return move(choices=list(Trumpf))

    def choose_card(self):
        return move(choices=self.cards)


def move(choices):
    allowed = False
    while not allowed:
        choice = random.choice(choices)
        allowed = yield choice
        if allowed:
            yield None
```
What's going on here?

The Random Player is pretty naive and he simply chooses randomly a card or a trumpf from the list of choices. 
If the turn is not allowed he randomly chooses a new one until the rules of Schieber are satisfied.

Other player examples are the [GreedyPlayer](example/greedy_player.py) or the [CliPlayer](pyschieber/player/cli_player.py).

Now you should be ready to get your hands dirty to implement your own player and beat the random players Tick, Trick and Track! :trophy:

## Enhancements
* Add Wiesen to the game
* Beautify the CLI :trollface:
* Provide a simple network player