# Flask Redis App

A small Flask application that uses Redis as a backing store/cache. This repository demonstrates how to connect a Flask app to Redis, store and retrieve data, and run the service locally or with Docker.

## Features
- Simple Flask app with Redis integration
- Example cache/set/get endpoints
- Docker and Docker Compose support
- Basic test instructions

## Tech stack
- Python 3.8+
- Flask
- redis-py
- Redis (server)

## Prerequisites
- Python 3.8 or newer
- pip
- Redis server (local or remote) or Docker
- (Optional) virtualenv or venv

## Environment variables
Set the following environment variables before running the app. You can also use a `.env` file and a loader like python-dotenv if desired.

- REDIS_URL — full Redis URL (e.g. `redis://localhost:6379/0`) OR
- REDIS_HOST — Redis host (default: `localhost`)
- REDIS_PORT — Redis port (default: `6379`)
- REDIS_DB — Redis DB number (default: `0`)
- FLASK_APP — Flask application entry (e.g. `app.py` or package name)
- FLASK_ENV — `development` or `production`

If both REDIS_URL and individual host/port/db variables are present, prefer REDIS_URL.

## Installation (local)
1. Clone the repository:
   ```bash
   git clone https://github.com/ckaraui/flask-redis-app.git
   cd flask-redis-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables (example):
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export REDIS_URL=redis://localhost:6379/0
   ```

5. Run the app:
   ```bash
   flask run
   ```
   or:
   ```bash
   python app.py
   ```

## Docker / Docker Compose
A quick way to run Redis and the Flask app together is with Docker Compose. Example `docker-compose.yml`:

```yaml
version: "3.8"
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"

  web:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379/0
      - FLASK_APP=app.py
      - FLASK_ENV=development
    ports:
      - "5000:5000"
    depends_on:
      - redis
```

Start the services:
```bash
docker-compose up --build
```

## Example API usage
Below are example curl commands demonstrating typical Redis-backed endpoints. Update paths to match your app's endpoints if they differ.

- Set a value (POST JSON):
  ```bash
  curl -X POST http://localhost:5000/cache \
    -H "Content-Type: application/json" \
    -d '{"key":"mykey","value":"hello world","ttl":3600}'
  ```

- Get a value:
  ```bash
  curl http://localhost:5000/cache/mykey
  ```

- Delete a value:
  ```bash
  curl -X DELETE http://localhost:5000/cache/mykey
  ```

If your app uses different endpoints or request shapes, replace the examples above with the appropriate routes/fields.

## Running tests
If the project includes tests (pytest recommended), run:
```bash
pytest
```
If no tests exist yet, consider adding tests for the Redis integration (use a test Redis instance or fakeredis for unit tests).

## Troubleshooting
- Connection errors: verify REDIS_URL or host/port and that Redis is running.
- Permission or port conflicts: ensure nothing else is using the port (default 5000 for Flask, 6379 for Redis).
- Virtualenv issues: ensure you activated the environment and installed requirements into it.

## Contributing
Contributions are welcome. Suggested workflow:
1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Make changes and tests
4. Open a pull request describing your changes

Please follow any existing code style and add tests for new functionality.

## License
Specify your license here (e.g., MIT). If you don't have one yet, consider adding an appropriate LICENSE file.

## Next steps I can help with
- Customize this README to match the exact endpoints and usage in your code.
- Add a LICENgSE file or a CONTRIBUTING file.
- Open a branch and push the README directly to the repository.