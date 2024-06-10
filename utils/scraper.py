from bs4 import BeautifulSoup
from utils.models import Tour
import requests

BASE_URL = "https://www.worldsurfleague.com"


def get_round_links(soup: BeautifulSoup) -> list:
    round_nav_items = soup.find_all("div", class_="post-event-watch-round-nav__item")
    tours = [Tour.from_soup(i) for i in round_nav_items]
    tours = [tour for tour in tours if tour is not None]

    # Get the round links on each tour page
    for tour in tours:
        r = requests.get(BASE_URL + tour.event_link)
        soup = BeautifulSoup(r.text, "html.parser")
        round_links = soup.find_all("a", attrs={"data-request-name": "postEventWatch"})
        tour.round_links = [i["href"] for i in round_links]

    return tours


def get_round_links_for_event(url: str) -> list:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return get_round_links(soup)


def get_round_data(url: str) -> BeautifulSoup:
    base_url = "https://www.worldsurfleague.com"
    r = requests.get(base_url + url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup
