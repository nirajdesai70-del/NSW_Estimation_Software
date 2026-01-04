#!/bin/bash
# Force Finder to refresh and show files on T9 drive

echo "=== Force Finder Refresh Script ==="
echo ""

# Step 1: Clean up resource forks
echo "1. Cleaning up resource forks..."
find /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/output -name "._*" -delete 2>/dev/null
echo "   ✓ Resource forks removed"

# Step 2: Touch all files to update timestamps
echo "2. Updating file timestamps..."
find /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/output -type f -name "*.xlsx" ! -name "~$*" -exec touch {} \; 2>/dev/null
echo "   ✓ File timestamps updated"

# Step 3: Create a visible marker file
echo "3. Creating visibility test file..."
echo "FILES EXIST - Created $(date)" > /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/output/FILES_EXIST.txt
echo "   ✓ Test file created"

# Step 4: List all files
echo ""
echo "4. Files in output directory:"
ls -lh /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/output/*.xlsx 2>/dev/null | awk '{print "   - " $9 " (" $5 ")"}'

echo ""
echo "=== Next Steps ==="
echo "1. Press Option + Command + Esc"
echo "2. Select 'Finder' and click 'Relaunch'"
echo "3. Navigate to: T9 → Projects → Projects → NSW_Estimation_Software → tools → catalog_pipeline_v2 → output"
echo "4. Press Command + R to refresh"
echo ""
echo "If you can see FILES_EXIST.txt but not .xlsx files, check Finder View Options (Command + J)"
echo "   - Make sure 'Arrange by' is set to 'None'"
echo "   - Make sure no file type filters are active"




