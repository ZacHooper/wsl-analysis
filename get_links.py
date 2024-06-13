import requests
from bs4 import BeautifulSoup
import re
import csv


class Event:
    def __init__(self, event_window, event_name, event_link, event_location):
        self.event_window = event_window
        self.event_name = event_name
        self.event_link = event_link
        self.event_location = event_location

    def __str__(self):
        return f"{self.event_window} {self.event_name} {self.event_link} {self.event_location}"

    def to_dict(self):
        return {
            "event_window": self.event_window,
            "event_name": self.event_name,
            "event_link": self.event_link,
            "event_location": self.event_location,
        }

    def from_soup(soup):
        event_window = soup.find("td", class_="event-date-range").text
        event_name = soup.find("a", class_="event-schedule-details__event-name")
        # remove span from event_name
        try:
            event_name.span.decompose()
        except AttributeError:
            pass
        event_name = event_name.text
        event_link = (
            soup.find("a", class_="event-schedule-details__event-name")["href"]
            .replace("main", "results")
            .replace("event", "results")
        )
        event_location = soup.find(
            "span", class_="event-schedule-details__location"
        ).text
        return Event(event_window, event_name, event_link, event_location)


def get_event_links(year: int) -> None:
    url = f"https://www.worldsurfleague.com/events/{year}/ct?all=1"

    # Load Page
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Find all event elements
    event_table = soup.find("table", class_="tableType-event")
    tbody = event_table.find("tbody")
    event_rows = tbody.find_all("tr", class_=re.compile("^event-\d+"))

    # Parse events
    events = [Event.from_soup(event) for event in event_rows]

    # Write to csv
    keys = events[0].to_dict().keys()

    with open("events.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows([event.to_dict() for event in events])


if __name__ == "__main__":
    get_event_links(2023)
