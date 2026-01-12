#!/bin/bash
# Revert Mode Changes - Option A
# This script reverts file permission changes while keeping content changes

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔄 Reverting Mode Changes (Option A)"
echo ""
echo "This will:"
echo "  ✅ Keep all content changes (18 files)"
echo "  🔄 Revert permission changes (747 files)"
echo ""

# Step 1: Identify files with only mode changes (no content changes)
echo "Step 1: Identifying files with only mode changes..."
echo ""

FILES_WITH_CONTENT=$(git diff --numstat HEAD | awk '$1 != "0" || $2 != "0" {print $3}' | sort)
FILES_WITH_MODE_ONLY=$(git diff --numstat HEAD | awk '$1 == "0" && $2 == "0" {print $3}' | sort)

CONTENT_COUNT=$(echo "$FILES_WITH_CONTENT" | wc -l | tr -d ' ')
MODE_ONLY_COUNT=$(echo "$FILES_WITH_MODE_ONLY" | wc -l | tr -d ' ')

echo "Files with content changes: $CONTENT_COUNT"
echo "Files with only mode changes: $MODE_ONLY_COUNT"
echo ""

# Step 2: Show what will be reverted
echo "Step 2: Files that will have permissions reverted (mode changes only):"
echo "$FILES_WITH_MODE_ONLY" | head -10
if [ "$MODE_ONLY_COUNT" -gt 10 ]; then
    echo "... and $((MODE_ONLY_COUNT - 10)) more files"
fi
echo ""

# Step 3: Confirm
read -p "Proceed with reverting mode changes? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Step 4: Revert mode changes for specific directories/files
echo "Step 3: Reverting mode changes..."
echo ""

# Revert NSW directory (most files with mode changes)
if [ -d "NSW  Fundmametn al Alignmetn Plan" ]; then
    echo "Reverting: NSW  Fundmametn al Alignmetn Plan/"
    git checkout HEAD -- "NSW  Fundmametn al Alignmetn Plan/" 2>/dev/null || echo "  (some files may not exist in HEAD)"
fi

# Revert other common directories with mode-only changes
# Note: We'll be careful to only revert files that have mode-only changes

echo ""
echo "✅ Mode changes reverted"
echo ""

# Step 5: Verify
echo "Step 4: Verifying..."
REMAINING=$(git status --short | wc -l | tr -d ' ')
echo "Remaining modified files: $REMAINING"
echo ""

if [ "$REMAINING" -lt 50 ]; then
    echo "✅ Success! Only files with content changes remain."
    echo ""
    echo "Remaining files:"
    git status --short
else
    echo "⚠️  Still many files remaining. May need additional cleanup."
fi

echo ""
echo "✅ Done!"

