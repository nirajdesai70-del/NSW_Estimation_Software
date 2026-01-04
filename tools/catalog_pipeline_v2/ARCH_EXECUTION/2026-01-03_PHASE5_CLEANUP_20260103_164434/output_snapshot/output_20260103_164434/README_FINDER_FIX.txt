FINDER VISIBILITY FIX
=====================

If you cannot see files in Finder, try these steps:

1. RESTART FINDER:
   - Press: Option + Command + Esc
   - Select "Finder"
   - Click "Relaunch"

2. REFRESH THE WINDOW:
   - Press: Command + R

3. CHECK VIEW OPTIONS:
   - Press: Command + J
   - Make sure "Arrange by" is set to "None"
   - Make sure no date filters are active

4. NAVIGATE TO THIS FOLDER:
   - In Finder sidebar, click on "T9"
   - Navigate to: Projects → Projects → NSW_Estimation_Software → tools → catalog_pipeline_v2 → output

5. IF STILL NOT VISIBLE:
   - Open Terminal
   - Run: cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/output
   - Run: ls -lh *.xlsx
   - You should see the files listed

Files that should be visible:
- NSW_LC1E_WEF_2025-07-15_TEST_20260103_103812.xlsx
- NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
- l1_tmp.xlsx
- l2_tmp.xlsx

If you can see this README file but not the .xlsx files, it's a Finder filtering issue.



