import os

import psycopg2
from flask import Flask, jsonify

conn = psycopg2.connect(os.environ['DATABASE_URL'])

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
  cur = conn.cursor()
  cur.execute('SELECT * FROM your_table')
  data = cur.fetchall()
  cur.close()
  conn.close()
  return jsonify(data)
  
  


