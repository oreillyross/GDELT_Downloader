import argparse
import csv
import sqlite3

from constants import gdelt_columns


def create_events_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        GLOBALEVENTID INTEGER PRIMARY KEY,
        SQLDATE INTEGER,
        MonthYear INTEGER,
        Year INTEGER,
        FractionDate REAL,
        Actor1Code TEXT,
        Actor1Name TEXT,
        Actor1CountryCode TEXT,
        Actor1KnownGroupCode TEXT,
        Actor1EthnicCode TEXT,
        Actor1Religion1Code TEXT,
        Actor1Religion2Code TEXT,
        Actor1Type1Code TEXT,
        Actor1Type2Code TEXT,
        Actor1Type3Code TEXT,
        Actor2Code TEXT,
        Actor2Name TEXT,
        Actor2CountryCode TEXT,
        Actor2KnownGroupCode TEXT,
        Actor2EthnicCode TEXT,
        Actor2Religion1Code TEXT,
        Actor2Religion2Code TEXT,
        Actor2Type1Code TEXT,
        Actor2Type2Code TEXT,
        Actor2Type3Code TEXT,
        IsRootEvent INTEGER,
        EventCode TEXT,
        EventBaseCode TEXT,
        EventRootCode TEXT,
        QuadClass INTEGER,
        GoldsteinScale REAL,
        NumMentions INTEGER,
        NumSources INTEGER,
        NumArticles INTEGER,
        AvgTone REAL,
        Actor1Geo_Type INTEGER,
        Actor1Geo_FullName TEXT,
        Actor1Geo_CountryCode TEXT,
        Actor1Geo_ADM1Code TEXT,
        Actor1Geo_ADM2Code TEXT,
        Actor1Geo_Lat REAL,
        Actor1Geo_Long REAL,
        Actor1Geo_FeatureID TEXT,
        Actor2Geo_Type INTEGER,
        Actor2Geo_FullName TEXT,
        Actor2Geo_CountryCode TEXT,
        Actor2Geo_ADM1Code TEXT,
        Actor2Geo_ADM2Code TEXT,
        Actor2Geo_Lat REAL,
        Actor2Geo_Long REAL,
        Actor2Geo_FeatureID TEXT,
        ActionGeo_Type INTEGER,
        ActionGeo_FullName TEXT,
        ActionGeo_CountryCode TEXT,
        ActionGeo_ADM1Code TEXT,
        ActionGeo_ADM2Code TEXT,
        ActionGeo_Lat REAL,
        ActionGeo_Long REAL,
        ActionGeo_FeatureID TEXT,
        DATEADDED INTEGER,
        SOURCEURL TEXT
    )
    ''')


def read_gdelt_file(file_path, db_path):
 
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_events_table(cursor)
    event_data = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            event_data = dict(zip(gdelt_columns, row))

        
        
        numeric_fields = [
            'GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'IsRootEvent',
            'QuadClass', 'NumMentions', 'NumSources', 'NumArticles',
            'Actor1Geo_Type', 'Actor2Geo_Type', 'ActionGeo_Type', 'DATEADDED'
        ]
        for field in numeric_fields:
            event_data[field] = int(
                event_data[field]) if event_data[field] else None

            for field in [
                    'FractionDate', 'GoldsteinScale', 'AvgTone',
                    'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor2Geo_Lat',
                    'Actor2Geo_Long', 'ActionGeo_Lat', 'ActionGeo_Long'
            ]:
                event_data[field] = float(
                    event_data[field]) if event_data[field] else None

            # Insert data into the database
            cursor.execute(
                '''
            INSERT OR REPLACE INTO events ({})
            VALUES ({})
            '''.format(', '.join(gdelt_columns),
                       ', '.join(['?' for _ in gdelt_columns])),
                [event_data[col] for col in gdelt_columns])

    conn.commit()
    conn.close()
    print(f"Data has been successfully imported into {db_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read GDELT Data and save to SQLite")
    
    parser.add_argument("filename", help="Path to the GDELT file")
    
    parser.add_argument("--db",
                        default="gdelt.db",
                        help="Path to the SQLite database file")
    args = parser.parse_args()
    
    read_gdelt_file(args.filename, args.db)
