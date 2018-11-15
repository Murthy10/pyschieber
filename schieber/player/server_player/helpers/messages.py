from enum import Enum

from schieber.player.server_player.helpers.server_cards import ServerCard, Color


class GameType:
    def __init__(self, mode, trumpfColor=None):
        self.mode = mode

        if trumpfColor is not None:
            self.trumpf_color = Color[trumpfColor]

    def __repr__(self):
        return "{} | {}".format(self.mode, self.trumpf_color)

    def to_dict(self):
        if hasattr(self, 'trumpf_color'):
            return dict(mode=self.mode,
                        trumpfColor=self.trumpf_color.name)

        return dict(mode=self.mode)


class RoundScore:
    def __init__(self, name, points, currentRoundPoints):
        self.team_name = name
        self.total_points = points
        self.current_game_points = currentRoundPoints

    def __str__(self):
        return "Score: Team: {0}, Total points: {1}, Current points: {2}".format(self.team_name, self.total_points,
                                                                                 self.current_game_points)


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def is_member(self, player):
        for member in self.players:
            if member.id == player.id:
                return True

        return False

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "{0} {1}".format(self.name, self.players)


class Player:
    def __init__(self, id, seatId, name):
        self.id = id
        self.seatId = seatId
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "{0} [{1}]".format(self.name, self.seatId)


MessageType = Enum('MessageType',
                   ['REQUEST_PLAYER_NAME', 'CHOOSE_PLAYER_NAME', 'BROADCAST_TEAMS', 'DEAL_CARDS', 'REQUEST_TRUMPF',
                    'CHOOSE_TRUMPF', 'REJECT_TRUMPF', 'BROADCAST_TRUMPF', 'BROADCAST_STICH', 'BROADCAST_WINNER_TEAM',
                    'BROADCAST_GAME_FINISHED', 'PLAYED_CARDS', 'REQUEST_CARD', 'CHOOSE_CARD', 'REJECT_CARD',
                    'REQUEST_SESSION_CHOICE', 'CHOOSE_SESSION', 'SESSION_JOINED', 'BROADCAST_SESSION_JOINED',
                    'BAD_MESSAGE', 'BROADCAST_TOURNAMENT_RANKING_TABLE', 'START_TOURNAMENT',
                    'BROADCAST_TOURNAMENT_STARTED', 'JOIN_BOT'])


def create_request_player_name():
    return dict(
        type=MessageType.REQUEST_PLAYER_NAME
    )


def create_choose_player_name(playerName):
    return dict(
        type=MessageType.CHOOSE_PLAYER_NAME.name,
        data=playerName
    )


def create_broadcast_teams(data):
    teams = []
    for team_info in data:
        team = Team(team_info["name"], [Player(**player_info) for player_info in team_info["players"]])
        teams.append(team)

    return dict(
        type=MessageType.BROADCAST_TEAMS,
        data=teams
    )


def create_deal_cards(cards):
    return dict(
        type=MessageType.DEAL_CARDS,
        data=[ServerCard(item["number"], item["color"]) for item in cards]
    )


def create_request_trumpf(geschoben):
    return dict(
        type=MessageType.REQUEST_TRUMPF,
        data=geschoben
    )


def create_reject_trumpf(gameType):
    return dict(
        type=MessageType.REJECT_TRUMPF,
        data=GameType(**gameType)
    )


def create_choose_trumpf(gameType):
    return dict(
        type=MessageType.CHOOSE_TRUMPF.name,
        data=gameType.to_dict()
    )


def create_broadcast_trumpf(gameType):
    return dict(
        type=MessageType.BROADCAST_TRUMPF,
        data=GameType(**gameType)
    )


def create_broadcast_stich(data):
    score = [RoundScore(**score) for score in data.pop("teams")]

    return dict(
        type=MessageType.BROADCAST_STICH,
        data=dict(
            score=score,
            playedCards=[ServerCard(**card) for card in data.pop("playedCards")],
            winner=Player(**data)
        )
    )


def create_broadcast_game_finished(data):
    return dict(
        type=MessageType.BROADCAST_GAME_FINISHED,
        data=[RoundScore(**score) for score in data]
    )


def create_broadcast_winner_team(score):
    return dict(
        type=MessageType.BROADCAST_WINNER_TEAM,
        data=RoundScore(**score)
    )


def create_played_cards(played_cards):
    return dict(
        type=MessageType.PLAYED_CARDS,
        data=[ServerCard(item["number"], item["color"]) for item in played_cards]
    )


def create_request_card(cards):
    return dict(
        type=MessageType.REQUEST_CARD,
        data=cards
    )


