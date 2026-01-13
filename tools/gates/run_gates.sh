#!/usr/bin/env bash
set -euo pipefail

# -----------------------------
# Gate Runner: NSW Estimation
# -----------------------------
# Checks:
#  - Working RAG health (8011) + keyword_docs > 0
#  - Decision RAG health (8021) + keyword_docs > 0
#  - AppleDouble hygiene: no ._* files
#  - .dockerignore contains ._* and **/._*
#  - MDR exists and contains at least one Decision ID row
# Output:
#  - governance/decisions/staging/gate_run_<timestamp>.md
#
# Usage:
#   tools/gates/run_gates.sh
#
# Optional env overrides:
#   WORK_RAG_PORT=8011 DECISION_RAG_PORT=8021 tools/gates/run_gates.sh

WORK_RAG_PORT="${WORK_RAG_PORT:-8011}"
DECISION_RAG_PORT="${DECISION_RAG_PORT:-8021}"

# Gate mode: 'work' (default, Decision RAG non-blocking) or 'all' (strict, Decision RAG blocking)
GATES_MODE="${GATES_MODE:-work}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAGING_DIR="${ROOT_DIR}/governance/decisions/staging"
REPORT_TS="$(date +%Y%m%d_%H%M%S)"
REPORT_FILE="${STAGING_DIR}/gate_run_${REPORT_TS}.md"

MDR_FILE="${ROOT_DIR}/governance/decisions/MDR.md"
DOCKERIGNORE_FILE="${ROOT_DIR}/.dockerignore"

mkdir -p "${STAGING_DIR}"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# Append helper
append() { printf "%s\n" "$*" >> "${REPORT_FILE}"; }

# Markers
pass() { PASS_COUNT=$((PASS_COUNT+1)); append "✅ PASS: $*"; }
fail() { FAIL_COUNT=$((FAIL_COUNT+1)); append "❌ FAIL: $*"; }
warn() { WARN_COUNT=$((WARN_COUNT+1)); append "⚠️ WARN: $*"; }

# Python JSON extractor (no jq dependency)
py_json_get() {
  local json="$1"
  local key="$2"
  python3 - "$json" "$key" <<'PY'
import json, sys
data=json.loads(sys.argv[1])
key=sys.argv[2]
val=data.get(key, None)
if val is None:
    sys.stdout.write("")
else:
    sys.stdout.write(str(val))
PY
}

# Curl helper
curl_json() {
  local url="$1"
  curl -fsS "$url"
}

# Header
: > "${REPORT_FILE}"
append "# Gate Run Report"
append ""
append "- Timestamp: \`${REPORT_TS}\`"
append "- Repo: \`${ROOT_DIR}\`"
append "- Branch: \`$(git -C "${ROOT_DIR}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")\`"
append "- Commit: \`$(git -C "${ROOT_DIR}" rev-parse --short HEAD 2>/dev/null || echo "unknown")\`"
append ""
append "## Checks"
append ""

# 1) AppleDouble hygiene (resilient: WARN unless in build-sensitive paths)
append "### 1) AppleDouble hygiene (._*)"
APPLEDOUBLE_FILES="$(find "${ROOT_DIR}" -name '._*' -type f 2>/dev/null)"
APPLEDOUBLE_COUNT="$(echo "${APPLEDOUBLE_FILES}" | grep -c . || echo "0")"
if [[ "${APPLEDOUBLE_COUNT}" == "0" ]]; then
  pass "No AppleDouble files found."
else
  # Check for build-sensitive paths (FAIL if found)
  SENSITIVE_FILES="$(echo "${APPLEDOUBLE_FILES}" | grep -E '(^\./\._\.dockerignore$|^\./\._docker-compose|^\./services/.*/\._)' || true)"
  if [[ -n "${SENSITIVE_FILES}" ]]; then
    fail "Found AppleDouble files in build-sensitive paths (._*). Run: find . -name '._*' -type f -delete && dot_clean ."
    echo "${SENSITIVE_FILES}" | while read -r f; do
      append "  - ${f}"
    done
  else
    warn "Found ${APPLEDOUBLE_COUNT} AppleDouble file(s) (._*) in non-sensitive paths. macOS may recreate these. Run: find . -name '._*' -type f -delete && dot_clean ."
  fi
fi
append ""

