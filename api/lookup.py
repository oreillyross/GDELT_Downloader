from flask import Blueprint
from utils.db import get_db_conn

lookup_bp = Blueprint("Lookup", __name__)

@lookup_bp.route("/api/goldstein_scales", methods=['GET'])
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


@lookup_bp.route('/api/event_codes', methods=['GET'])
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