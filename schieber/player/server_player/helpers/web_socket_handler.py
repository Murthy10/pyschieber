import json
import logging
import asyncio
import websockets

from schieber.player.server_player.helpers import messages

logger = logging.getLogger(__name__)


class WebSocketHandler:
    def __init__(self, bot, address):
        self.bot = bot
        self.address = address
        self.started = False

    async def handler(self):
        async with websockets.connect(self.address) as websocket:
            while self.started:
                try:
                    message = await websocket.recv()
                except websockets.exceptions.ConnectionClosed:
                    self.started = False
                    logger.debug("Stopped, because connection is closed.")
                    break
                logger.debug("Received message {}".format(message))
                payload = json.loads(message)
                type = payload["type"]
                try:
                    payload_data = payload["data"]
                except KeyError:
                    payload_data = {}
                incoming = payload
                answer = None
                try:
                    incoming = messages.create(type, payload_data)
                    answer = self.bot.handle_message(incoming)
                except:
                    logger.exception("Handling {} caused an error".format(incoming))
                if answer:
                    await websocket.send(json.dumps(answer))

    def start(self):
        self.started = True
        asyncio.get_event_loop().run_until_complete(self.handler())
        if not self.bot.is_max_game_reached():
            self.start()

    def stop(self):
        self.started = False
