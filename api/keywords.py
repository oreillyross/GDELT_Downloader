from flask import Blueprint, jsonify, request

from db.pg2_db import conn

keywords_bp = Blueprint("keywords", __name__)


@keywords_bp.route("/keywords", methods=["POST"])
def create_keyword():
  new_keyword = request.json.get("keyword", "") if request.json else ""
  with conn.cursor() as cur:
    cur.execute("INSERT INTO keywords (keyword) VALUES (%s) RETURNING id",
                (new_keyword, ))
    result = cur.fetchone()
    new_id = result[0] if result else None
    conn.commit()
  return jsonify({"id": new_id, "keyword": new_keyword}), 201


@keywords_bp.route("/keywords", methods=["GET"])
def get_keywords():
  with conn.cursor() as cur:
    cur.execute("SELECT * from keywords")
    keywords = cur.fetchall()
    return jsonify(keywords)


@keywords_bp.route("/keywords/<int:id>", methods=["PUT"])
def update_keyword(id):
  updated_keyword = request.json.get("keyword", "") if request.json else ""
  with conn.cursor() as cur:
    cur.execute("UPDATE keywords SET keyword = %s WHERE id = %s",
                (updated_keyword, id))
    conn.commit()
  return jsonify({"message": "Keyword updated successfully"}), 201


@keywords_bp.route("/keywords/<int:id>", methods=["DELETE"])
def delete_keyword(id):
  with conn.cursor() as cur:
    cur.execute("DELETE keywords WHERE id = %s", (id))
    conn.commit()
  return jsonify({"message": "Keyword successfully deleted"}), 201
