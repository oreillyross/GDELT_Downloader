from flask import Blueprint, jsonify, request
from threading import Thread


from utils.db import get_db_conn

is_collecting = True
collection_thread = None

admin_bp = Blueprint("Admin", __name__)

@admin_bp.route("/api/start_collecting", methods=["POST"])
def start_collection():
    global is_collecting, collection_thread
    if not is_collecting:
        is_collecting = True
        thread = Thread(target=fetch_and_save_file)
        thread.daemon = True
        thread.start()
        return jsonify({"message": "Data Collection started"}), 200
    return jsonify({"message": "Data collection ongoing"})


@admin_bp.route("/api/stop_collecting", methods=["POST"])
def stop_collecting():
    global is_collecting, collection_thread
    if is_collecting:
        is_collecting = False
        return jsonify({"message": "Data collection stopped"}), 200
    return jsonify({"message": "Data collection not running."}), 200


@admin_bp.route("/api/collection_status", methods=["GET"])
def collection_status():
    global is_collecting
    return jsonify({"Collection Status": is_collecting}), 200


# Route to check the server is running
@admin_bp.route('/')
def index():
    return "GDELT Data Fetcher is running. Check the logs for data download status."

