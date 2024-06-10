from dataclasses import dataclass
from bs4 import BeautifulSoup
import re
import json


@dataclass
class Tour:
    tour_code: str
    sex: str
    event_link: str
    round_links: list[str]

    def __init__(
        self, tour_code: str, sex: str, event_link: list[str], round_links: list[str]
    ):
        self.tour_code = tour_code
        self.sex = sex
        self.event_link = event_link
        self.round_links = round_links

    def from_soup(soup: BeautifulSoup):
        event_data = json.loads(soup.find("a")["data-gtm-event"])

        # The gender heat buttons data will be a list of dictionaries
        if isinstance(event_data, dict):
            return

        # The gender heat buttons should have click_type "heat details click"
        click_type = event_data[0]["click_type"]
        if click_type != "heat details click":
            return

        tour_code = event_data[0]["tour_code"]
        round_name = soup.find("span", class_="round-name").text
        sex = re.search(r"(\w+)'s", round_name).group(1).lower()
        event_link = soup.find("a")["href"]
        round_links = []
        return Tour(tour_code, sex, event_link, round_links)


class Heat:
    def __init__(
        self,
        event_id,
        round_number,
        heat_id,
        heat_number,
        athlete_id,
        singlet,
        name,
        score,
        waves,
    ):
        self.event_id = event_id
        self.round_number = round_number
        self.heat_id = heat_id
        self.heat_number = heat_number
        self.athlete_id = athlete_id
        self.singlet = singlet
        self.name = name
        self.score = score
        self.waves = waves

    def __str__(self):
        return f"{self.event_id} {self.round_number} {self.heat_id} {self.heat_number} {self.athlete_id} {self.singlet} {self.name} {self.score} {self.waves}"

    def __repr__(self):
        return f"{self.event_id} {self.round_number} {self.heat_id} {self.heat_number} {self.athlete_id} {self.singlet} {self.name} {self.score} {self.waves}"

    def __dict__(self):
        return {
            "event_id": self.event_id,
            "round_number": self.round_number,
            "heat_id": self.heat_id,
            "heat_number": self.heat_number,
            "athlete_id": self.athlete_id,
            "singlet": self.singlet,
            "name": self.name,
            "score": self.score,
            "waves": self.waves,
        }

    def from_soup(soup: BeautifulSoup):
        heats = []
        heat_id = soup["data-heat-id"]
        heat_number = soup["data-heat-number"]
        round_number = soup["data-round-number"]
        event_id = soup["data-event-id"]
        athletes = soup.find_all("div", class_="hot-heat-athlete")

        for athlete in athletes:
            athlete_id = athlete["data-athlete-id"]
            singlet = athlete["data-athlete-singlet"]
            name = athlete.find("div", class_="hot-heat-athlete__name").text
            score = athlete.find("div", class_="hot-heat-athlete__score").text
            try:
                waves = athlete.find(
                    "div", class_="hot-heat-athlete__counted-waves"
                ).text
            # TODO better handle injury so no waves
            except:
                waves = "0"

            heats.append(
                Heat(
                    event_id,
                    round_number,
                    heat_id,
                    heat_number,
                    athlete_id,
                    singlet,
                    name,
                    score,
                    waves,
                )
            )
        return heats
