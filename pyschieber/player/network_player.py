import logging, json
import threading
from enum import Enum
from http.server import HTTPServer, BaseHTTPRequestHandler

from pyschieber.player.base_player import BasePlayer

State = Enum('State', ['CHOOSE_CARD', 'CHOOSE_TRUMPF', 'NO_ACTION'])


# TODO Improve functionality, handle race conditions
class NetworkPlayer(BasePlayer):
    @classmethod
    def with_parameters(cls, name, tournament, port=3000):
        player = cls(name=name)
        player.tournament = tournament
        player.port = port
        player.state = State.NO_ACTION
        player.chosen_trumpf = None
        player.chosen_card = None
        return player

    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            trumpf = self.chosen_trumpf
            allowed = yield trumpf
            if allowed:
                yield None
            else:
                self.state = State.CHOOSE_TRUMPF

    def choose_card(self):
        pass

    def stich_over(self):
        pass

    def run(self, server_class=HTTPServer):
        logging.basicConfig(level=logging.INFO)
        server_address = ('', self.port)
        httpd = server_class(server_address, RequestHandler)
        httpd.player = self
        logging.info('Starting httpd...\n')
        try:
            threading.Thread(target=httpd.serve_forever).start()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        state = self.server.player.tournament.get_status()
        state['STATE'] = str(self.server.player.state.name)
        json_string = json.dumps(state)
        self.wfile.write(json_string.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
