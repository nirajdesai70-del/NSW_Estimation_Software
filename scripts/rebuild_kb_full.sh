#!/bin/bash

# Rebuild KB Index with Full Indexing
# This script rebuilds the KB index using --full flag to index ALL markdown files
# in RAG_KB directory, not just the curated manifest files

set -e  # Exit on error

# Get the project root directory (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🧠 Rebuilding KB index with FULL indexing (all markdown files)..."
echo ""

# Run the indexer with --rebuild and --full flags
python3 services/kb_indexer/indexer.py --rebuild --verbose --full

echo ""
echo "✅ KB rebuild complete with full indexing!"
