from enum import Enum

from pyschieber.suit import Suit

Trumpf = Enum('Trumpf', ['OBE_ABE', 'UNDE_UFE'] + [suit.value for suit in Suit])

