import json
import logging
from enum import Enum

from schieber.player.server_player.helpers.parser.game_type_parser import pyschieber_trumpf_to_game_type, \
    game_type_to_pyschieber_trumpf

from schieber.player.server_player.helpers import messages
from schieber.player.server_player.helpers.messages import MessageType
from schieber.player.server_player.helpers.parser.card_parser import pyscheiber_card_to_challenge_card, \
    challenge_card_to_pyschieber_card
from schieber.player.server_player.helpers.server_cards import ServerCard
from schieber.player.server_player.helpers.web_socket_handler import WebSocketHandler
from schieber.rules.stich_rules import card_allowed
from schieber.rules.trumpf_rules import trumpf_allowed

logger = logging.getLogger(__name__)

SessionType = Enum('SessionType', ['TOURNAMENT', 'SINGLE_GAME'])


class ServerPlayer:
    def __init__(self, pyschieber_bot, session_name, server_address, chosen_team_index=0, max_games=-1):
        self.pyschieber_bot = pyschieber_bot
        self.name = pyschieber_bot.name
        self.session_name = session_name
        self.server_address = server_address
        self.chosen_team_index = chosen_team_index

        self.teams = None
        self.hand_cards = []
        self.won_stich_in_game = []
        self.last_round_points = 0
        self.players_in_session = []
        self.table = []
        self.stiche = []
        self.chosen_card = None
        self.points = [0, 0]
        self.game_type = None
        self.geschoben = None

        self.first_player_in_stich = 0
        self.trumpf_choosing_player = 0
        self.count_games = 0
        self.max_games = max_games
        self.connection = None
        self.websocket_handler = WebSocketHandler(bot=self, address=server_address)

    def start(self):
        logger.info("Connecting to {}".format(self.server_address))
        self.websocket_handler.start()

    def handle_message(self, message):
        answer = None
        type = message["type"]
        if isinstance(type, MessageType):
            message_type = type
        else:
            message_type = MessageType[type]

        try:
            data = message["data"]
        except KeyError:
            data = {}

        if message_type == MessageType.REQUEST_PLAYER_NAME:
            logger.info('MyName: ' + self.name)
            answer = messages.create(MessageType.CHOOSE_PLAYER_NAME, self.name)

        elif message_type == MessageType.REQUEST_SESSION_CHOICE:
            answer = messages.create(MessageType.CHOOSE_SESSION,
                                     "AUTOJOIN",
                                     self.session_name,
                                     SessionType.SINGLE_GAME.name,
                                     False,
                                     self.chosen_team_index)
            logger.info('session choice answer: %s', answer)

        elif message_type == MessageType.DEAL_CARDS:
            self.last_round_points = 0
            self.hand_cards = data
            self.pyschieber_bot.cards = [challenge_card_to_pyschieber_card(card) for card in self.hand_cards]

        elif message_type == MessageType.REQUEST_TRUMPF:
            game_type = self.handle_request_trumpf()
            answer = messages.create(MessageType.CHOOSE_TRUMPF, game_type)

        elif message_type == MessageType.REQUEST_CARD:
            card = self.handle_request_card(data)
            answer = messages.create(MessageType.CHOOSE_CARD, card)

        elif message_type == MessageType.PLAYED_CARDS:
            self.handle_played_cards(data)

        elif message_type == MessageType.REJECT_CARD:
            self.handle_reject_card(data)

        elif message_type == MessageType.BROADCAST_GAME_FINISHED:
            self.handle_game_finished()
            self.won_stich_in_game = []
            # if not self.is_max_game_reached():
            # self.websocket_handler.start()
        elif message_type == MessageType.BROADCAST_SESSION_JOINED:
            player = data["player"]
            if self.name == player.name:
                self.player = player
                self.pyschieber_bot.id = player.seatId
                self.pyschieber_bot.game_started()
            self.players_in_session = data["playersInSession"]

        elif message_type == MessageType.BROADCAST_STICH:
            winner = data["winner"]
            self.first_player_in_stich = winner.seatId
            won_stich = self.in_my_team(winner)
            self.won_stich_in_game.append(won_stich)
            total_points = self.total_points(data["score"])
            current_game_points = self.current_game_points(data["score"])

            if won_stich:
                round_points = current_game_points - self.last_round_points
            else:
                round_points = 0
            self.last_round_points = current_game_points
            self.table = self.table_to_pyschieber_played_cards(data['playedCards'])
            self.handle_stich(winner, round_points, total_points)
            for i, score in enumerate(data['score']):
                self.points[i] = score.total_points

        elif message_type == MessageType.BROADCAST_TOURNAMENT_STARTED:
            pass
        elif message_type == MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE:
            pass
        elif message_type == MessageType.BROADCAST_TEAMS:
            self.teams = data
            for team in self.teams:
                if team.is_member(self.player):
                    self.my_team = team

        elif message_type == MessageType.BROADCAST_TRUMPF:
            self.handle_trumpf(data)

        elif message_type == MessageType.BROADCAST_WINNER_TEAM:
            self.first_player_in_stich = 0
            self.trumpf_choosing_player = 0
            self.count_games += 1
            print(data)
        else:
            logger.warning("Sorry, i cannot handle this message: " + json.dumps(message))
        return answer

    def handle_played_cards(self, played_cards):
        self.update_hand(played_cards)
        card = challenge_card_to_pyschieber_card(played_cards[-1])
        state = self.pyschieber_state()
        self.pyschieber_bot.move_made(self.first_player_in_stich, card, state)
        self.first_player_in_stich = (self.first_player_in_stich + 1) % 4

    def handle_request_trumpf(self):
        generator = self.pyschieber_bot.choose_trumpf(geschoben=self.geschoben)
        chosen_trumpf = None
        allowed = False
        while not allowed:
            chosen_trumpf = next(generator)
            allowed = self.is_trumpf_allowed(chosen_trumpf=chosen_trumpf)
            generator.send(allowed)
        return pyschieber_trumpf_to_game_type(chosen_trumpf)

    def handle_trumpf(self, game_type):
        self.geschoben = game_type.mode == "SCHIEBE"  # just remember if it's a geschoben match
        self.game_type = game_type

    def handle_stich(self, winner, round_points, total_points):
        self.pyschieber_stich(winner.seatId)
        self.pyschieber_bot.stich_over(self.pyschieber_state())
        self.table = []

    def handle_game_finished(self):
        self.last_round_points = 0
        self.stiche = []
        self.points = [0, 0]
        self.trumpf_choosing_player = (self.trumpf_choosing_player + 1) % 4
        self.first_player_in_stich = self.trumpf_choosing_player

    def handle_reject_card(self, data):
        logger.warning(" ######   SERVER REJECTED CARD   #######")
        logger.warning("Player: {}".format(self.pyschieber_bot.name))
        logger.warning("Rejected card: %s", data)
        logger.warning("Hand cards schieber: %s", self.pyschieber_bot.cards)
        logger.warning("Hand cards: %s", self.hand_cards)
        logger.warning("Table cards: %s", self.table)
        logger.warning("Gametype: %s", self.game_type)

    def handle_request_card(self, table_cards):
        self.table = self.table_to_pyschieber_played_cards(table_cards)
        generator = self.pyschieber_bot.choose_card(state=self.pyschieber_state())
        chosen_card = None
        allowed = False
        while not allowed:
            chosen_card = next(generator)
            allowed = self.is_card_allowed(choosen_card=chosen_card, table_cards_dict=table_cards)
            generator.send(allowed)
        card = pyscheiber_card_to_challenge_card(chosen_card)
        self.chosen_card = chosen_card
        return card

    def in_my_team(self, winner):
        return self.my_team.is_member(winner)

    def current_game_points(self, scores):
        for score in scores:
            if self.my_team.name == score.team_name:
                return score.current_game_points
        return 0

    def total_points(self, scores):
        for score in scores:
            if self.my_team.name == score.team_name:
                return score.total_points
        return 0

    def update_hand(self, played_cards):
        last_played_card = played_cards[-1]
        for i in range(len(self.hand_cards)):
            if last_played_card.number == self.hand_cards[i].number \
                    and last_played_card.color == self.hand_cards[i].color:
                self.hand_cards.pop(i)
                self.pyschieber_bot.cards.remove(self.chosen_card)
                break

    def pyschieber_state(self):
        trumpf = game_type_to_pyschieber_trumpf(self.game_type)
        state = {'trumpf': trumpf.name, 'geschoben': self.geschoben,
                 'teams': [{'points': self.points[0]}, {'points': self.points[1]}],
                 'table': self.table, 'point_limit': 2500, 'stiche': self.stiche}
        return state

    def table_to_pyschieber_played_cards(self, table_cards_dict):
        table_cards = []
        if table_cards_dict:
            if isinstance(table_cards_dict[0], ServerCard):
                table_cards = table_cards_dict
            else:
                table_cards = [ServerCard(number=card['number'], color=card['color']) for card in table_cards_dict]
        table = [challenge_card_to_pyschieber_card(card) for card in table_cards]
        first_player_id = (self.pyschieber_bot.id - len(table)) % 4
        played_cards = []
        for card in table:
            played_cards.append({'player_id': first_player_id, 'card': str(card)})
            first_player_id = (first_player_id + 1) % 4
        return played_cards

    def is_card_allowed(self, choosen_card, table_cards_dict):
        table_cards = [ServerCard(number=card['number'], color=card['color']) for card in table_cards_dict]
        table = [challenge_card_to_pyschieber_card(card) for card in table_cards]
        trumpf = game_type_to_pyschieber_trumpf(self.game_type)
        return card_allowed(table_cards=table, chosen_card=choosen_card, hand_cards=self.pyschieber_bot.cards,
                            trumpf=trumpf)

    def is_trumpf_allowed(self, chosen_trumpf):
        return trumpf_allowed(chosen_trumpf, self.geschoben)

    def pyschieber_stich(self, stich_player_id):
        trumpf = game_type_to_pyschieber_trumpf(self.game_type)
        stich = {
            'player_id': stich_player_id,
            'trumpf': trumpf,
            'played_cards': self.table[:]
        }
        self.stiche.append(stich)

    def is_max_game_reached(self):
        return 0 <= self.max_games <= self.count_games
