# TODO: get list of URLs for main events. For now let's not worry about looping through and getting everything.
# Maybe beterr for now to get a concrete list. Start with 2023??
# Handle the "bracket" results page. Uses different class name.
# Handle mens & womens on same result page. Will need to scrape the link to get the womens page. May then need to scrape each of the round urls for womens too.FIRST20cv

import pandas as pd
from utils.scraper import get_round_data, get_round_links_for_event
from utils.parser import parse_round_data
from utils.storage import save_event_data, heats_to_df

# url = "https://www.worldsurfleague.com/events/0000/anything/2750/anything/results"


def main():
    events_df = pd.read_csv("events.csv")
    for i, row in events_df.iterrows():
        print(f"{i}: {row['event_name']}")
        window = row["event_window"]
        name = row["event_name"]
        location = row["event_location"]
        url = row["event_link"]
        # Find the round links
        tours = get_round_links_for_event(url)

        # Loop through Mens & Womens rounds
        for tour in tours:
            print(f"Tour: {tour.tour_code}")
            heats = []
            for round_link in tour.round_links:
                print(f"Round: {round_link}")
                soup = get_round_data(round_link)
                heats += parse_round_data(soup)

            heats_df = heats_to_df(heats)
            heats_df["tour_code"] = tour.tour_code
            heats_df["event_window"] = window
            heats_df["event_name"] = name
            heats_df["event_location"] = location
            heats_df["event_url"] = url
            save_event_data(heats_df)


if __name__ == "__main__":
    main()
