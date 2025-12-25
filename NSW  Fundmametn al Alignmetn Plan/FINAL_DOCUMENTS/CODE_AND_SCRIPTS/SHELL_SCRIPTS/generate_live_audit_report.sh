#!/usr/bin/env bash
set -euo pipefail

LIVE_REPO="${1:-/Users/nirajdesai/Projects/nish}"
OUT_DIR="${2:-./_live_audit_reports}"

mkdir -p "$OUT_DIR"
TS="$(date '+%Y%m%d_%H%M%S')"
REPORT="$OUT_DIR/live_audit_$TS.txt"

{
  echo "=== LIVE AUDIT REPORT ==="
  echo "Timestamp: $(date)"
  echo "Repo: $LIVE_REPO"
  echo

  if [ ! -d "$LIVE_REPO" ]; then
    echo "ERROR: Repo path not found: $LIVE_REPO"
    exit 1
  fi

  cd "$LIVE_REPO"

  echo "## 1) Git branch + status"
  echo "Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'N/A')"
  echo "HEAD:   $(git rev-parse --short HEAD 2>/dev/null || echo 'N/A')"
  echo
  git status --porcelain=v1 || true
  echo

  echo "## 2) Git diff (working tree)"
  git diff --stat || true
  echo
  git diff || true
  echo

  echo "## 3) Untracked files"
  git ls-files --others --exclude-standard || true
  echo

  echo "## 4) Recent file modifications (last 3 days) — best effort"
  # macOS compatible: prefer BSD stat
  if stat -f "%m %N" . >/dev/null 2>&1; then
    find . -type f -mtime -3 -maxdepth 6 2>/dev/null | while read -r f; do
      stat -f "%Sm  %N" -t "%Y-%m-%d %H:%M:%S" "$f" 2>/dev/null || true
    done | sort || true
  else
    # fallback Linux-like
    find . -type f -mtime -3 -maxdepth 6 -print0 2>/dev/null | xargs -0 ls -lt 2>/dev/null || true
  fi

  echo
  echo "## 5) Scripts/governance folder listing (quick sanity)"
  ls -la scripts/governance 2>/dev/null || echo "No scripts/governance folder"
  echo
  echo "=== END REPORT ==="
} | tee "$REPORT"

echo
echo "Saved report: $REPORT"




