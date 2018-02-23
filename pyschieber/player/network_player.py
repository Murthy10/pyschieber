import logging
from enum import Enum
from http.server import HTTPServer, BaseHTTPRequestHandler

from pyschieber.player.base_player import BasePlayer

State = Enum('State', ['CHOOSE_CARD', 'CHOOSE_TRUMPF', 'NO_ACTION'])


# TODO Improve functionality
class NetworkPlayer(BasePlayer, BaseHTTPRequestHandler):
    @classmethod
    def with_port(cls, name, port=3000):
        player = cls(name=name)
        player.port = port
        player.state = dict(STATE=State.NO_ACTION)
        player.chosen_trumpf = None
        player.chosen_card = None
        return cls

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

    def run(self, server_class=HTTPServer, port=3000):
        logging.basicConfig(level=logging.INFO)
        server_address = ('', port)
        httpd = server_class(server_address, NetworkPlayer)
        logging.info('Starting httpd...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
