import os

from flask_cors import CORS
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

CORS(app)


def get_db_conn():
  return psycopg2.connect(os.environ['DATABASE_URL'])

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
  app.run(debug=True)
