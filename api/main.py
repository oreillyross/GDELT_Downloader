import os

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db_conn():
  return psycopg2.connect(os.environ['DATABASE_URL'])


@app.route('/api/data', methods=['GET'])
def get_data():
  param_value = request.args.get("country")
  conn = get_db_conn()
  try:
    cur = conn.cursor()
    query = "SELECT * FROM cameo_countries WHERE label like %s"
    country_query = f"%{param_value}%"
    cur.execute(query, (country_query, ))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)
  finally:
    conn.close()


if __name__ == '__main__':
  app.run(debug=True)
