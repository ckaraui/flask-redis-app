from flask import Flask
from .extensions import db, jwt, cache
from .routes.auth import auth_bp
from .routes.books import books_bp  # <-- importer le blueprint books

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret-jwt-key'
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://redis:6379/0'

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(books_bp)  # <-- enregistrer blueprint books

    return app
