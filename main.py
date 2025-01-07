import os
import time
import zipfile
from datetime import datetime, timedelta
from threading import Thread

import psycopg2
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from api.keywords import keywords_bp
from data_clean import urlSources

# Create Flask app
app = Flask(__name__)

app.register_blueprint(keywords_bp)

CORS(app)


def get_db_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'])


# Directory where the files will be saved
SAVE_DIRECTORY = "gdelt_data"
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)


def last_15_minute_mark():
    now = datetime.now()
    # Calculate the minutes to subtract to get to the last 15-minute mark
    minutes_to_subtract = now.minute % 15
    # Subtract the minutes and reset seconds and microseconds to zero
    closest_time = now - timedelta(minutes=minutes_to_subtract,
                                   seconds=now.second,
                                   microseconds=now.microsecond)
    return closest_time.strftime('%Y%m%d%H%M') + '00'


# GDELT API URL Template (For daily events)
API_URL_TEMPLATE = "http://data.gdeltproject.org/gdeltv2/{date}.export.CSV.zip"


def fetch_and_save_file():
    while True:
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
            else:
                print(f"Failed to download data from {url}"
                      f"(status code: {response.status_code})")

        except Exception as e:
            print(f"Error fetching data: {e}")

        # Sleep for 15 minutes before fetching again
        time.sleep(15 * 60)  # 15 minutes


# Run the data fetching in a background thread
def start_fetching_thread():
    thread = Thread(target=fetch_and_save_file)
    thread.daemon = True
    thread.start()


# Route to check the server is running
@app.route('/')
def index():
    return "GDELT Data Fetcher is running. Check the logs for data download status."


file_path = "gdelt_data/20250106154500.export.CSV"


@app.route("/api/urls", methods=["GET"])
def getUrls():
    return urlSources(file_path=file_path)


@app.route("/api/goldstein_scales", methods=['GET'])
def get_goldstein_scales():
    query = "SELECT * from cameo_goldstein_scale"
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    finally:
        conn.close()


@app.route('/api/event_codes', methods=['GET'])
def get_event_codes():
    query = "SELECT * from cameo_event_codes"
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    finally:
        conn.close()


@app.route('/api/data', methods=['GET'])
def get_data():
    param_value = request.args.get("country")
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        if param_value:
            query = "SELECT * FROM cameo_countries WHERE label like %s"
        else:
            query = "SELECT * FROM cameo_countries"
        country_query = f"%{param_value}%"
        cur.execute(query, (country_query, ))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    finally:
        conn.close()


if __name__ == '__main__':
    # Start the background thread
    start_fetching_thread()

    # Start Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)
