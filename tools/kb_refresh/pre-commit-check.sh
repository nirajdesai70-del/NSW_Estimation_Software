#!/bin/bash
#
# Pre-commit check script (standalone version)
#
# Can be used as a git hook or manually run before commits
#

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CHAT_MIRROR_DIR="$REPO_ROOT/RAG_KB/chat_mirror"
DELTA_REPORT="$REPO_ROOT/RAG_KB/build_reports/DELTA_SINCE_LAST.md"

echo "Running pre-commit checks..."

# Check if Phase 5 docs changed (staged)
PHASE5_CHANGED=$(git diff --cached --name-only 2>/dev/null | grep -E "^docs/PHASE_5/" || true)

if [ -n "$PHASE5_CHANGED" ]; then
    DELTA_UPDATED=$(git diff --cached --name-only 2>/dev/null | grep -E "^RAG_KB/build_reports/DELTA_SINCE_LAST.md" || true)
    
    if [ -z "$DELTA_UPDATED" ]; then
        echo "⚠️  WARNING: Phase 5 docs changed but DELTA_SINCE_LAST.md not in commit"
        echo "   Run: python3 tools/kb_refresh/run_kb_refresh.py"
        WARNINGS=1
    fi
fi

# Check if any chat mirror files need attention
echo "Checking chat mirror files..."
TODAY=$(date +%Y-%m-%d)
CHAT_FILES_TODAY=$(find "$CHAT_MIRROR_DIR" -name "${TODAY}_*.md" 2>/dev/null || true)

if [ -z "$CHAT_FILES_TODAY" ]; then
    echo "ℹ️  INFO: No chat mirror files for today ($TODAY)"
fi

echo "Pre-commit checks complete"
exit 0

