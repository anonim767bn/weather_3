CITIES_TABLE = 'city'
CITIES_SELECT = f'select * from {CITIES_TABLE}'
CITIES_INSERT = f'insert into {CITIES_TABLE} (name, latitude, longtitude) VALUES (%s, %s, %s)'
CITIES_DELETE = f'delete from {CITIES_TABLE} WHERE name=%s'
CITY_SINGLE_SELECT = f'select latitude, longtitude from {CITIES_TABLE} WHERE name=%s'

YANDEX_URL = 'https://api.weather.yandex.ru/v2/informers'

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
GET_RETURNS = 'html' # switch to json if you like

TEMPLATE_CITIES = 'cities.html'
TEMPLATE_MAIN = 'index.html'
