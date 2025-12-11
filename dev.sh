#!/bin/bash
# Development startup script — exports env vars and launches Flask app

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[dev.sh] Setting up development environment...${NC}"

# Export environment variables for local development
export FLASK_APP=run.py
export FLASK_ENV=development
export JWT_SECRET_KEY=dev-secret-change-me-in-prod
export DATABASE_URL=sqlite:///data.db
export REDIS_HOST=localhost
export REDIS_PORT=6379

echo -e "${GREEN}✓ Env vars exported:${NC}"
echo "  FLASK_APP=$FLASK_APP"
echo "  FLASK_ENV=$FLASK_ENV"
echo "  JWT_SECRET_KEY=$JWT_SECRET_KEY"
echo "  DATABASE_URL=$DATABASE_URL"
echo "  REDIS_HOST=$REDIS_HOST"
echo "  REDIS_PORT=$REDIS_PORT"
echo ""

# Check if venv exists, create if missing
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[dev.sh] Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ venv created${NC}"
fi

# Activate venv
source .venv/bin/activate
echo -e "${GREEN}✓ venv activated${NC}"
echo ""

# Install/upgrade requirements
echo -e "${YELLOW}[dev.sh] Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Initialize database
echo -e "${YELLOW}[dev.sh] Initializing database...${NC}"
python init_db.py
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# Warn about Redis
echo -e "${YELLOW}[dev.sh] Redis dependency:${NC}"
echo "  Make sure Redis is running on localhost:6379"
echo "  Quick start (Docker): docker run -d --name local-redis -p 6379:6379 redis:7"
echo ""

# Start Flask development server
echo -e "${GREEN}[dev.sh] Starting Flask dev server on http://0.0.0.0:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""
flask run --host=0.0.0.0 --port=5000
