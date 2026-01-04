#!/usr/bin/env bash
# Catalog Pipeline v2 - Housekeeping Execution Script
# 
# Purpose: Execute the housekeeping plan to organize scripts and archive execution debris
# Usage: ./EXECUTE_HOUSEKEEPING.sh
#
# This script:
# 1. Creates ARCH_EXECUTION structure
# 2. Organizes scripts (active vs legacy)
# 3. Archives output debris
# 4. Archives documentation debris
# 5. Creates README files

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Catalog Pipeline v2 - Housekeeping"
echo "=========================================="
echo ""

# ============================================================================
# PHASE 1: Create Structure
# ============================================================================

echo "📋 Phase 1: Creating structure..."

# Create ARCH_EXECUTION structure
mkdir -p ARCH_EXECUTION/2025-12_ITERATION_1/{tmp_outputs,test_outputs,old_outputs,debug,one_off_scripts}
mkdir -p ARCH_EXECUTION/2025-12_ITERATION_2/{tmp_outputs,test_outputs,old_outputs,debug,one_off_scripts}

# Create script subfolders (for legacy/one-off only)
mkdir -p scripts/legacy

echo "   ✅ Structure created"
echo ""

# ============================================================================
# PHASE 2: Organize Scripts
# ============================================================================

echo "📋 Phase 2: Organizing scripts..."

# NOTE: We keep active scripts at scripts/ root for backward compatibility
# with templates/run_pipeline.sh. We only move legacy/one-off scripts.

# Tag active scripts (add status comment)
echo "   Tagging active scripts..."
for script in scripts/lc1e_extract_canonical.py scripts/lc1e_build_l2.py scripts/derive_l1_from_l2.py scripts/build_nsw_workbook_from_canonical.py scripts/migrate_sku_price_pack.py scripts/build_l2_from_canonical.py scripts/build_master_workbook.py; do
    if [ -f "$script" ]; then
        # Check if already tagged
        if ! grep -q "STATUS: ACTIVE" "$script" 2>/dev/null; then
            # Add tag after shebang or docstring
            if head -1 "$script" | grep -q "^#!"; then
                # Has shebang, add after first line
                sed -i '' '1a\
# STATUS: ACTIVE — Phase-5 v1.2 CLEAN
' "$script" 2>/dev/null || true
            else
                # No shebang, add at top
                echo "# STATUS: ACTIVE — Phase-5 v1.2 CLEAN" | cat - "$script" > /tmp/tagged_script && mv /tmp/tagged_script "$script" 2>/dev/null || true
            fi
        fi
    fi
done

# Move legacy scripts
echo "   Moving legacy scripts..."
if [ -f "scripts/build_nsw_workbook.py" ]; then
    # Tag before moving
    if ! grep -q "STATUS: LEGACY" "scripts/build_nsw_workbook.py" 2>/dev/null; then
        sed -i '' '1a\
# STATUS: LEGACY — superseded, do not use
' scripts/build_nsw_workbook.py 2>/dev/null || true
    fi
    mv scripts/build_nsw_workbook.py scripts/legacy/ 2>/dev/null || true
fi

# Move one-off scripts to ARCH_EXECUTION
echo "   Moving one-off scripts to ARCH_EXECUTION..."
mv scripts/apply_phase2_fixes.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/apply_phase2_fixes_openpyxl.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/apply_phase3_fixes.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/review_phase2_file.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/review_item_master_excel.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/validate_against_v6_v2.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/validate_canonical_against_source.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/inspect_lc1e_raw.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/inspect_pricelist.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
mv scripts/build_catalog_chain_master.py ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true

# Handle lc1e subfolder if it exists
if [ -d "scripts/lc1e" ]; then
    echo "   Moving scripts/lc1e subfolder..."
    mv scripts/lc1e ARCH_EXECUTION/2025-12_ITERATION_2/one_off_scripts/ 2>/dev/null || true
fi

