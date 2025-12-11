from flask import Blueprint, request, jsonify
from app.extensions import cache
from app.models import Book
from app.extensions import db

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def list_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author} for b in books])

@books_bp.route("/", methods=["POST"])
def create_book():
    data = request.get_json() or {}
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify({"msg": "title and author required"}), 400
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return jsonify({"msg": "Book added"}), 201
