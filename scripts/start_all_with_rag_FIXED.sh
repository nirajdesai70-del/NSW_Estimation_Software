#!/bin/bash
set -e

echo "=== START ALL + RAG ==="

############################################
# Helpers
############################################

wait_http_ok () {
  local url="$1"
  local label="$2"
  local tries="${3:-20}"
  local delay="${4:-1}"

  for i in $(seq 1 "$tries"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "✅ $label OK"
      return 0
    fi
    sleep "$delay"
  done

  echo "⚠️ $label not ready after $tries seconds: $url"
  return 1
}

############################################
# Safety & Environment
############################################

# SSD must be mounted
if [ ! -d "/Volumes/T9" ]; then
  osascript -e 'display dialog "T9 SSD is not mounted.\n\nPlease connect T9 before starting." buttons {"OK"} with icon stop'
  exit 1
fi

# Canonical NSW root
NSW_ROOT="/Volumes/T9/Projects/NSW_Estimation_Software"
BACKEND_DIR="$NSW_ROOT/backend"

# Prevent Docker socket confusion
unset DOCKER_HOST

# Ensure docker context
docker context use mac-desktop >/dev/null 2>&1 || true

############################################
# Stop everything cleanly
############################################

echo "🧹 Running Stop All first..."
/Users/nirajdesai/bin/stop_all.sh || true

############################################
# Start RAG (Docker) - FIXED: Added --remove-orphans
############################################

echo "🚀 Starting RAG Query (8011)..."
cd "$NSW_ROOT"
docker compose -f docker-compose.rag.yml --profile rag up -d --remove-orphans

############################################
# XAMPP MySQL check
############################################

XAMPP_SOCK="/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"
if [ ! -S "$XAMPP_SOCK" ]; then
  echo "❌ XAMPP MySQL socket not found"
  exit 1
fi
echo "✅ XAMPP MySQL OK (socket detected)"

############################################
# Start Nish (8000)
############################################

echo "🚀 Starting Nish (8000)..."
cd /Volumes/T9/Projects/nish
php -d error_reporting="E_ALL & ~E_DEPRECATED & ~E_USER_DEPRECATED" artisan serve \
  --host=127.0.0.1 --port=8000 >/tmp/nish_8000.log 2>&1 &

sleep 2

############################################
# Start NSW API (8003)
############################################

echo "🚀 Starting NSW (8003)..."

# Check PostgreSQL first (REQUIRED for Phase-6)
echo "   🐘 Checking PostgreSQL (5433)..."
if ! lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "   Starting PostgreSQL..."
  cd "$NSW_ROOT"
  # FIXED: Added --remove-orphans to clean up orphan containers
  docker compose --profile db up -d --remove-orphans postgres
  echo "   ⏳ Waiting for PostgreSQL to be ready..."
  sleep 5
  if ! lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1; then
    echo "   ❌ PostgreSQL failed to start"
    exit 1
  fi
fi
echo "   ✅ PostgreSQL is running"

cd "$BACKEND_DIR"

if [ ! -f ".venv/bin/activate" ]; then
  echo "❌ Project venv missing: $BACKEND_DIR/.venv"
  exit 1
fi

source ".venv/bin/activate"

# Set DATABASE_URL (CRITICAL - prevents SQLite default error)
export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg://nsw_user:nsw_dev_password@localhost:5433/nsw_estimation}"

# Test import before starting (catches config errors early)
echo "   Testing application import..."
if ! python -c "from app.main import app" >/dev/null 2>&1; then
  echo "   ❌ Application import failed. Check errors:"
  python -c "from app.main import app" 2>&1 | head -15
  exit 1
fi
echo "   ✅ Application imports successfully"

# Kill any existing process on port 8003
lsof -ti:8003 | xargs kill -9 2>/dev/null || true
sleep 1

# Start uvicorn
python -m uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8003 \
  --reload \
  >/tmp/nsw_8003.log 2>&1 &

############################################
# Health checks (THIS IS NEW)
############################################

echo ""
echo "=== HEALTH CHECKS ==="
wait_http_ok "http://127.0.0.1:8011/health" "RAG" 25 1 || true
wait_http_ok "http://127.0.0.1:8003/health" "NSW" 30 1 || true

echo ""
echo "=== STATUS ==="
lsof -nP -iTCP -sTCP:LISTEN | egrep ":(8000|8003|8011)" || true

osascript -e 'display notification "Nish(8000) + NSW(8003) + RAG(8011) started"'
