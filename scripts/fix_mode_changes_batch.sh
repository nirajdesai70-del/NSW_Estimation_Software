#!/bin/bash
# Fix Mode Changes - Batch Processing
# Removes executable bit from files with only mode changes

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔄 Fixing Mode Changes (Batch Processing)"
echo ""

# Get list of files with only mode changes
MODE_ONLY_FILES=$(git diff --numstat HEAD | awk '$1 == "0" && $2 == "0" {print $3}')

TOTAL=$(echo "$MODE_ONLY_FILES" | grep -v "^$" | wc -l | tr -d ' ')
echo "Found $TOTAL files with only mode changes"
echo ""

if [ "$TOTAL" -eq 0 ]; then
    echo "✅ No files with only mode changes"
    exit 0
fi

# Process in batches of 50
BATCH_SIZE=50
PROCESSED=0
FAILED=0

echo "Processing files in batches of $BATCH_SIZE..."
echo ""

while IFS= read -r file; do
    if [ -z "$file" ]; then
        continue
    fi
    
    # Remove executable bit
    if git update-index --chmod=-x "$file" 2>/dev/null; then
        PROCESSED=$((PROCESSED + 1))
        
        # Show progress every 50 files
        if [ $((PROCESSED % 50)) -eq 0 ]; then
            echo "  Processed $PROCESSED files..."
        fi
    else
        FAILED=$((FAILED + 1))
    fi
done <<< "$MODE_ONLY_FILES"

echo ""
echo "✅ Processed: $PROCESSED files"
if [ $FAILED -gt 0 ]; then
    echo "⚠️  Failed: $FAILED files"
fi
echo ""

# Verify
REMAINING=$(git diff --numstat HEAD | awk '$1 == "0" && $2 == "0" {count++} END {print count+0}')
CONTENT=$(git diff --numstat HEAD | awk '$1 != "0" || $2 != "0" {count++} END {print count+0}')

echo "Verification:"
echo "  Mode-only changes remaining: $REMAINING"
echo "  Content changes remaining: $CONTENT"
echo ""

if [ "$REMAINING" -eq 0 ]; then
    echo "✅ Success! All mode changes fixed."
elif [ "$REMAINING" -lt 10 ]; then
    echo "✅ Almost done! Only $REMAINING files remaining."
else
    echo "⚠️  Some files remain. May need additional processing."
fi

echo ""
echo "✅ Done!"

