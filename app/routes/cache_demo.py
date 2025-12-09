from flask import Blueprint
from ..extensions import cache
import time

cache_bp = Blueprint("cache", __name__)

@cache_bp.route("/expensive")
@cache.cached(timeout=30)
def expensive():
    time.sleep(3)  # simulate long process
    return "Résultat coûteux avec cache"
