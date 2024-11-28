import pandas as pd
import os
from datetime import datetime

from utils import get_latest_file
from constants import gdelt_columns

# Check current working directory
print("Current Working Directory:", os.getcwd())

# List files in gdelt_data directory
print("Files in 'gdelt_data':", os.listdir('gdelt_data'))

# Define the file path
file_path = get_latest_file("gdelt_data")

# Load the tab-delimited CSV file
try:
    events = pd.read_csv(file_path, delimiter='\t', header=None) 
    print("Data loaded successfully!")
    events.columns = gdelt_columns
    events['SQLDATE'] = pd.to_datetime(events['SQLDATE'], format='%Y%m%d')
    today = pd.to_datetime(datetime.now().date())
    today_events = events[events['SQLDATE'] == today ]
    print(f"before dropping duplicates count: {len(today_events)}")
    deduped = today_events.drop_duplicates(subset=["SOURCEURL"])
    print(f"after dropping duplicates count: {len(deduped)}")
    print(deduped.head(20))
    print(events.iloc[:]) 
    html_table = deduped.to_html()
    with open("data.html", "w") as f:
      f.write(html_table)

except FileNotFoundError:
    print(f"File not found: {file_path}")
except pd.errors.EmptyDataError:
    print("No data: The file is empty.")
except pd.errors.ParserError:
    print("Parsing error: Check the file format.")
except Exception as e:
    print(f"An error occurred: {e}")
