from collections import namedtuple

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])
Stich = namedtuple('Stich', ['player', 'played_cards', 'trumpf'])