# Keep LC1E_README.md in scripts/ root (documentation)
# (No move needed)

echo "   ✅ Scripts organized"
echo ""

# ============================================================================
# PHASE 3: Archive Output Debris
# ============================================================================

echo "📋 Phase 3: Archiving output debris..."

# Move temporary outputs
if [ -f "output/l1_tmp.xlsx" ]; then
    mv output/l1_tmp.xlsx ARCH_EXECUTION/2025-12_ITERATION_2/tmp_outputs/ 2>/dev/null || true
fi

if [ -f "output/l2_tmp.xlsx" ]; then
    mv output/l2_tmp.xlsx ARCH_EXECUTION/2025-12_ITERATION_2/tmp_outputs/ 2>/dev/null || true
fi

# Move test files
if [ -f "output/NSW_LC1E_WEF_2025-07-15_TEST_20260103_103812.xlsx" ]; then
    mv output/NSW_LC1E_WEF_2025-07-15_TEST_20260103_103812.xlsx ARCH_EXECUTION/2025-12_ITERATION_2/test_outputs/ 2>/dev/null || true
fi

# Move old outputs (if not needed)
if [ -f "output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx" ]; then
    echo "   ⚠️  Found old output: NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx"
    echo "      Keeping in output/ for now (may still be referenced)"
    # Uncomment to move:
    # mv output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx ARCH_EXECUTION/2025-12_ITERATION_1/old_outputs/ 2>/dev/null || true
fi

# Move debug files
if [ -f "output/FILES_EXIST.txt" ]; then
    mv output/FILES_EXIST.txt ARCH_EXECUTION/2025-12_ITERATION_2/debug/ 2>/dev/null || true
fi

if [ -f "output/README_FINDER_FIX.txt" ]; then
    mv output/README_FINDER_FIX.txt ARCH_EXECUTION/2025-12_ITERATION_2/debug/ 2>/dev/null || true
fi

if [ -f "output/TEST_VISIBILITY.txt" ]; then
    mv output/TEST_VISIBILITY.txt ARCH_EXECUTION/2025-12_ITERATION_2/debug/ 2>/dev/null || true
fi

# Handle lc1e subfolder in output
if [ -d "output/lc1e" ]; then
    echo "   Reviewing output/lc1e/ subfolder..."
    # Move test/tmp files, keep final if needed
    find output/lc1e -name "*TEST*" -o -name "*tmp*" -o -name "*~$*" | while read -r file; do
        mv "$file" ARCH_EXECUTION/2025-12_ITERATION_2/tmp_outputs/ 2>/dev/null || true
    done
    # Keep final files in output/lc1e/ for now
fi

echo "   ✅ Output debris archived"
echo ""

# ============================================================================
# PHASE 4: Archive Documentation (Selective)
# ============================================================================

echo "📋 Phase 4: Archiving documentation..."

# Move historical execution docs
for doc in PHASE_2_*.md PHASE_3_*.md EXECUTION_*.md EXCEL_REVIEW_*.md GAP_*.md PATCH_REVIEW_*.md CRITICAL_FIXES_APPLIED.md CANONICAL_EXTRACTOR_*.md NSW_BUILDER_FIX_COMPLETE.md FIX_FINDER_VISIBILITY.md ACCESSORIES_MASTER_GAPS_RESOLVED.md V6_*.md OPTION_B_*.md NEXT_STEPS_LC1E.md LC1E_STATUS.md PAUSE_NOTE.md REVIEW_COMPLETE_SUMMARY.md; do
    if [ -f "$doc" ]; then
        echo "   Moving: $doc"
        mv "$doc" ARCH_EXECUTION/2025-12_ITERATION_2/ 2>/dev/null || true
    fi
done

