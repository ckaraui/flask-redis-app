from flask import Blueprint, request, jsonify
from ..models import Book
from ..extensions import db

books_bp = Blueprint("books", __name__)

@books_bp.route("/books", methods=["POST"])
def add_book():
    data = request.json
    book = Book(title=data["title"], author=data["author"])
    db.session.add(book)
    db.session.commit()
    return jsonify(msg="Book added")

@books_bp.route("/books", methods=["GET"])
def get_books():
    all_books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author} for b in all_books])
