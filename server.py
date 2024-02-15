import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional
from urllib.parse import unquote

import db
from config import *
from views import page_from_cities, main_page
from weather import get_weather


def json_from_cities(cities: list[tuple]) -> str:
    return json.dumps({name: {'lat': lat, 'lon': lon} for name, lat, lon in cities})


def cities_to_strings(cities: list[tuple]) -> list:
    return [f'{city}\t{lat}\t{lon}' for city, lat, lon in cities]


class CustomHandler(SimpleHTTPRequestHandler):
    db_connection, cursor = db.connect()

    def router(self):
        if self.path.startswith('/cities'):
            return self.cities()
        elif self.path.startswith('/weather'):
            return self.weather()
        else:
            return main_page()

    def get_query(self) -> dict:
        quest_mark = '?'
        if quest_mark not in self.path:
            return {}
        query = self.path[self.path.index(quest_mark)+1:]
        return {pair.split('=')[0]: pair.split('=')[1] for pair in query.split('&')}

    def weather(self):
        CITY_KEY = 'city'
        query = self.get_query()
        if CITY_KEY in query.keys():
            response = db.get_city(self.cursor, query[CITY_KEY])
            if response:
                return str(get_weather(*response))
        return ''

    def cities(self):
        cities = db.get_cities(self.cursor)
        if GET_RETURNS == 'json':
            body = json_from_cities(cities)
        elif GET_RETURNS == 'html':
            body = page_from_cities(cities_to_strings(cities))
        else:
            body = ''
        return body

    def do_GET(self) -> None:
        self.respond(OK)
        self.wfile.write(self.router().encode())

    def respond(self, code: int, message: Optional[str] = None) -> None:
        self.send_response(code, message)
        self.send_header(HEADER_TYPE, f'text/{GET_RETURNS}')
        self.end_headers()

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
