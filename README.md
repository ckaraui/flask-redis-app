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

Quick start — Local (venv + Redis)
**Prerequisite: Start Redis locally** (Docker recommended)
```bash
docker run -d --name local-redis -p 6379:6379 redis:7
# verify: docker exec -it local-redis redis-cli ping
# should return: PONG
```

**Then run the app using `dev.sh`** (automates venv, deps, db init, env vars)
```bash
chmod +x dev.sh
./dev.sh
# This will:
# - Create/activate venv if needed
# - Install dependencies
# - Initialize database
# - Export all required env vars
# - Start Flask on http://0.0.0.0:5000
```

**Or manually** (if you prefer):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=run.py
export FLASK_ENV=development
export JWT_SECRET_KEY=dev-secret-change-me-in-prod
export DATABASE_URL=sqlite:///data.db
export REDIS_HOST=localhost
export REDIS_PORT=6379

python init_db.py
flask run --host=0.0.0.0 --port=5000
```

Environment variables
- `FLASK_APP` — entry point (default for this project: `run.py`)
- `FLASK_ENV` — `development` or `production` (dev enables auto-reload & debug)
- `DATABASE_URL` — SQLAlchemy DB URL (default: `sqlite:///data.db`)
- `JWT_SECRET_KEY` — secret for signing JWTs (never commit real secrets; use dev placeholder locally)
- `REDIS_HOST` — Redis hostname (local dev: `localhost`; Docker Compose: `redis`)
- `REDIS_PORT` — Redis port (default: `6379`)
- `CACHE_TYPE` — cache backend (default: `RedisCache`; use `SimpleCache` for dev without Redis)

**Note:** When running locally, `REDIS_HOST=localhost` points to your machine. When using Docker Compose, `REDIS_HOST=redis` resolves to the `redis` service inside the compose network. The `dev.sh` script uses `localhost` by default.

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
- **Redis connection error ("Name or service not known")**: 
  - Local dev: ensure Redis is running (`docker run -d --name local-redis -p 6379:6379 redis:7`) and `REDIS_HOST=localhost` is set.
  - Docker Compose: ensure the `redis` service is defined in `docker-compose.yml` and `REDIS_HOST=redis`.
  - Test Redis: `docker exec -it local-redis redis-cli ping` (should return `PONG`).
- **400 Bad Request HTML**: check request body and `Content-Type` header (some REST clients include extra text).
- **venv issues**: make sure the virtual environment is activated (`source .venv/bin/activate`).
- **Port conflicts**: ensure port 5000 (Flask) and 6379 (Redis) are available.

Key files
- `app/__init__.py` — app factory and blueprint registration
- `app/config.py` — configuration and env var usage
- `app/extensions.py` — shared extensions (`db`, `cache`, `jwt`, `migrate`)
- `app/routes/` — blueprints (`auth.py`, `books.py`, `cache.py`)
- `init_db.py` — quick DB bootstrap used by Dockerfile entrypoint
- `run.py` — exposes `app = create_app()` for Gunicorn
