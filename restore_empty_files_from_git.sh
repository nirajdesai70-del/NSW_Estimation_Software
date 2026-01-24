#!/bin/bash
# Comprehensive script to restore all empty files from git history
# This script finds all empty markdown files and restores them from the last commit where they had content

set -e

REPO_ROOT="/Volumes/T9/Projects/NSW_Estimation_Software"
cd "$REPO_ROOT"

echo "=========================================="
echo "Restoring Empty Files from Git History"
echo "=========================================="
echo ""

# Find all empty markdown files
echo "Step 1: Finding all empty markdown files..."
find . -type f -name "*.md" -size 0 -not -path "./.git/*" > /tmp/empty_files.txt

TOTAL_EMPTY=$(wc -l < /tmp/empty_files.txt | tr -d ' ')
echo "Found $TOTAL_EMPTY empty markdown files"
echo ""

# Process each empty file
echo "Step 2: Restoring files from git history..."
RESTORED_COUNT=0
SKIP_COUNT=0
FAILED_COUNT=0
ALREADY_HAS_CONTENT=0

while IFS= read -r file; do
    # Remove leading ./ from path
    file="${file#./}"
    
    # Skip if file doesn't exist (shouldn't happen, but safety check)
    if [ ! -f "$file" ]; then
        echo "  ⚠️  File not found: $file"
        ((FAILED_COUNT++))
        continue
    fi
    
    # Verify file is actually empty
    if [ -s "$file" ]; then
        echo "  ✓ File has content (skipping): $file"
        ((ALREADY_HAS_CONTENT++))
        continue
    fi
    
    # Find all commits where this file exists
    COMMITS=$(git log --all --full-history --oneline -- "$file" 2>/dev/null | awk '{print $1}')
    
    if [ -z "$COMMITS" ]; then
        echo "  ⚠️  No git history found: $file"
        ((FAILED_COUNT++))
        continue
    fi
    
    # Try each commit until we find one with content
    RESTORED=0
    for COMMIT in $COMMITS; do
        # Get file content from this commit
        CONTENT=$(git show "$COMMIT:$file" 2>/dev/null || echo "")
        
        # Check if content is non-empty (more than just whitespace)
        if [ -n "$CONTENT" ] && [ ${#CONTENT} -gt 10 ]; then
            # Create directory if needed
            mkdir -p "$(dirname "$file")"
            
            # Restore file content
            echo "$CONTENT" > "$file"
            
            # Verify it was restored
            if [ -s "$file" ]; then
                echo "  ✓ Restored: $file (from commit $COMMIT, ${#CONTENT} chars)"
                ((RESTORED_COUNT++))
                RESTORED=1
                break
            fi
        fi
    done
    
    if [ $RESTORED -eq 0 ]; then
        echo "  ⚠️  No content found in git history: $file"
        ((FAILED_COUNT++))
    fi
done < /tmp/empty_files.txt

echo ""
echo "=========================================="
echo "Summary:"
echo "  Total empty files found: $TOTAL_EMPTY"
echo "  Files restored: $RESTORED_COUNT"
echo "  Files already had content: $ALREADY_HAS_CONTENT"
echo "  Files failed to restore: $FAILED_COUNT"
echo "=========================================="
echo ""

if [ $RESTORED_COUNT -gt 0 ]; then
    echo "✅ Successfully restored $RESTORED_COUNT files!"
    echo ""
    echo "Next steps:"
    echo "  1. Review the restored files: git status"
    echo "  2. Stage them: git add ."
    echo "  3. Commit: git commit -m 'Restore empty files from git history'"
    echo ""
    echo "Files restored:"
    git status --short | grep "^??\|^ M" | head -20
    if [ $(git status --short | grep "^??\|^ M" | wc -l) -gt 20 ]; then
        echo "... and more"
    fi
else
    echo "⚠️  No files were restored."
    if [ $FAILED_COUNT -gt 0 ]; then
        echo "   $FAILED_COUNT files could not be restored (no content in git history)."
    fi
fi
echo ""
