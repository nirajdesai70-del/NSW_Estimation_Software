# NSW Schema Inventory Coverage Report (v1.0)

**Generated:** 2026-01-05 17:39:55  
**Status:** ✅ ALIGNED — Full and key-only inventories are synchronized

---

## Files

- **Full inventory:** `NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv`
- **Key-only inventory:** `NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv`
- **Diff view:** `NSW_INVENTORY_DIFF_VIEW_v1.0.csv`
- **Coverage report:** `NSW_INVENTORY_COVERAGE_REPORT_v1.0.md` (this file)

---

## Counts Summary

| Metric | Count |
|--------|-------|
| **Full inventory tables** | 34 |
| **Key-only inventory tables** | 34 |
| **Common tables** | 34 |
| **Tables in full only** | 0 |
| **Tables in key-only only** | 0 |
| **Module mismatches** | 0 |

---

## Coverage Status

✅ **FULLY ALIGNED** — All 34 tables are present in both inventories with matching module assignments.

### Missing Tables

**Tables present in full but missing in key-only:** 0
None ✅

**Tables present in key-only but missing in full:** 0
None ✅

---

## Module Distribution

| Module | Full Inventory | Key-Only Inventory | Status |
|--------|----------------|-------------------|--------|
| AI | 1 | 1 | ✅ Match |
| AUDIT | 1 | 1 | ✅ Match |
| AUTH | 4 | 4 | ✅ Match |
| CIM | 13 | 13 | ✅ Match |
| MBOM | 2 | 2 | ✅ Match |
| PRICING | 4 | 4 | ✅ Match |
| QUO | 5 | 5 | ✅ Match |
| SHARED | 3 | 3 | ✅ Match |
| TAX | 1 | 1 | ✅ Match |

---

## Module Mismatches

0 table(s) with module assignment differences:

**None** ✅ — All tables have consistent module assignments across both inventories.

---

## Diff View Sanity Checks

- ✅ All tables in diff view are present in both inventories
- ✅ `in_full=True` and `in_key=True` for all common tables
- ✅ Module normalization applied (blank `module` fields filled from `module_key`)

---

## Previous Report Status

**Note:** The previous coverage report (dated before this regeneration) showed:
- Full inventory: 18 tables
- Key-only inventory: 34 tables  
- Missing in full: 16 tables

**Resolution:** That report was **stale** and reflected an incomplete state during inventory generation. The current state shows:
- ✅ Both inventories are complete with 34 tables
- ✅ Zero missing tables in either direction
- ✅ All module assignments are consistent

---

## Conclusion

**Coverage Status:** ✅ **ALIGNED**

The schema inventory is ready for:
- ✅ DDL generation (schema.sql)
- ✅ Schema Canon compilation (NSW_SCHEMA_CANON_v1.0.md)
- ✅ Seed script generation (Step-4)
- ✅ Implementation validation

**Next Steps:**
1. Proceed to **Step-4 (Seed Script)** or
2. Proceed to **Step-5 (Schema Canon compilation)**

---

**Last Updated:** 2026-01-05 17:39:55  
**Version:** 1.0 (regenerated)
# Test modification - Mon Jan  5 23:43:35 IST 2026
