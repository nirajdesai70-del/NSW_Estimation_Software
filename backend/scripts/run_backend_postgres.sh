#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/Volumes/T9/Projects/NSW_Estimation_Software"
BACKEND_DIR="$REPO_ROOT/backend"

# Always use Postgres for this run
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/nsw_dev"

# Always provide a default port (this is the fix for your error)
export NSW_BACKEND_PORT="${NSW_BACKEND_PORT:-8003}"

# Activate venv
source "$BACKEND_DIR/.venv/bin/activate"

cd "$BACKEND_DIR"

echo ">>> DATABASE_URL=$DATABASE_URL"
echo ">>> NSW_BACKEND_PORT=$NSW_BACKEND_PORT"

# IMPORTANT: use python module call (avoids PATH issues)
python -m uvicorn app.main:app --reload --port "$NSW_BACKEND_PORT"
