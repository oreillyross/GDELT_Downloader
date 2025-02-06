
import pandas as pd

from constants import gdelt_columns
from utils import get_latest_file


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
    print(f"Loaded {len(df)} rows")
    print("\nFirst few rows:")
    print(df.head(0))
    print(df[['Actor1Name', 'Actor2Name', 'EventCode', 'EventBaseCode']].head())
