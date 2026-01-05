# Inventory CSV Files - Root Cause Analysis

**Date:** 2026-01-06  
**Issue:** Full inventory CSV file (`NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv`) appeared empty during re-verification  
**Status:** Root cause identified

---

## Summary

The main full inventory CSV file (`NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv`) is **not tracked in git** and contains only the header row (82 bytes, 1 line). This file was never properly generated and committed as part of the Category-C freeze (commit 2b5b957).

---

## Root Cause

### What Happened

1. **File Status:**
   - `NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv` exists on disk but is **untracked** in git
   - File contains only header row: `table_name,column_name,data_type,nullable,default,pk,fk_ref,indexes,module_owner`
   - File size: 82 bytes (just the header)
   - Line count: 1 (header only)

2. **Git Status:**
   ```
   git status: Untracked files
   - docs/PHASE_5/04_SCHEMA_CANON/INVENTORY/NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv
   ```

3. **What Was Committed (commit 2b5b957):**
   - ✅ `NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv` - Tracked in git (31 lines, 5397 bytes)
   - ✅ `NSW_INVENTORY_DIFF_VIEW_v1.0.csv` - Tracked in git (31 lines, 1257 bytes)
   - ❌ `NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv` - **NOT committed** (only header exists)

4. **Generator Script:**
   - ✅ Script exists: `tools/generate_inventory_from_ddl.py`
   - ❌ Script was **not executed** before freeze commit
   - Script can regenerate full inventory from `schema.sql` DDL

---

## Why This Happened (Process Gap)

### Missing Steps in Freeze Process

The Category-C freeze process (Step-5) did not include:

1. **Pre-Freeze Step:** Generate full inventory CSV from DDL
   - Should have run: `python3 tools/generate_inventory_from_ddl.py`
   - Should have verified all 3 CSV files were generated

2. **Commit Step:** Include all inventory files in commit 2b5b957
   - Only 2 of 3 CSV files were committed
   - Full inventory CSV was not included

3. **Validation Step:** Verify all inventory files are in git
   - No verification that all expected files were committed
   - Only DDL validation was performed (which passed)

### Process Gap Analysis

| Step | Expected | Actual | Gap |
|------|----------|--------|-----|
| Generate Inventory CSVs | Run generator script | Script exists but not executed | ❌ Missing execution |
| Verify Files Generated | Check all 3 CSV files exist | Only 2 CSVs tracked in git | ❌ Missing verification |
| Commit Inventory Files | Include all 3 CSV files | Only 2 CSV files committed | ❌ Missing file |
| Validation Gate | Verify all artifacts committed | Only DDL validated | ⚠️ Partial validation |

---

## Impact Assessment

### Non-Blocking (Current Status)

✅ **Not a blocker** because:
- DDL (`schema.sql`) is the **canonical source of truth**
- Documentation (`NSW_SCHEMA_CANON_v1.0.md`) is comprehensive
- Key-only and diff-view CSVs are available
- Validation was completed using DDL directly
- Full inventory can be regenerated from DDL anytime

### However, Process Issue

⚠️ **Process gap** identified:
- Documentation references full inventory CSV as source of truth
- README mentions full inventory should exist
- Generator script exists but wasn't used
- Incomplete artifact set in version control

---

## What Should Have Been Done

### Correct Process (Should Have Been)

1. **Before Freeze Commit:**
   ```bash
   cd docs/PHASE_5/04_SCHEMA_CANON
   python3 tools/generate_inventory_from_ddl.py
   # Verify all 3 CSV files generated
   ls -lh INVENTORY/*.csv
   ```

2. **Commit All Files:**
   ```bash
   git add INVENTORY/NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv
   git add INVENTORY/NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv
   git add INVENTORY/NSW_INVENTORY_DIFF_VIEW_v1.0.csv
   git commit -m "Category-C Step-5: Include all inventory CSV files"
   ```

3. **Verification Checklist:**
   - ✅ All 3 CSV files exist
   - ✅ All 3 CSV files tracked in git
   - ✅ CSV files contain data (not just headers)
   - ✅ CSV counts match DDL (34 tables)
   - ✅ Coverage report validates alignment

---

## What Can Be Done Now

### Option 1: Generate and Commit (Recommended)

Since we're post-freeze, we have two options:

**Option A: Leave as-is (Document Only)**
- Document that full inventory CSV can be regenerated from DDL
- Update README to clarify generator script usage
- Accept that DDL is canonical source

**Option B: Generate and Commit (If Needed)**
- Run generator script to create full inventory
- Verify it matches DDL structure
- Commit as documentation artifact (not schema change)
- Document in commit message that it's a post-freeze artifact addition

### Recommendation

**Option A (Leave as-is)** because:
- Schema Canon v1.0 is frozen (commit 2b5b957)
- DDL is the authoritative source
- Full inventory can be regenerated on-demand
- No functional impact
- Avoids unnecessary commits post-freeze

**If full inventory is needed for tooling/automation:**
- Generate it from DDL using the generator script
- Use it locally/temporarily
- Document the regeneration process
- Don't commit unless required for tooling dependencies

---

## Lessons Learned

### Process Improvements

1. **Pre-Freeze Checklist:**
   - ✅ Verify all generator scripts have been run
   - ✅ Verify all expected output files exist
   - ✅ Verify all files are tracked in git
   - ✅ Verify file contents (not just headers)

2. **Freeze Commit Validation:**
   - ✅ Verify commit includes all expected artifacts
   - ✅ Verify no untracked files remain
   - ✅ Verify file sizes are reasonable (not just headers)

3. **Documentation:**
   - ✅ Clarify which files are required vs optional
   - ✅ Document generator script usage
   - ✅ Document canonical source of truth (DDL)

---

## Technical Details

### File States

| File | Git Status | Size | Lines | Content |
|------|-----------|------|-------|---------|
| `NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv` | ❌ Untracked | 82 bytes | 1 | Header only |
| `NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv` | ✅ Tracked | 5397 bytes | 31 | Full content |
| `NSW_INVENTORY_DIFF_VIEW_v1.0.csv` | ✅ Tracked | 1257 bytes | 31 | Full content |

### Generator Script

- **Location:** `tools/generate_inventory_from_ddl.py`
- **Purpose:** Parse `schema.sql` and generate 3 CSV inventory files
- **Status:** Script exists and is functional
- **Usage:** `python3 tools/generate_inventory_from_ddl.py`

---

## Conclusion

**Root Cause:** Full inventory CSV file was never generated and committed during the Category-C freeze process.

**Impact:** Non-blocking - DDL serves as canonical source, full inventory can be regenerated.

**Action:** Document the gap, accept current state (DDL is canonical), and improve process for future freezes.

---

**Analysis Date:** 2026-01-06  
**Status:** ✅ Root cause identified, impact assessed, recommendations provided

