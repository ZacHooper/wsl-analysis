from bs4 import BeautifulSoup
from utils.models import Heat
from bs4 import ResultSet


def find_cards_on_page(soup: BeautifulSoup) -> ResultSet:
    class_name = "post-event-watch-heat-grid__heat"
    cards = soup.find_all("div", class_=class_name)
    if len(cards) == 0:
        class_name = "post-event-watch-heat-bracket-stage__heat"
        cards = soup.find_all("div", class_=class_name)
    return cards


def parse_cards(cards: ResultSet):
    h = [Heat.from_soup(card) for card in cards]
    # Flatten
    return [item for sublist in h for item in sublist]


def parse_round_data(soup: BeautifulSoup) -> list[Heat]:
    cards = find_cards_on_page(soup)
    parsed_cards = parse_cards(cards)
    return parsed_cards
