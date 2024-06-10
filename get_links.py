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


year = 2024
url = f"https://www.worldsurfleague.com/events/{year}/ct?all=1"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

event_table = soup.find("table", class_="tableType-event")
tbody = event_table.find("tbody")
event_rows = tbody.find_all("tr", class_=re.compile("^event-\d+"))

events = []
for event in event_rows:
    event_window = event.find("td", class_="event-date-range").text
    event_name = event.find("a", class_="event-schedule-details__event-name")
    # remove span from event_name
    try:
        event_name.span.decompose()
    except AttributeError:
        pass
    event_name = event_name.text
    event_link = (
        event.find("a", class_="event-schedule-details__event-name")["href"]
        .replace("main", "results")
        .replace("event", "results")
    )
    event_location = event.find("span", class_="event-schedule-details__location").text
    events.append(Event(event_window, event_name, event_link, event_location))

# Write to csv
keys = events[0].to_dict().keys()

with open("events.csv", "w", newline="") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows([event.to_dict() for event in events])
