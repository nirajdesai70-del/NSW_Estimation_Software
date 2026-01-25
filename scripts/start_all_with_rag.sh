#!/bin/bash

# Start All Services with RAG
# Starts core Docker services + RAG + non-Docker backend/frontend
# Optional: --clean to stop/remove existing containers first

set -e  # Exit on error

USE_CLEAN=0
if [ "${1:-}" = "--clean" ]; then
  USE_CLEAN=1
fi

# Get the project root directory (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Prevent Docker socket confusion
unset DOCKER_HOST

# Prefer Docker Desktop context if available
docker context use mac-desktop >/dev/null 2>&1 || true

wait_http_ok () {
  local url="$1"
  local label="$2"
  local tries="${3:-30}"
  local delay="${4:-1}"

  for i in $(seq 1 "$tries"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "✅ $label OK"
      return 0
    fi
    sleep "$delay"
  done

  echo "⚠️  $label not ready after $tries seconds: $url"
  return 1
}

if [ "$USE_CLEAN" -eq 1 ]; then
  echo "Cleaning existing containers..."
  docker compose -f docker-compose.rag.decisions.yml --profile decisions_rag down --remove-orphans || true
  docker compose -f docker-compose.rag.yml --profile rag down --remove-orphans || true
  docker compose --profile db --profile cache down --remove-orphans || true
fi

echo "Starting core Docker services..."
docker compose --profile db --profile cache up -d postgres redis

echo "Starting RAG services..."
docker compose -f docker-compose.rag.yml --profile rag up -d kb_query
docker compose -f docker-compose.rag.decisions.yml --profile decisions_rag up -d decisions_query

echo "Starting backend (FastAPI)..."
if [ -d "$PROJECT_ROOT/backend" ]; then
  cd "$PROJECT_ROOT/backend"

  if [ -d ".venv" ]; then
    source ".venv/bin/activate"
  elif [ -d "venv" ]; then
    source "venv/bin/activate"
  fi

  lsof -ti:8001 | xargs kill -9 2>/dev/null || true
  python3 -m uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8001 \
    --reload \
    >/tmp/nsw_backend_8001.log 2>&1 &
fi

echo "Starting frontend (Vite)..."
if [ -d "$PROJECT_ROOT/frontend" ]; then
  cd "$PROJECT_ROOT/frontend"
  if [ ! -d "node_modules" ]; then
    npm install
  fi
  lsof -ti:3000 | xargs kill -9 2>/dev/null || true
  npm run dev >/tmp/nsw_frontend_3000.log 2>&1 &
fi

cd "$PROJECT_ROOT"

echo ""
echo "=== HEALTH CHECKS ==="
wait_http_ok "http://localhost:8011/health" "RAG (main)" 40 1 || true
wait_http_ok "http://localhost:8021/health" "RAG (decisions)" 40 1 || true
wait_http_ok "http://localhost:8001/health" "Backend" 40 1 || true

echo ""
echo "Services running:"
docker compose --profile db --profile cache ps
docker compose -f docker-compose.rag.yml --profile rag ps
docker compose -f docker-compose.rag.decisions.yml --profile decisions_rag ps

echo ""
echo "Endpoints:"
echo "  RAG main:      http://localhost:8011/health"
echo "  RAG decisions: http://localhost:8021/health"
echo "  Backend:       http://localhost:8001/health"
echo "  Frontend:      http://localhost:3000"
