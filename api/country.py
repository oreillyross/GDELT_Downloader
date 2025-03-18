from flask import Blueprint, request, jsonify
from utils.db import get_db_conn

country_bp = Blueprint("Country", __name__)

@country_bp.route('/api/country', methods=['GET'])
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