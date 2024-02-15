import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional
from urllib.parse import unquote

import db

HOST, PORT = '127.0.0.1', 8000
OK = 200
BAD_REQUEST = 400
SERVER_ERROR = 500
CREATED = 201
NO_CONTENT = 204
NOT_FOUND = 404
HEADER_TYPE = 'Content-Type'
HEADER_LEN = 'Content-Length'
POST_KEYS = 'name', 'lat', 'lon'


def json_from_cities(cities: list[tuple]) -> str:
    return json.dumps({name: {'lat': lat, 'lon': lon} for name, lat, lon in cities})


class CustomHandler(SimpleHTTPRequestHandler):
    db_connection, cursor = db.connect()

    def respond(self, code: int, message: Optional[str] = None) -> None:
        self.send_response(code, message)
        self.send_header(HEADER_TYPE, 'text/json')
        self.end_headers()

    def do_GET(self) -> None:
        cities = db.get_cities(self.cursor)
        self.respond(OK)
        self.wfile.write(json_from_cities(cities).encode())

    def do_POST(self) -> None:
        body_len = self.headers.get(HEADER_LEN)
        if not body_len:
            self.respond(BAD_REQUEST)
            return
        try:
            body = json.loads(self.rfile.read(int(body_len)))
        except (json.JSONDecodeError, ValueError):
            self.respond(BAD_REQUEST)
            return
        if any(key not in body for key in POST_KEYS) or len(POST_KEYS) != len(body):
            self.respond(BAD_REQUEST)
            return
        if db.add_city(self.db_connection, self.cursor, tuple([body[key] for key in POST_KEYS])):
            self.respond(CREATED)
        else:
            self.respond(SERVER_ERROR, 'was not posted')

    def do_DELETE(self) -> None:
        if self.path.count('/') != 1:
            self.respond(BAD_REQUEST)
            return
        path = unquote(self.path)
        city_name = path[path.find('/')+1:]
        if db.delete_city(self.db_connection, self.cursor, city_name):
            self.respond(NO_CONTENT)
        else:
            self.respond(NOT_FOUND)


if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), CustomHandler)
    print(f'Server started at {HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped by user')
    finally:
        server.server_close()
