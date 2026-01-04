#!/bin/bash
# Fix Git Pack Issues - Remove macOS Resource Fork Files
# This script removes ._* files from .git/objects/pack/ that cause "non-monotonic index" errors

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔧 Fixing Git Pack Issues..."
echo ""

# Check if .git/objects/pack exists
if [ ! -d ".git/objects/pack" ]; then
    echo "❌ .git/objects/pack directory not found"
    exit 1
fi

# Find and remove ._* files in .git/objects/pack
RESOURCE_FORKS=$(find .git/objects/pack -name "._*" -type f 2>/dev/null | wc -l | tr -d ' ')

if [ "$RESOURCE_FORKS" -eq 0 ]; then
    echo "✅ No resource fork files found in .git/objects/pack"
    exit 0
fi

echo "Found $RESOURCE_FORKS resource fork file(s) in .git/objects/pack"
echo ""
echo "Files to be removed:"
find .git/objects/pack -name "._*" -type f 2>/dev/null
echo ""

read -p "Remove these files? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Remove the files
find .git/objects/pack -name "._*" -type f -delete 2>/dev/null

echo "✅ Removed resource fork files from .git/objects/pack"
echo ""
echo "Verifying git status..."
git status --porcelain 2>&1 | head -5 || echo "Git status check completed (some errors may persist)"
echo ""
echo "✅ Done! Git pack issues should be resolved."

