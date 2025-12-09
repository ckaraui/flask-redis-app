from flask import Flask
from .extensions import db, jwt, cache
from .routes.auth import auth_bp
from .routes.books import books_bp
from .routes.cache_demo import cache_bp
from .config import DevelopmentConfig

def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(books_bp, url_prefix="/api")
    app.register_blueprint(cache_bp, url_prefix="/cache")

    return app