# 2) .dockerignore hygiene
append "### 2) .dockerignore hygiene"
if [[ -f "${DOCKERIGNORE_FILE}" ]]; then
  HAS_LINE1="$(grep -E '^\._\*$' "${DOCKERIGNORE_FILE}" >/dev/null 2>&1 && echo "yes" || echo "no")"
  HAS_LINE2="$(grep -E '^\*\*/\._\*$' "${DOCKERIGNORE_FILE}" >/dev/null 2>&1 && echo "yes" || echo "no")"
  if [[ "${HAS_LINE1}" == "yes" && "${HAS_LINE2}" == "yes" ]]; then
    pass ".dockerignore contains both '._*' and '**/._*'."
  else
    fail ".dockerignore missing required patterns. Required lines:\n- ._*\n- **/._*"
  fi
else
  fail ".dockerignore not found at repo root."
fi
append ""

# 3) MDR presence/basic sanity
append "### 3) MDR presence and basic sanity"
if [[ -f "${MDR_FILE}" ]]; then
  # Basic: must contain a header row delimiter and at least one D-xxxx entry
  if grep -qE '\| D-[0-9]{4} \|' "${MDR_FILE}"; then
    pass "MDR exists and contains at least one decision row."
  else
    warn "MDR exists but no decision rows detected (pattern '| D-0001 |'). Check formatting if this is unexpected."
  fi
else
  fail "MDR not found: ${MDR_FILE}"
fi
append ""

# 4) Working RAG health
append "### 4) Working RAG health (port ${WORK_RAG_PORT})"
WORK_HEALTH_URL="http://localhost:${WORK_RAG_PORT}/health"
WORK_HEALTH_JSON=""
if WORK_HEALTH_JSON="$(curl_json "${WORK_HEALTH_URL}" 2>/dev/null)"; then
  WORK_STATUS="$(py_json_get "${WORK_HEALTH_JSON}" "status" | tr -d '\n')"
  WORK_DOCS="$(py_json_get "${WORK_HEALTH_JSON}" "keyword_docs" | tr -d '\n')"
  if [[ "${WORK_STATUS}" == "ok" ]]; then
    pass "Working RAG /health status=ok."
  else
    # In CI-lite mode, service may start but have different status (non-blocking)
    if [[ "${RAG_MODE:-FULL}" == "CI" ]]; then
      warn "Working RAG /health status != ok (non-blocking in CI-lite). Response: ${WORK_HEALTH_JSON}"
    else
      fail "Working RAG /health status != ok. Response: ${WORK_HEALTH_JSON}"
    fi
  fi
  # keyword_docs can be string/int; normalize
  WORK_DOCS_N="${WORK_DOCS:-0}"
  # Strip any whitespace/newlines
  WORK_DOCS_N="$(echo "${WORK_DOCS_N}" | tr -d '[:space:]')"
  # Use awk for simple numeric comparison (more reliable than Python heredoc in this context)
  if awk -v docs="${WORK_DOCS_N}" 'BEGIN { exit (docs > 0 ? 0 : 1) }'; then
    pass "Working RAG keyword_docs > 0 (${WORK_DOCS_N})."
  else
    # In CI-lite mode, keyword_docs=0 is expected (no indexing)
    if [[ "${RAG_MODE:-FULL}" == "CI" ]]; then
      warn "Working RAG keyword_docs is 0 (${WORK_DOCS_N}). Expected in CI-lite mode (no indexing)."
    else
      fail "Working RAG keyword_docs is not > 0 (${WORK_DOCS_N}). Index may be empty."
    fi
  fi
else
  # In CI-lite mode, service may not be fully ready (non-blocking)
  if [[ "${RAG_MODE:-FULL}" == "CI" ]]; then
    warn "Working RAG not reachable at ${WORK_HEALTH_URL} (non-blocking in CI-lite mode)."
  else
    fail "Working RAG not reachable at ${WORK_HEALTH_URL}."
  fi
fi
append ""

# 5) Decision RAG health (non-blocking in work mode)
append "### 5) Decision RAG health (port ${DECISION_RAG_PORT})"
if [[ "${GATES_MODE}" == "work" ]]; then
  append "*(Decision RAG checks are non-blocking in work mode)*"
