from flask import Blueprint, jsonify
from app.extensions import cache

cache_bp = Blueprint("cache", __name__)

@cache_bp.route("/cache/expensive", methods=["GET"])
@cache.cached(timeout=30)
def expensive():
    import time
    time.sleep(2)  # simulate long computation
    return jsonify({"value": "Expensive result"})

@cache_bp.route("/cache/clear", methods=["GET"])
def clear_cache():
    cache.clear()
    return jsonify({"message": "Cache cleared"})
