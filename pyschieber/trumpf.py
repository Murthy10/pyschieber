from enum import Enum

from pyschieber.suit import Suit

Trumpf = Enum('Trumpf', ['OBE_ABE', 'UNDE_UFE'] + [str(suit.name) for suit in Suit] + ['SCHIEBEN'])
