from utils.models import Heat, Tour
import pandas as pd


def heats_to_df(heats: list[Heat]):
    heat_df = pd.DataFrame([heat.__dict__() for heat in heats])
    # Drop dupes by heat_id & name
    heat_df = heat_df.drop_duplicates(subset=["heat_id", "name"])
    return heat_df


def save_event_data(heats_df: pd.DataFrame):
    tour_code = heats_df["tour_code"].iloc[0]
    event_id = heats_df["event_id"].iloc[0]
    output_path = f"output/{tour_code}_{event_id}_heat_data.csv"
    heats_df.to_csv(output_path, index=False)
