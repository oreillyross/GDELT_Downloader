
import pandas as pd

from constants import gdelt_columns
from utils.db import get_db_conn
from utils.event_codes import load_event_codes
from utils.sources import get_latest_file, get_title


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

#TODO Provide a way to change this limit fromt the front end, through an API call.
def get_event_data(limit=100):
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

def load_event_data_DB():
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        events = get_event_data()
        print(f"received {len(events)} events, processing...")
        for event in events:
            print({event})
            sqldate = str(event.get('SQLDATE'))
            formattedDate = f"{sqldate[:4]}-{sqldate[4:6]}-{sqldate[6:8]}"
            title = get_title(event.get('SOURCEURL'))
            cur.execute("""
                INSERT INTO Events (SQLDATE, Title, EventDescription, Location, Url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (SQLDATE, Url) DO NOTHING
            """, (
                formattedDate,
                title,
                event.get('EventDescription', ''),
                event.get('Actor1Geo_FullName', ''),
                event.get('SOURCEURL', '')
            ))
            print(f"inserted record: {title}")
        conn.commit()
        print("Succesfully loaded events into database")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

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
