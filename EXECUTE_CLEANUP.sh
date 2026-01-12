#!/bin/bash
# Cleanup Execution Script
# Date: 2026-01-03
# Purpose: Execute the 5 manual cleanup actions

set -e

ROOT_DIR="/Volumes/T9/Projects/Projects/NSW_Estimation_Software"
cd "$ROOT_DIR"

echo "=========================================="
echo "NSW Cleanup Execution Script"
echo "=========================================="
echo ""

# Step 1: Find and move CONTACTOR dataset
echo "Step 1: Finding CONTACTOR dataset..."
DATASET_FILE=$(find . -maxdepth 6 -name "ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx" 2>/dev/null | head -1)

if [ -n "$DATASET_FILE" ]; then
    echo "  ✓ Found: $DATASET_FILE"
    TARGET_DIR="SoR/CONTACTOR/v1.4"
    TARGET_FILE="$TARGET_DIR/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx"
    
    mkdir -p "$TARGET_DIR"
    mv "$DATASET_FILE" "$TARGET_FILE"
    echo "  ✓ Moved to: $TARGET_FILE"
else
    echo "  ⚠ NOT FOUND: ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx"
    echo "  → Please locate manually and move to: SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx"
fi

echo ""

# Step 2: Move Revised ItemMaster folder
echo "Step 2: Finding Revised ItemMaster folder..."
REVISED_FOLDER=$(find . -maxdepth 2 -type d -iname "*revised*itemmaster*" -o -iname "*itemmaster*revised*" 2>/dev/null | head -1)

if [ -n "$REVISED_FOLDER" ]; then
    echo "  ✓ Found: $REVISED_FOLDER"
    TARGET_DIR="DATA_MIGRATION_ARCHIVE/ItemMaster_Revisions"
    mkdir -p "$TARGET_DIR"
    
    FOLDER_NAME=$(basename "$REVISED_FOLDER")
    mv "$REVISED_FOLDER" "$TARGET_DIR/"
    echo "  ✓ Moved to: $TARGET_DIR/$FOLDER_NAME"
else
    echo "  ⚠ NOT FOUND: Revised ItemMaster folder"
    echo "  → If it exists elsewhere, move manually to: DATA_MIGRATION_ARCHIVE/ItemMaster_Revisions/"
fi

echo ""

# Step 3: Archive root-level deprecated folders
echo "Step 3: Archiving root-level deprecated folders..."
ARCHIVE_DIR="ARCH/2026-01-03_PRE_CLEANUP/root_deprecated"
mkdir -p "$ARCHIVE_DIR"

DEPRECATED_FOLDERS=("input" "output" "logs" "templates")
MOVED_COUNT=0

for folder in "${DEPRECATED_FOLDERS[@]}"; do
    if [ -d "$folder" ] && [ ! -L "$folder" ]; then
        # Check if it's not part of catalog_pipeline_v2
        if [ "$folder" != "scripts" ] || [ ! -d "tools/catalog_pipeline_v2/scripts" ]; then
            echo "  ✓ Found: $folder/"
            mv "$folder" "$ARCHIVE_DIR/" 2>/dev/null && ((MOVED_COUNT++)) || echo "    ⚠ Could not move $folder (may be in use)"
        else
            echo "  ⊘ Skipped: $folder/ (part of catalog_pipeline_v2)"
        fi
    fi
done

# Handle scripts separately (check if it's not v2 scripts)
if [ -d "scripts" ] && [ ! -d "tools/catalog_pipeline_v2/scripts" ]; then
    echo "  ✓ Found: scripts/"
    mv "scripts" "$ARCHIVE_DIR/" 2>/dev/null && ((MOVED_COUNT++)) || echo "    ⚠ Could not move scripts (may be in use)"
elif [ -d "scripts" ]; then
    echo "  ⊘ Skipped: scripts/ (catalog_pipeline_v2/scripts exists, keeping root scripts)"
fi

if [ $MOVED_COUNT -eq 0 ]; then
    echo "  ✓ No deprecated folders found at root (or already archived)"
fi

echo ""

# Step 4: Verification
echo "Step 4: Verification..."
echo ""

# Check if dataset is in correct location
if [ -f "SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx" ]; then
    echo "  ✅ CONTACTOR dataset: SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx"
else
    echo "  ⚠ CONTACTOR dataset: NOT FOUND in SoR/"
fi

# Check folder structure
if [ -d "SoR" ] && [ -d "SoE" ] && [ -d "SoW" ] && [ -d "ARCH" ]; then
    echo "  ✅ Folder structure: SoR/, SoE/, SoW/, ARCH/ exist"
else
    echo "  ⚠ Folder structure: Missing some folders"
fi

echo ""
echo "=========================================="
echo "Cleanup Complete (automated steps)"
echo "=========================================="
echo ""
echo "⚠ MANUAL STEPS REMAINING:"
echo ""
echo "1. Add README_DATASET_CONTROL sheet to Excel:"
echo "   - Open: SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx"
echo "   - Insert new sheet at position 1: README_DATASET_CONTROL"
echo "   - Copy content from: SoR/CONTACTOR/v1.4/README_DATASET_CONTROL.md"
echo ""
echo "2. Apply Excel protection:"
echo "   - DATA sheets: Blue tab + protect (allow filter/sort)"
echo "   - README sheets: Green tab + protect"
echo "   - Archive sheets: Red tab + protect"
echo ""
echo "See CLEANUP_EXECUTION_SUMMARY.md for detailed instructions."
echo ""



