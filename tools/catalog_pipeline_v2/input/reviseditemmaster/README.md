# Revised Item Master Directory

**Purpose:** Contains the revised item master Excel file for review and analysis

**Expected File:** `itemmaster020126.xlsx`

**Status:** ⏳ Waiting for file to be placed in this directory

---

## File Location

Once the file is available, it should be placed at:
```
tools/catalog_pipeline_v2/input/reviseditemmaster/itemmaster020126.xlsx
```

---

## Analysis

Once the file is in place, run:

```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2
python3 scripts/review_item_master_excel.py "input/reviseditemmaster/itemmaster020126.xlsx" --output excel_review_report.json
```

This will:
1. Analyze all sheets (README, Process, Data)
2. Check for terminology conflicts
3. Compare with patch requirements
4. Generate detailed report

---

**Last Updated:** 2025-01-XX

