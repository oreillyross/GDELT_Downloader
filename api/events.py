from flask import Blueprint, jsonify, request
from utils.db import get_db_conn


events_bp = Blueprint("events", __name__)


@events_bp.route("/api/events", methods=["GET"])
def getEvents():
    query = "SELECT * from events"
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        result = []
        for row in data:
            event = {
                "date": row[0],
                "title": row[1],
                "event_description": row[2],
                "location": row[3],
                "url": row[4],
            }
            result.append(event)
        return jsonify(result)
    finally:
        conn.close()