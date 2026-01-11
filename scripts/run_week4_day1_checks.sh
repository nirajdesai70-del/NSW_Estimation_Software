#!/usr/bin/env bash
set -euo pipefail

echo "======================================"
echo " Phase-6 | Week-4 Day-1 Checks"
echo "======================================"

# ---- ENV defaults ----
export NSW_API_BASE="${NSW_API_BASE:-http://localhost:8003/api/v1}"
export NSW_TENANT_ID="${NSW_TENANT_ID:-1}"
export NSW_USER_ID="${NSW_USER_ID:-1}"

export NSW_COST_QID="${NSW_COST_QID:-4}"
export NSW_COST_PANEL_ID="${NSW_COST_PANEL_ID:-8}"
export NSW_FROZEN_QID="${NSW_FROZEN_QID:-0}"   # set to enable freeze test

export DB_HOST="${DB_HOST:-localhost}"
export DB_PORT="${DB_PORT:-5433}"
export DB_USER="${DB_USER:-nsw_user}"
export DB_PASSWORD="${DB_PASSWORD:-nsw_dev_password}"
export DB_NAME="${DB_NAME:-nsw_estimation}"

echo "Checking backend health…"
if ! curl -sf "http://localhost:8003/health" >/dev/null 2>&1; then
  echo "❌ Backend not reachable at http://localhost:8003"
  exit 1
fi
echo "✅ Backend reachable"

echo
echo "Running canon drift check…"
./scripts/check_schema_drift.sh

echo
echo "Running Week-3 regression tests…"
python3 -m pytest -q \
  tests/costing/test_cost_adders_upsert.py \
  tests/costing/test_cost_summary_api.py \
  tests/catalog/test_catalog_pilot_binding.py

echo
echo "Running Week-4 Day-1 tests…"
python3 -m pytest -q \
  tests/quotation/test_quotation_state_visibility.py \
  tests/quotation/test_freeze_immutability_cost_adders.py

echo
echo "======================================"
echo " ✅ Week-4 Day-1 Checks PASSED"
echo "======================================"
