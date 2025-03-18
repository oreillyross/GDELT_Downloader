
import pandas as pd

from constants import gdelt_columns
from utils.db import get_db_conn
from utils.event_codes import load_event_codes
from utils.sources import get_latest_file, get_title
from utils.get_sql_date import get_sqldate_today
from utils.time_funcs import last_15_minute_mark
from constants import API_URL_TEMPLATE


is_collecting = True
collection_thread = None

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

#TODO Provide a way to change this limit from the front end, through an API call.
def get_event_data(limit=100):
    df = load_latest_gdelt_data()
    events = load_event_codes()
    today = get_sqldate_today()
    event_rows = df[df['SQLDATE'] == today].head(limit)
    result = []
    for _, row in event_rows.iterrows():
        event_code = str(row['EventCode']).zfill(3)
        event_data = {k: (None if pd.isna(v) else v) for k,v in row.items()}
        event_data['EventDescription'] = events.get(event_code, "Unknown Code")
        result.append(event_data)
    print(f"")
    return result

def load_event_data_DB():
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        events = get_event_data()
        print(f"received {len(events)} events, processing...")
        for event in events:
            print(f"processing event: {event}")
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


def fetch_and_save_file():

    global is_collecting
    while is_collecting:
    # Get the current date in the format GDELT expects

        date_str = last_15_minute_mark()

        # Construct the download URL
        url = API_URL_TEMPLATE.format(date=date_str)

        try:
        # Make the request to download the zip file
            print(f"Fetching data from {url}...")
            response = requests.get(url)
            if response.status_code == 200:
                # Save the zip file
                zip_filename = os.path.join(SAVE_DIRECTORY,
                                        f"gdelt_{date_str}.zip")
                with open(zip_filename, 'wb') as f:
                    f.write(response.content)

                # Extract the zip file
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(SAVE_DIRECTORY)
                    print(
                    f"Data saved and extracted to {SAVE_DIRECTORY} at {date_str}"
                )
                for filename in zip_ref.namelist():
                    print(f"extracted: {filename}")

                os.remove(zip_filename)
                print(f"{zip_filename} has been deleted successfuly")
                load_event_data_DB()
            else:
                print(f"Failed to download data from {url}"
                      f"(status code: {response.status_code})")

        except Exception as e:
            print(f"Error fetching data: {e}")

    # Sleep for 15 minutes before fetching again
        time.sleep(15 * 60)  # 15 minutes
