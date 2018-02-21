[![Build Status](https://travis-ci.org/Murthy10/pyschieber.svg?branch=master)](https://travis-ci.org/Murthy10/pyschieber)
<a href="url"><img src="/docs/images/jass.png" align="right" width="300" ></a>
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

### CLI
Beside of the API, pyschieber provides a CLI client to play the funny Scheiber Jass game.
Currently your opponent will be a bot choosing a random card.

After the pip installation you could run the ```pyschieber``` command on the console to play a game:
```bash
$ pyschieber
------------------------------------------------------------------------------------------------------------------------
Round 1 starts.
------------------------------------------------------------------------------------------------------------------------
Hand cards: 

0 : <ACORN:Under>
1 : <ROSE:9>
2 : <SHIELD:Banner>
3 : <SHIELD:Ober>
4 : <BELL:Under>
5 : <SHIELD:Koennig>
6 : <BELL:8>
7 : <BELL:Koennig>
8 : <ACORN:Koennig>


Trumpf:
0 : Trumpf.OBE_ABE
1 : Trumpf.UNDE_UFE
2 : Trumpf.ROSE
3 : Trumpf.BELL
4 : Trumpf.ACORN
5 : Trumpf.SHIELD
Please chose the trumpf by the number from 0 to 5: 

```



### API
Content will follow...




## TODO
* Implement Wies
* Enhance documentation
* Architectural refactoring
* Beautify the CLI
* Implement Network Player
