from flask import Blueprint, jsonify
from app.extensions import cache
import time

cache_bp = Blueprint("cache", __name__, url_prefix="/cache")

@cache_bp.route("/expensive", methods=["GET"])
@cache.cached(timeout=30)
def expensive():
    time.sleep(2)
    return jsonify({"value": "Expensive result"})

@cache_bp.route("/clear", methods=["POST"])
def clear_cache():
    cache.clear()
    return jsonify({"msg": "Cache cleared"})
