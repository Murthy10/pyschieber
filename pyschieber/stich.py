from collections import namedtuple

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])
Stich = namedtuple('Stich', ['player', 'played_cards', 'trumpf'])


def played_cards_dict(played_card):
    return {
        'player_id': played_card.player.id,
        'card': str(played_card.card)
    }


def stich_dict(stich):
    return {
        'player_id': stich.player.id,
        'trumpf': stich.trumpf.name,
        'played_cards': [played_cards_dict(played_card) for played_card in stich.played_cards]
    }
