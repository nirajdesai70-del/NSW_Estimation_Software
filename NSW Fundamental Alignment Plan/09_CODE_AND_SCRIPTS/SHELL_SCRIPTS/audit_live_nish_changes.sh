#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-/Users/nirajdesai/Projects/nish}"
DAYS="${2:-2}"   # show files modified in last N days (default 2)

if [ ! -d "$TARGET_DIR" ]; then
  echo "ERROR: Target directory not found: $TARGET_DIR"
  exit 1
fi

echo "============================================================"
echo "LIVE Repo Audit (READ-ONLY)"
echo "Target : $TARGET_DIR"
echo "Window : last $DAYS day(s)"
echo "Time   : $(date)"
echo "============================================================"
echo

cd "$TARGET_DIR"

# 1) Basic repo check
if [ ! -d ".git" ]; then
  echo "WARN: $TARGET_DIR is not a git repository (.git missing)."
  echo "Showing timestamp-based changes only."
  echo
else
  echo "---- GIT: branch + status ----"
  git rev-parse --abbrev-ref HEAD || true
  echo
  git status --porcelain || true
  echo

  echo "---- GIT: staged changes (names) ----"
  git diff --name-only --cached || true
  echo

  echo "---- GIT: working tree changes (names) ----"
  git diff --name-only || true
  echo

  echo "---- GIT: untracked files ----"
  git ls-files --others --exclude-standard || true
  echo

  echo "---- GIT: compare against origin/main (best effort) ----"
  # Try fetch without failing the whole script
  git fetch --quiet origin || true
  if git show-ref --quiet refs/remotes/origin/main; then
    echo "Files changed vs origin/main:"
    git diff --name-status origin/main...HEAD || true
  else
    echo "WARN: origin/main not found (remote missing or branch name differs)."
    echo "Tip: check your default branch name (main/master)."
  fi
  echo
fi

# 2) Timestamp-based file changes (works even if git is clean)
echo "---- FILESYSTEM: recently modified (last $DAYS day[s]) ----"
# Exclude .git directory; show newest first
find "$TARGET_DIR" \
  -path "$TARGET_DIR/.git" -prune -o \
  -type f -mtime "-$DAYS" -print0 \
  | xargs -0 -I {} stat -f "%m %Sm %N" -t "%Y-%m-%d %H:%M:%S" "{}" 2>/dev/null \
  | sort -nr \
  | head -n 200 \
  | sed 's/^[0-9]* //'
echo

# 3) Recently created files (ctime) – best effort on macOS
echo "---- FILESYSTEM: recently changed metadata (possible creates/renames) ----"
find "$TARGET_DIR" \
  -path "$TARGET_DIR/.git" -prune -o \
  -type f -ctime "-$DAYS" -print0 \
  | xargs -0 -I {} stat -f "%c %Sc %N" -t "%Y-%m-%d %H:%M:%S" "{}" 2>/dev/null \
  | sort -nr \
  | head -n 200 \
  | sed 's/^[0-9]* //'
echo

echo "============================================================"
echo "DONE. This script performs NO WRITES and makes NO DB calls."
echo "============================================================"




