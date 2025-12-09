from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db
from passlib.hash import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    hashed = bcrypt.hash(password)
    user = User(username=username, password=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"id": user.id, "username": user.username}), 200
