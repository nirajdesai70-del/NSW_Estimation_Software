# Fix Finder Visibility Issues on T9 Drive

## Problem
Files exist on disk (visible in Terminal) but are not showing in Finder on your T9 external drive.

## Solution Steps

### Step 1: Restart Finder
1. Press `Option + Command + Esc` (or `⌥⌘Esc`)
2. Select "Finder" from the list
3. Click "Relaunch"
4. Wait for Finder to restart

### Step 2: Refresh Finder View
1. In Finder, navigate to: `T9 → Projects → Projects → NSW_Estimation_Software → tools → catalog_pipeline_v2 → output`
2. Press `Command + R` to refresh the window
3. Or close and reopen the Finder window

### Step 3: Check Finder View Options
1. In Finder, go to **View → Show View Options** (or press `⌘J`)
2. Make sure:
   - "Show all files" is checked (if available)
   - No date filters are applied
   - Sort by: "Name" or "Date Modified"
   - Arrange by: "None" (not by date)

### Step 4: Show Hidden Files (if needed)
1. Open Terminal
2. Run: `defaults write com.apple.finder AppleShowAllFiles -bool true`
3. Press `Option + Command + Esc`
4. Select "Finder" and click "Relaunch"

### Step 5: Clear Finder Cache (if still not working)
1. Open Terminal
2. Run these commands:
   ```bash
   cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2
   find . -name ".DS_Store" -delete
   find . -name "._*" -delete
   ```
3. Restart Finder again (Step 1)

### Step 6: Verify Files Exist
In Terminal, run:
```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/output
ls -lh *.xlsx
```

You should see:
- NSW_LC1E_WEF_2025-07-15_TEST_20260103_103812.xlsx
- NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
- l1_tmp.xlsx
- l2_tmp.xlsx

## Why This Happens
- **External drives (exFAT/NTFS)**: macOS handles file visibility differently on external drives
- **Resource forks**: macOS creates `._*` files that can interfere with Finder
- **Finder cache**: Finder caches directory listings and may not refresh automatically
- **Extended attributes**: Some metadata can cause visibility issues

## Prevention
The script `build_nsw_workbook_from_canonical.py` has been updated to:
- Clear extended attributes after creating files
- Set proper file permissions
- This should prevent future visibility issues

## Quick Fix Command
Run this in Terminal to clean up and refresh:
```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2
find . -name "._*" -delete
find . -name ".DS_Store" -delete
killall Finder
```

Then manually restart Finder (Step 1 above).



