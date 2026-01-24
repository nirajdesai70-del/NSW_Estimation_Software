#!/usr/bin/env bash
set -euo pipefail

root="${1:-.}"
echo "Removing macOS artifacts under: $root"

find "$root" -name ".DS_Store" -delete
find "$root" -name "._*" -delete
find "$root" -name "__MACOSX" -type d -prune -exec rm -rf {} +

echo "Done."

