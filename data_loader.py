
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

def get_event_data(limit=20):
    df = load_latest_gdelt_data()
    events = load_event_codes()

    event_rows = df.head(limit)
    result = []
    for _, row in event_rows.iterrows():
        event_code = str(row['EventCode']).zfill(3)
        event_data = {k: (None if pd.isna(v) else v) for k,v in row.items()}
        event_data['EventDescription'] = events.get(event_code, "Unknown Code")
        result.append(event_data)
    return result
        

if __name__ == "__main__":
    print("Events as a list")
    events = get_event_data(5)
    print(events)
    # df = load_latest_gdelt_data()
    # events = load_event_codes()
    # print(f"Loaded {len(df)} rows")
    # print("\nFirst few rows:")
    # print(df.head(0))
    # event_rows = df[['Actor1Name', 'Actor2Name', 'EventCode', 'EventBaseCode', 'SOURCEURL']].head(20)
    # print(event_rows)
    # print("\nEvent Descriptions:")
    # for _, row in event_rows.iterrows():
    #     event_code = str(row['EventCode']).zfill(3)       
    #     if event_code in events:
    #         print(f"EventCode {row['EventCode']}: {events[event_code]}")
