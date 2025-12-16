#!/bin/bash

# NSW_Estimation_Software – Snapshot Copy Script
# Purpose: Safely copy files from ../nish into source_snapshot/ for reference
# WARNING: This script ONLY copies. It does NOT modify the original ../nish repository.

SRC="../nish"
DST="./source_snapshot"

# Check if source directory exists
if [ ! -d "$SRC" ]; then
    echo "ERROR: Source directory '$SRC' does not exist."
    echo "Please verify the path to the original NEPL system."
    exit 1
fi

# Create destination directory if it doesn't exist
mkdir -p "$DST"

# Copy files using rsync (excludes .git, node_modules, vendor)
rsync -av \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='vendor' \
  --exclude='.env' \
  --exclude='*.log' \
  --exclude='.DS_Store' \
  "$SRC/" "$DST/"

echo "✅ Snapshot copy completed safely."
echo "📁 Source: $SRC"
echo "📁 Destination: $DST"
echo ""
echo "⚠️  REMINDER: source_snapshot/ is read-only reference."
echo "   Do NOT edit files inside it. Use it only for documentation and trace."

