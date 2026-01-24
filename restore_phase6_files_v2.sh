#!/bin/bash
# Restore all Phase 6 files from git history to current filesystem
# Only restores root-level files, not RAG_KB duplicates

set -e

REPO_ROOT="/Volumes/T9/Projects/NSW_Estimation_Software"
cd "$REPO_ROOT"

echo "=========================================="
echo "Restoring Phase 6 Files from Git History"
echo "=========================================="
echo ""

# Find all Phase 6 files in git history (root level only, exclude RAG_KB)
echo "Step 1: Finding root-level Phase 6 files in git history..."
git log --all --full-history --name-only --pretty=format: | \
    grep -iE "phase.*6|phase6|phase_6" | \
    grep "\.md$" | \
    grep -v "^RAG_KB/" | \
    grep -v "^docs/PHASE_3/" | \
    grep -v "^docs/PHASE_5/02_FREEZE_GATE/" | \
    grep -v "^docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/" | \
    grep -v "^tools/catalog_pipeline_v2/" | \
    grep -v "^trace/" | \
    sort -u > /tmp/phase6_files_root.txt

TOTAL_FILES=$(wc -l < /tmp/phase6_files_root.txt | tr -d ' ')
echo "Found $TOTAL_FILES root-level Phase 6 files in git history"
echo ""

# Restore files
echo "Step 2: Restoring files..."
RESTORE_COUNT=0
SKIP_COUNT=0
FAILED_COUNT=0

while IFS= read -r file; do
    # Skip if file already exists
    if [ -f "$file" ]; then
        echo "  ✓ Already exists: $file"
        ((SKIP_COUNT++))
        continue
    fi
    
    # Find all commits where this file exists
    COMMITS=$(git log --all --full-history --oneline -- "$file" | awk '{print $1}')
    
    if [ -z "$COMMITS" ]; then
        echo "  ⚠️  No commit found for: $file"
        ((FAILED_COUNT++))
        continue
    fi
    
    # Try each commit until one works
    RESTORED=0
    for COMMIT in $COMMITS; do
        # Create directory if needed
        mkdir -p "$(dirname "$file")"
        
        # Try to restore file from git history
        if git show "$COMMIT:$file" > "$file" 2>/dev/null; then
            echo "  ✓ Restored: $file (from commit $COMMIT)"
            ((RESTORE_COUNT++))
            RESTORED=1
            break
        fi
    done
    
    if [ $RESTORED -eq 0 ]; then
        echo "  ⚠️  Failed to restore: $file (tried all commits)"
        ((FAILED_COUNT++))
    fi
done < /tmp/phase6_files_root.txt

echo ""
echo "=========================================="
echo "Summary:"
echo "  Total files found: $TOTAL_FILES"
echo "  Files already exist: $SKIP_COUNT"
echo "  Files restored: $RESTORE_COUNT"
echo "  Files failed: $FAILED_COUNT"
echo "=========================================="
echo ""

if [ $RESTORE_COUNT -gt 0 ]; then
    echo "✅ Successfully restored $RESTORE_COUNT files!"
    echo ""
    echo "Next steps:"
    echo "  1. Review the restored files"
    echo "  2. Stage them: git add ."
    echo "  3. Commit: git commit -m 'Restore Phase 6 files from git history'"
else
    echo "⚠️  No files were restored. Check if files already exist or if there are path issues."
fi
echo ""
