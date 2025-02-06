
import pandas as pd
from utils import get_latest_file
from constants import gdelt_columns

def load_latest_gdelt_data():
    # Get the latest file path
    latest_file = get_latest_file("gdelt_data")
    
    # Load the data into pandas DataFrame
    df = pd.read_csv(latest_file, 
                    delimiter='\t', 
                    header=None,
                    names=gdelt_columns)
    
    return df

if __name__ == "__main__":
    df = load_latest_gdelt_data()
    print(f"Loaded {len(df)} rows")
    print("\nFirst few rows:")
    print(df.head())
