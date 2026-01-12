#!/bin/bash
# Safe Mode Change Reversion - Option A
# Reverts file permissions for files with ONLY mode changes (no content changes)

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔄 Reverting Mode Changes (Option A) - Safe Method"
echo ""

# Get list of files with only mode changes (0 lines added, 0 lines deleted)
echo "Identifying files with only mode changes..."
MODE_ONLY_FILES=$(git diff --numstat HEAD | awk '$1 == "0" && $2 == "0" {print $3}')

MODE_COUNT=$(echo "$MODE_ONLY_FILES" | grep -v "^$" | wc -l | tr -d ' ')
echo "Found $MODE_COUNT files with only mode changes"
echo ""

if [ "$MODE_COUNT" -eq 0 ]; then
    echo "✅ No files with only mode changes found"
    exit 0
fi

# Show sample
echo "Sample files (first 10):"
echo "$MODE_ONLY_FILES" | head -10
echo ""

# Group by directory for safer reverting
echo "Grouping by directory..."
NSW_FILES=$(echo "$MODE_ONLY_FILES" | grep "^NSW" | head -5)
OTHER_FILES=$(echo "$MODE_ONLY_FILES" | grep -v "^NSW" | head -5)

echo "NSW directory files: $(echo "$MODE_ONLY_FILES" | grep "^NSW" | wc -l | tr -d ' ')"
echo "Other files: $(echo "$MODE_ONLY_FILES" | grep -v "^NSW" | wc -l | tr -d ' ')"
echo ""

# Confirm
read -p "Revert mode changes for these files? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Revert mode changes file by file (safer)
echo ""
echo "Reverting mode changes..."
REVERTED=0
FAILED=0

while IFS= read -r file; do
    if [ -z "$file" ]; then
        continue
    fi
    
    # Check if file exists in git
    if git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
        # File is tracked, safe to revert
        if git checkout HEAD -- "$file" 2>/dev/null; then
            REVERTED=$((REVERTED + 1))
            if [ $((REVERTED % 50)) -eq 0 ]; then
                echo "  Reverted $REVERTED files..."
            fi
        else
            FAILED=$((FAILED + 1))
        fi
    else
        # File not tracked, skip
        FAILED=$((FAILED + 1))
    fi
done <<< "$MODE_ONLY_FILES"

echo ""
echo "✅ Reverted: $REVERTED files"
if [ $FAILED -gt 0 ]; then
    echo "⚠️  Skipped: $FAILED files (not tracked in git)"
fi
echo ""

# Verify
echo "Verifying..."
REMAINING_MODE=$(git diff --numstat HEAD | awk '$1 == "0" && $2 == "0" {count++} END {print count+0}')
REMAINING_CONTENT=$(git diff --numstat HEAD | awk '$1 != "0" || $2 != "0" {count++} END {print count+0}')

echo "Remaining files with only mode changes: $REMAINING_MODE"
echo "Remaining files with content changes: $REMAINING_CONTENT"
echo ""

if [ "$REMAINING_MODE" -lt 10 ]; then
    echo "✅ Success! Most mode changes reverted."
else
    echo "⚠️  Some mode changes remain. May need manual review."
fi

echo ""
echo "✅ Done!"

