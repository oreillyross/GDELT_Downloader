import os
import time
import zipfile



import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from api.keywords import keywords_bp
from api.events import events_bp
from api.admin import admin_bp
from data_loader import get_event_data, load_event_data_DB
from utils.db import get_db_conn

# Create Flask app
app = Flask(__name__)

app.register_blueprint(keywords_bp)
app.register_blueprint(events_bp)
app.register_blueprint(admin_bp)
CORS(app)




# Directory where the files will be saved
SAVE_DIRECTORY = "gdelt_data"
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)










# Run the data fetching in a background thread
def start_fetching_thread():
    thread = Thread(target=fetch_and_save_file)
    thread.daemon = True
    thread.start()



file_path = "gdelt_data/20250205084500.export.CSV"





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