# Keep governance/reference docs (explicitly)
echo "   Keeping governance/reference docs in root:"
echo "      - README.md"
echo "      - OPERATING_MODEL.md"
echo "      - NEXT_SERIES_BOOTSTRAP.md"
echo "      - SETUP_COMPLETE.md"
echo "      - HOUSEKEEPING_PLAN.md"
echo "      - LC1E_PRICELIST_STRUCTURE.md (if exists)"
echo "      - INPUT_FILE_REQUIREMENTS.md (if exists)"

echo "   ✅ Documentation archived"
echo ""

# ============================================================================
# PHASE 5: Create README Files
# ============================================================================

echo "📋 Phase 5: Creating README files..."

# Create ARCH_EXECUTION/README.md
cat > ARCH_EXECUTION/README.md <<'EOF'
# Execution Archive

This folder contains execution debris from previous pipeline iterations.

**Structure:**
- `2025-12_ITERATION_1/` - First iteration execution artifacts
- `2025-12_ITERATION_2/` - Second iteration execution artifacts

**Subfolders:**
- `tmp_outputs/` - Temporary intermediate files
- `test_outputs/` - Test execution outputs
- `old_outputs/` - Superseded final outputs
- `debug/` - Debug files and logs
- `one_off_scripts/` - Temporary fix scripts and validation tools

**Purpose:** Archive temporary files, test outputs, and one-off scripts without deleting them.

**Rule:** New execution debris should go to `SoW/` (temporary) or `ARCH/` (after freeze), not here.
EOF

# Create scripts/README.md
cat > scripts/README.md <<'EOF'
# Pipeline Scripts

**Active Scripts** (scripts/ root):
- Scripts currently used in Phase-5 LC1E pipeline
- Kept at root level for backward compatibility with `templates/run_pipeline.sh`
- Tagged with `# STATUS: ACTIVE — Phase-5 v1.2 CLEAN`
- Includes both series-specific (lc1e_*) and generic scripts

**Legacy Scripts** (`legacy/`):
- Superseded scripts, kept for reference
- Tagged with `# STATUS: LEGACY — superseded, do not use`

**One-off Scripts** (`ARCH_EXECUTION/`):
- Temporary fix scripts and validation tools
- Moved to execution archive after use

**Note:** Active scripts remain at scripts/ root to maintain compatibility with existing templates and execution scripts.
EOF

echo "   ✅ README files created"
echo ""

# ============================================================================
# PHASE 6: Create Script Index
# ============================================================================

echo "📋 Phase 6: Creating script index..."

# Update scripts/README.md with actual script list
cat >> scripts/README.md <<'EOF'

## Active Scripts (scripts/ root)

These scripts are kept at the root level for backward compatibility with `templates/run_pipeline.sh`:

- `lc1e_extract_canonical.py` - Extract canonical from raw pricelist (LC1E-specific)
- `lc1e_build_l2.py` - Build L2 from canonical (LC1E-specific)
- `derive_l1_from_l2.py` - Derive L1 from L2 (generic)
- `build_nsw_workbook_from_canonical.py` - Build NSW workbook (PRIMARY, generic)
- `migrate_sku_price_pack.py` - Migrate SKU/price/ratings
- `build_l2_from_canonical.py` - Generic L2 builder (used by template)
- `build_master_workbook.py` - Legacy format builder (optional output)

All active scripts are tagged with: `# STATUS: ACTIVE — Phase-5 v1.2 CLEAN`
EOF

echo "   ✅ Script index updated"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "=========================================="
echo "✅ Housekeeping Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  ✅ Structure created"
echo "  ✅ Scripts organized"
echo "  ✅ Output debris archived"
echo "  ✅ Documentation archived"
echo "  ✅ README files created"
echo ""
echo "Next steps:"
echo "  1. Review moved files in ARCH_EXECUTION/"
echo "  2. Tag scripts with status comments (see Phase 6)"
echo "  3. Update any script references if paths changed"
echo "  4. Verify active scripts still work"
echo ""
echo "Note: If scripts/ paths changed, update templates/run_pipeline.sh"
echo "      to reference scripts/active/ or adjust paths accordingly."
echo ""

