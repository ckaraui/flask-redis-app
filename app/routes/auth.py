from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.before_request
def debug_request():
    if request.path == "/auth/login" and request.method == "POST":
        try:
            raw = request.get_data(as_text=True)
            print(f"[DEBUG LOGIN] method={request.method}, content_type={request.content_type}, content_length={request.content_length}, raw_body={raw!r}")
        except Exception as e:
            print(f"[DEBUG LOGIN] Error reading request: {e}")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    # Support JSON, form-encoded, and fallback to query params.
    data = {}
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        # common case: application/x-www-form-urlencoded or multipart/form-data
        data = request.form.to_dict() or {}
        # final fallback: query params (or empty dict)
        if not data:
            data = request.args.to_dict() or {}

    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        # Debugging: show content type and raw body when credentials missing
        try:
            raw = request.get_data(as_text=True)
        except Exception:
            raw = "<could not read raw body>"
        print(f"[auth.login] missing credentials; content_type={request.content_type!r}, raw_body={raw!r}")
        return jsonify({"msg": "username and password required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "Not found"}), 404
    return jsonify({"id": user.id, "username": user.username}), 200
