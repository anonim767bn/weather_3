CITIES_TABLE = 'city'
CITIES_SELECT = f'select * from {CITIES_TABLE}'
CITIES_INSERT = f'insert into {CITIES_TABLE} (name, latitude, longtitude) VALUES (%s, %s, %s)'
CITIES_DELETE = f'delete from {CITIES_TABLE} WHERE name=%s'