def create_choose_card(card):
    return dict(
        type=MessageType.CHOOSE_CARD.name,
        data=card.to_dict()
    )


def create_reject_card(card):
    return dict(
        type=MessageType.REJECT_CARD,
        data=ServerCard(card["number"], card["color"])
    )


def create_request_session_choice(*availableSessions):
    return dict(
        type=MessageType.REQUEST_SESSION_CHOICE,
        data=availableSessions
    )


def create_choose_session(sessionChoice="AUTOJOIN", sessionName="Session 1", sessionType="TOURNAMENT",
                          asSpectator=False,
                          chosenTeamIndex=0):
    return dict(
        type=MessageType.CHOOSE_SESSION.name,
        data=dict(
            sessionChoice=sessionChoice,
            sessionName=sessionName,
            sessionType=sessionType,
            asSpectator=asSpectator,
            chosenTeamIndex=chosenTeamIndex
        )
    )


def create_session_joined(sessionName, player, playersInSession):
    return dict(
        type=MessageType.SESSION_JOINED,
        data={
            sessionName,
            player,
            playersInSession
        }
    )


def create_broadcast_session_joined(data):
    return dict(
        type=MessageType.BROADCAST_SESSION_JOINED,
        data={
            "sessionName": data["sessionName"],
            "player": Player(**data["player"]),
            "playersInSession": [Player(**player) for player in data["playersInSession"]]
        }
    )


def create_bad_message(message):
    return dict(
        type=MessageType.BAD_MESSAGE,
        data=message
    )


def create_tournament_ranking_table(rankingTable):
    return dict(
        type=MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE,
        data=rankingTable
    )


def create_start_tournament():
    return dict(
        type=MessageType.START_TOURNAMENT
    )


def create_broadcast_tournament_started():
    return dict(
        type=MessageType.BROADCAST_TOURNAMENT_STARTED
    )


def create_join_bot(data):
    return dict(
        type=MessageType.JOIN_BOT,
        data=data
    )


def create(type, *args):
    if isinstance(type, MessageType):
        messageType = type
    else:
        try:
            messageType = MessageType[type]
        except:
            raise 'Unknown message type ' + type

    if messageType == MessageType.REQUEST_PLAYER_NAME:
        return create_request_player_name()
    elif messageType == MessageType.CHOOSE_PLAYER_NAME:
        return create_choose_player_name(*args)
    elif messageType == MessageType.BROADCAST_TEAMS:
        return create_broadcast_teams(*args)
    elif messageType == MessageType.DEAL_CARDS:
        return create_deal_cards(*args)
    elif messageType == MessageType.REQUEST_TRUMPF:
        return create_request_trumpf(*args)
    elif messageType == MessageType.REJECT_TRUMPF:
        return create_reject_trumpf(*args)
    elif messageType == MessageType.CHOOSE_TRUMPF:
        return create_choose_trumpf(*args)
    elif messageType == MessageType.BROADCAST_TRUMPF:
        return create_broadcast_trumpf(*args)
    elif messageType == MessageType.BROADCAST_WINNER_TEAM:
        return create_broadcast_winner_team(*args)
    elif messageType == MessageType.BROADCAST_STICH:
        return create_broadcast_stich(*args)
    elif messageType == MessageType.BROADCAST_GAME_FINISHED:
        return create_broadcast_game_finished(*args)
    elif messageType == MessageType.PLAYED_CARDS:
        return create_played_cards(*args)
    elif messageType == MessageType.REQUEST_CARD:
        return create_request_card(*args)
    elif messageType == MessageType.CHOOSE_CARD:
        return create_choose_card(*args)
    elif messageType == MessageType.REJECT_CARD:
        return create_reject_card(*args)
    elif messageType == MessageType.REQUEST_SESSION_CHOICE:
        return create_request_session_choice(*args)
    elif messageType == MessageType.CHOOSE_SESSION:
        return create_choose_session(*args)
    elif messageType == MessageType.SESSION_JOINED:
        return create_session_joined(*args)
    elif messageType == MessageType.BROADCAST_SESSION_JOINED:
        return create_broadcast_session_joined(*args)
    elif messageType == MessageType.BAD_MESSAGE:
        return create_bad_message(*args)
    elif messageType == MessageType.BROADCAST_TOURNAMENT_RANKING_TABLE:
        return create_tournament_ranking_table(*args)
    elif messageType == MessageType.START_TOURNAMENT:
        return create_start_tournament()
    elif messageType == MessageType.BROADCAST_TOURNAMENT_STARTED:
        return create_broadcast_tournament_started()
    elif messageType == MessageType.JOIN_BOT:
        return create_join_bot(args)
    else:
        raise 'Unknown message type ' + messageType