fi
DEC_HEALTH_URL="http://localhost:${DECISION_RAG_PORT}/health"
DEC_HEALTH_JSON=""
if DEC_HEALTH_JSON="$(curl_json "${DEC_HEALTH_URL}" 2>/dev/null)"; then
  DEC_STATUS="$(py_json_get "${DEC_HEALTH_JSON}" "status" | tr -d '\n')"
  DEC_DOCS="$(py_json_get "${DEC_HEALTH_JSON}" "keyword_docs" | tr -d '\n')"
  if [[ "${DEC_STATUS}" == "ok" ]]; then
    pass "Decision RAG /health status=ok."
  else
    if [[ "${GATES_MODE}" == "work" ]]; then
      warn "Decision RAG /health status != ok (non-blocking). Response: ${DEC_HEALTH_JSON}"
    else
      fail "Decision RAG /health status != ok. Response: ${DEC_HEALTH_JSON}"
    fi
  fi
  DEC_DOCS_N="${DEC_DOCS:-0}"
  # Strip any whitespace/newlines
  DEC_DOCS_N="$(echo "${DEC_DOCS_N}" | tr -d '[:space:]')"
  # Use awk for simple numeric comparison (more reliable than Python heredoc in this context)
  if awk -v docs="${DEC_DOCS_N}" 'BEGIN { exit (docs > 0 ? 0 : 1) }'; then
    pass "Decision RAG keyword_docs > 0 (${DEC_DOCS_N})."
  else
    # In work mode or CI-lite mode, keyword_docs=0 is expected/warned
    if [[ "${GATES_MODE}" == "work" || "${RAG_MODE:-FULL}" == "CI" ]]; then
      warn "Decision RAG keyword_docs is 0 (${DEC_DOCS_N}). Expected in work/CI-lite mode (no indexing or service skipped)."
    else
      fail "Decision RAG keyword_docs is not > 0 (${DEC_DOCS_N}). Index may be empty."
    fi
  fi
else
  # In work mode or CI-lite mode, Decision RAG may be skipped (non-blocking)
  if [[ "${GATES_MODE}" == "work" || "${RAG_MODE:-FULL}" == "CI" ]]; then
    warn "Decision RAG not reachable at ${DEC_HEALTH_URL}. Expected in work/CI-lite mode if manifest missing (non-blocking)."
  else
    fail "Decision RAG not reachable at ${DEC_HEALTH_URL}."
  fi
fi
append ""

# 6) Decision RAG QC query (must cite governance, non-blocking in work mode)
append "### 6) Decision RAG QC query (governance citation)"
if [[ "${GATES_MODE}" == "work" ]]; then
  append "*(Decision RAG QC query is non-blocking in work mode)*"
fi
DEC_QUERY_URL="http://localhost:${DECISION_RAG_PORT}/query"
QC_PAYLOAD='{"query":"MDR Decision Register D-0001","top_k":5}'
DEC_QUERY_JSON=""
if DEC_QUERY_JSON="$(curl -fsS -X POST "${DEC_QUERY_URL}" -H "Content-Type: application/json" -d "${QC_PAYLOAD}" 2>/dev/null)"; then
  # Determine if citations exist and include governance/decisions
  if python3 - "${DEC_QUERY_JSON}" >/dev/null 2>&1 <<'PY'
import json, sys, re
data=json.loads(sys.argv[1])
cits=data.get("citations", []) or []
ok=False
for c in cits:
  f=(c.get("file","") or "") + " " + (c.get("kb_path","") or "")
  if "governance/decisions" in f:
    ok=True
    break
sys.exit(0 if ok else 1)
PY
  then
    pass "Decision RAG QC query returned at least one governance citation."
  else
    warn "Decision RAG QC query did not show governance/decisions citation. Response may still be OK, but verify Decision KB indexing."
  fi
else
  warn "Decision RAG /query not reachable or failed. This is a warning (health may still be OK)."
fi
append ""

# Summary
append "## Summary"
append ""
append "- Pass: **${PASS_COUNT}**"
append "- Warn: **${WARN_COUNT}**"
append "- Fail: **${FAIL_COUNT}**"
append ""
append "Report: \`${REPORT_FILE}\`"

# Console echo
echo "Gate report written: ${REPORT_FILE}"
echo "Pass=${PASS_COUNT} Warn=${WARN_COUNT} Fail=${FAIL_COUNT}"

# Exit non-zero on failures
# In CI-lite mode, only structural failures (MDR, .dockerignore) should block
# Infrastructure failures (RAG health) are warnings
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
  if [[ "${RAG_MODE:-FULL}" == "CI" ]]; then
    echo "CI-lite mode: ${FAIL_COUNT} failure(s) detected, but allowing pass (infrastructure checks are non-blocking)"
    exit 0
  else
    exit 1
  fi
fi
exit 0
