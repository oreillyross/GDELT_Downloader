import os
from flask import Flask
from flask_cors import CORS
from threading import Thread

from api.keywords import keywords_bp
from api.events import events_bp
from api.admin import admin_bp
from api.country import country_bp
from api.lookup import lookup_bp
from data_loader import fetch_and_save_file


# Create Flask app
app = Flask(__name__)

app.register_blueprint(keywords_bp)
app.register_blueprint(events_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(country_bp)
app.register_blueprint(lookup_bp)


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


if __name__ == '__main__':
    # Start the background thread
    start_fetching_thread()

    # Start Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)
