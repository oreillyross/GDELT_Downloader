import argparse
import sqlite3


def read_gdelt_events(db_path, limit=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get column names
    cursor.execute("PRAGMA table_info(events)")
    columns = [column[1] for column in cursor.fetchall()]

    # Fetch data
    cursor.execute(f"SELECT * FROM events LIMIT {limit}")
    rows = cursor.fetchall()

    # Print column names
    print("Columns:", ", ".join(columns))

    # Print rows
    for row in rows:
        print("\nEvent:")
        for col, value in zip(columns, row):
            print(f"  {col}: {value}")

    # Print total number of events
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]
    print(f"\nTotal number of events in the database: {total_events}")

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read GDELT events from SQLite database")
    parser.add_argument("db_path", help="Path to the SQLite database file")
    parser.add_argument("--limit", type=int, default=10, help="Number of events to display (default: 10)")
    args = parser.parse_args()

    read_gdelt_events(args.db_path, args.limit)