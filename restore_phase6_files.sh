#!/bin/bash
# Restore all Phase 6 files from git history to current filesystem

set -e

REPO_ROOT="/Volumes/T9/Projects/NSW_Estimation_Software"
cd "$REPO_ROOT"

echo "=========================================="
echo "Restoring Phase 6 Files from Git History"
echo "=========================================="
echo ""

# Find all Phase 6 files in git history
echo "Step 1: Finding all Phase 6 files in git history..."
git log --all --full-history --name-only --pretty=format: | \
    grep -iE "phase.*6|phase6|phase_6" | \
    grep "\.md$" | \
    sort -u > /tmp/phase6_files_all.txt

TOTAL_FILES=$(wc -l < /tmp/phase6_files_all.txt | tr -d ' ')
echo "Found $TOTAL_FILES Phase 6 files in git history"
echo ""

# Filter out files that already exist
echo "Step 2: Checking which files need to be restored..."
RESTORE_COUNT=0
SKIP_COUNT=0

while IFS= read -r file; do
    if [ -f "$file" ]; then
        echo "  ✓ Already exists: $file"
        ((SKIP_COUNT++))
    else
        # Find the commit where this file exists
        COMMIT=$(git log --all --full-history --oneline -- "$file" | head -1 | awk '{print $1}')
        
        if [ -n "$COMMIT" ]; then
            echo "  → Restoring: $file (from commit $COMMIT)"
            # Create directory if needed
            mkdir -p "$(dirname "$file")"
            # Try to restore file from git history
            # Try root path first, then RAG_KB path
            if git show "$COMMIT:$file" > "$file" 2>/dev/null; then
                echo "    ✓ Restored: $file"
                ((RESTORE_COUNT++))
            elif git show "$COMMIT:RAG_KB/work/docs/$file" > "$file" 2>/dev/null; then
                echo "    ✓ Restored from RAG_KB: $file"
                ((RESTORE_COUNT++))
            else
                echo "    ⚠️  Failed to restore: $file (tried root and RAG_KB paths)"
            fi
        else
            echo "  ⚠️  No commit found for: $file"
        fi
    fi
done < /tmp/phase6_files_all.txt

echo ""
echo "=========================================="
echo "Summary:"
echo "  Total files found: $TOTAL_FILES"
echo "  Files already exist: $SKIP_COUNT"
echo "  Files restored: $RESTORE_COUNT"
echo "=========================================="
echo ""
echo "Files restored to current filesystem."
echo "Review changes and commit when ready:"
echo "  git add ."
echo "  git commit -m 'Restore all Phase 6 files from git history'"
echo ""
