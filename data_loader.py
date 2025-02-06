
import pandas as pd

from constants import gdelt_columns
from utils.sources import get_latest_file
from utils.event_codes import load_event_codes


def load_latest_gdelt_data(dedupe_urls=True):
    # Get the latest file path
    latest_file = get_latest_file("gdelt_data")
    
    # Load the data into pandas DataFrame
    df = pd.read_csv(latest_file, 
                    delimiter='\t', 
                    header=None,
                    names=gdelt_columns)
    if dedupe_urls:
        df = df.drop_duplicates(subset=['SOURCEURL'])
    return df

if __name__ == "__main__":
    df = load_latest_gdelt_data()
    events = load_event_codes()
    print(f"Loaded {len(df)} rows")
    print("\nFirst few rows:")
    print(df.head(0))
    event_rows = df[['Actor1Name', 'Actor2Name', 'EventCode', 'EventBaseCode']].head()
    print(event_rows)
    print("\nEvent Descriptions:")
    for _, row in event_rows.iterrows():
        if row['EventCode'] in events:
            print(f"EventCode {row['EventCode']}: {events[row['EventCode']]}")
