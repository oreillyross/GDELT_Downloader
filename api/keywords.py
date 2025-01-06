from flask import Blueprint, jsonify, request

from db.pg2_db import get_conn, put_conn

keywords_bp = Blueprint("keywords", __name__)


@keywords_bp.route("/api/keywords", methods=["POST"])
def create_keyword():
  new_keyword = request.json.get("keyword", "") if request.json else ""
  conn = get_conn()
  try:
    with conn.cursor() as cur:
      cur.execute("INSERT INTO keywords (keyword) VALUES (%s) RETURNING id",
                  (new_keyword, ))
      result = cur.fetchone()
      new_id = result[0] if result else None
      conn.commit()
    return jsonify({"id": new_id, "keyword": new_keyword}), 201
  finally:
    put_conn(conn)

@keywords_bp.route("/api/keywords", methods=["GET"])
def get_keywords():
  conn = get_conn()
  try:
    with conn.cursor() as cur:
      cur.execute("SELECT * from keywords")
      keywords = cur.fetchall()
      return jsonify(keywords)
  finally:
    put_conn(conn)

@keywords_bp.route("/api/keywords/<int:id>", methods=["PUT"])
def update_keyword(id):
  updated_keyword = request.json.get("keyword", "") if request.json else ""
  conn = get_conn()
  try:
    with conn.cursor() as cur:
      cur.execute("UPDATE keywords SET keyword = %s WHERE id = %s",
                  (updated_keyword, id))
      conn.commit()
    return jsonify({"message": "Keyword updated successfully"}), 201
  finally:
    put_conn(conn)

@keywords_bp.route("/api/keywords/<int:id>", methods=["DELETE"])
def delete_keyword(id):
  conn = get_conn()
  try:
    with conn.cursor() as cur:
      cur.execute("DELETE FROM keywords WHERE id = %s", (id,))
      conn.commit()
    return jsonify({"message": "Keyword successfully deleted"}), 201
  finally:
    put_conn(conn)
