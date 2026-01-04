#!/bin/bash
# Cleanup Resource Fork Files from Working Directory
# Removes all ._* files (macOS resource forks) that are now ignored

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🧹 Cleaning Up Resource Fork Files"
echo ""

# Find all ._* files
RESOURCE_FORKS=$(find . -name "._*" -type f 2>/dev/null | grep -v ".git" | wc -l | tr -d ' ')

if [ "$RESOURCE_FORKS" -eq 0 ]; then
    echo "✅ No resource fork files found"
    exit 0
fi

echo "Found $RESOURCE_FORKS resource fork files"
echo ""

# Show sample
echo "Sample files (first 10):"
find . -name "._*" -type f 2>/dev/null | grep -v ".git" | head -10
echo ""

read -p "Delete these resource fork files? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Delete resource fork files
echo ""
echo "Deleting resource fork files..."
find . -name "._*" -type f 2>/dev/null | grep -v ".git" | while read file; do
    rm -f "$file"
done

DELETED=$(find . -name "._*" -type f 2>/dev/null | grep -v ".git" | wc -l | tr -d ' ')
REMAINING=$((RESOURCE_FORKS - DELETED))

echo ""
echo "✅ Deleted: $REMAINING files"
if [ "$DELETED" -gt 0 ]; then
    echo "⚠️  Remaining: $DELETED files (may be in .git or protected)"
fi
echo ""

echo "✅ Done!"

