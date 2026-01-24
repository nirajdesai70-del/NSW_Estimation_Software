#!/usr/bin/env bash
# adoption:
#   status: ADOPTED_FROM_V1
#   adopted_on: 2026-01-21
#   origin_root: "NSW Estimation Software V1.0"
#   origin_path: "tools/cleanup_mac_artifacts.sh"
#   owner: "TBD"
#   reason: "Phase C intake (governance-controlled adoption)."

set -euo pipefail

root="${1:-.}"
echo "Removing macOS artifacts under: $root"

find "$root" -name ".DS_Store" -delete
find "$root" -name "._*" -delete
find "$root" -name "__MACOSX" -type d -prune -exec rm -rf {} +

echo "Done."

