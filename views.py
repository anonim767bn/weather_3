from config import TEMPLATE_CITIES, TEMPLATE_MAIN

def page_from_cities(cities: list[str]) -> str:
    cities = '<br>'.join(cities)
    with open(TEMPLATE_CITIES, 'r') as file:
        template = file.read()
    return template.format(cities=cities)


def main_page() -> str:
    with open(TEMPLATE_MAIN, 'r') as file:
        return file.read()
