from flask import Blueprint, jsonify
from ..extensions import cache

books_bp = Blueprint("books", __name__)

# Exemple de données "simulées"
BOOKS = [
    {"id": 1, "title": "Flask for Beginners", "author": "Alice"},
    {"id": 2, "title": "Advanced Flask", "author": "Bob"},
    {"id": 3, "title": "Redis in Action", "author": "Charlie"}
]

# Route GET /books avec cache 60 secondes
@books_bp.route("/books", methods=["GET"])
@cache.cached(timeout=60)
def get_books():
    return jsonify(BOOKS)
