#!/usr/bin/env bash
set -euo pipefail

echo "======================================"
echo " Phase-6 | Week-4 Consolidated Checks"
echo "======================================"

# Keep same ENV defaults used across all runners
export NSW_API_BASE="${NSW_API_BASE:-http://localhost:8003/api/v1}"
export NSW_TENANT_ID="${NSW_TENANT_ID:-1}"
export NSW_USER_ID="${NSW_USER_ID:-1}"

export NSW_COST_QID="${NSW_COST_QID:-4}"
export NSW_COST_PANEL_ID="${NSW_COST_PANEL_ID:-8}"
export NSW_FROZEN_QID="${NSW_FROZEN_QID:-0}"
export NSW_PILOT_SKU="${NSW_PILOT_SKU:-LC1D09M7}"

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
echo "Running schema canon drift check…"
./scripts/check_schema_drift.sh

echo
echo "Running Week-3 Day-4 checks…"
./scripts/run_week3_checks.sh

echo
echo "Running Week-4 Day-1 checks…"
./scripts/run_week4_day1_checks.sh

echo
echo "Running Week-4 Day-2 checks…"
./scripts/run_week4_day2_checks.sh

echo
echo "Running Week-4 Day-3 checks…"
./scripts/run_week4_day3_checks.sh

echo
echo "Running Week-4 Day-4 API surface guard…"
python3 -m pytest -q tests/summary/test_cost_summary_top_level_whitelist.py

echo
echo "======================================"
echo " ✅ Phase-6 | Week-4 Consolidated Checks PASSED"
echo "======================================"
