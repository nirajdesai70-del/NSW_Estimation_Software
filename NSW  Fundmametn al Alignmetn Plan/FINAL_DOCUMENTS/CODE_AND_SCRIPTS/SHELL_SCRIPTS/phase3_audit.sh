#!/usr/bin/env bash
set -euo pipefail

echo "=== Phase-3 Audit (L0/L1/L2 + Gap Revalidation) ==="
echo "Repo: $(pwd)"
echo

need() {
  local f="$1"
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f"
    return 1
  fi
  echo "FOUND:   $f"
}

# --- 1) Critical files existence ---
echo "## 1) Required files"
need "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md" || true
need "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md" || true
echo

# --- 2) Confirm Gap Revalidation section exists in both gap registers ---
echo "## 2) Gap Revalidation section check"
for f in \
  "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md" \
  "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md"
do
  if [[ -f "$f" ]]; then
    if grep -q "Gap Revalidation.*Phase-3" "$f" 2>/dev/null; then
      echo "PASS: $f has Gap Revalidation (Phase-3)"
    else
      echo "FAIL: $f missing Gap Revalidation (Phase-3)"
    fi
  fi
done
echo

# --- 3) Canonical L0-L1-L2 block presence in the 6 priority docs ---
echo "## 3) Canonical L0-L1-L2 block check (6 priority docs)"
docs=(
  "docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md"
  "docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md"
  "docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md"
  "docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md"
  "docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md"
  "docs/SPECIFIC_ITEM_MASTER/PLAN/SPECIFIC_ITEM_MASTER_DETAILED_DESIGN.md"
)

for f in "${docs[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f"
    continue
  fi
  if grep -q "L0.*L1.*L2.*Layer Definitions" "$f" 2>/dev/null; then
    echo "PASS: $f"
  else
    echo "FAIL: $f missing L0-L1-L2 block"
  fi
done
echo

# --- 4) Quick ambiguity scan (generic/specific without L0/L1/L2 nearby) ---
echo "## 4) Quick ambiguity scan (heuristic)"
echo "NOTE: This is a heuristic, not a blocker. Review hits manually."
if command -v rg >/dev/null 2>&1; then
  rg -n "Generic products only|Specific products only|ProductType\s*=\s*1|ProductType\s*=\s*2" docs/MASTER_BOM/DESIGN docs/NEPL_STANDARDS/00_BASELINE_FREEZE docs/SPECIFIC_ITEM_MASTER/PLAN \
    2>/dev/null | head -n 80 || true
else
  grep -rn "Generic products only\|Specific products only\|ProductType.*=.*1\|ProductType.*=.*2" docs/MASTER_BOM/DESIGN docs/NEPL_STANDARDS/00_BASELINE_FREEZE docs/SPECIFIC_ITEM_MASTER/PLAN \
    2>/dev/null | head -n 80 || true
fi
echo
echo "=== Phase-3 Audit complete ==="

