# Flask Redis App

Minimal Flask application demonstrating Redis-backed caching and simple JWT auth.

Overview
- Factory app in `app/__init__.py` that registers blueprints from `app/routes/`.
- Shared extensions in `app/extensions.py`: `db`, `migrate`, `cache`, `jwt`.

Quick start — Docker Compose (recommended)
1. Build and start services (includes Redis):
```bash
docker-compose up -d --build
```
2. Watch logs:
```bash
docker-compose logs -f --tail=200 flask_app redis
```
3. Stop and remove:
```bash
docker-compose down
```

Quick start — Local (venv)
1. Create venv and install deps:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Set environment variables (examples):
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export JWT_SECRET_KEY=your_jwt_secret
export DATABASE_URL=sqlite:///data.db
# Redis connection used by Flask-Caching (container name when using compose):
export CACHE_REDIS_HOST=redis
export CACHE_REDIS_PORT=6379
```
3. Initialize DB (dev):
```bash
python init_db.py
```
4. Run the app (dev):
```bash
flask run --host=0.0.0.0 --port=5000
# or: python run.py
```

Environment variables (used by the app)
- `DATABASE_URL` — SQLAlchemy DB URL (default `sqlite:///data.db`)
- `JWT_SECRET_KEY` — secret for JWTs (default in code: `jwt-secret`)
- `CACHE_TYPE` — default `RedisCache` (configured in `app/config.py`)
- `CACHE_REDIS_HOST` / `CACHE_REDIS_PORT` — Redis host/port (defaults in code)
- `CACHE_DEFAULT_TIMEOUT` — cache TTL default (seconds)

Notes on DB & migrations
- `init_db.py` calls `db.create_all()` and is used by the Docker image entrypoint.
- `Flask-Migrate` is available (`migrate` in `app/extensions.py`) — for production use prefer `flask db migrate` / `flask db upgrade`.

Routes overview
- `POST /auth/register` — register user (body: `username`, `password`)
- `POST /auth/login` — login, returns `access_token` JSON
- `GET /auth/me` — requires `Authorization: Bearer <token>`
- `GET /books` / `POST /books` — simple book CRUD (cached `GET /books`)
- `GET /cache/expensive` — example cached endpoint
- `POST /cache/clear` — clear cache

Examples (curl)
- Register:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}'
```
- Login and extract token:
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}' | jq -r '.access_token')
echo $TOKEN
```
- Use token:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/auth/me
```

Troubleshooting
- Redis connection errors: ensure `redis` service is running (when using compose) and that `CACHE_REDIS_HOST` matches the container name `redis`.
- If you get a 400 HTML from Gunicorn before the Flask handler runs, check the request body and `Content-Type` header (REST clients sometimes include extra text).

Key files
- `app/__init__.py` — app factory and blueprint registration
- `app/config.py` — configuration and env var usage
- `app/extensions.py` — shared extensions (`db`, `cache`, `jwt`, `migrate`)
- `app/routes/` — blueprints (`auth.py`, `books.py`, `cache.py`)
- `init_db.py` — quick DB bootstrap used by Dockerfile entrypoint
- `run.py` — exposes `app = create_app()` for Gunicorn
