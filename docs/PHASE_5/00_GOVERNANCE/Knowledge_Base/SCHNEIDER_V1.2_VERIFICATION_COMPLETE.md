# Schneider v1.2 Verification Complete
## Consistency Fixes Applied - Ready for Script Generation

**Status:** VERIFIED  
**Date:** 2025-01-XX  
**Purpose:** Confirmation that v1.2 document is implementation-safe and ready for full catalog conversion scripts

---

## Verification Checklist

### ✅ Fix 1: Duty Wording - VERIFIED CORRECT

**Required:** "Duty class (AC1/AC3) belongs to SC_L3. Duty-specific ratings are KVU attributes on the L1 line. Duty does not create new L2 unless OEM Catalog No changes."

**Status:** ✅ **CORRECT**
- Line 171: "Duty class (AC1 / AC3) belongs to SC_L3 (Feature Class)."
- Line 664: "Duty class (AC1/AC3) is SC_L3 (Feature Class); duty-specific ratings are KVU attributes."
- All references consistent

### ✅ Fix 2: Poles Placement - VERIFIED CORRECT

**Required:** Poles belong to SC_L1 (Construction), not SC_L2

**Status:** ✅ **CORRECT**
- Line 571: Fixed "SC_L1/2: Operation" → "SC_L2: Operation" (Operation is SC_L2, not ambiguous)
- Line 580: "SC_L1: Poles" (correct)
- Line 587: "Pole count belongs to SC_L1 (Construction)" (correct)
- All references consistent

---

## Document Status

**SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.2.md**

- ✅ All contradictions resolved
- ✅ Duty classification: SC_L3 (Feature Class) - consistent throughout
- ✅ Poles placement: SC_L1 (Construction) - consistent throughout
- ✅ L2 generation: SKU-based only - consistent throughout
- ✅ Implementation-safe: Ready for script generation

---

## Next Steps - Script Generation Plan

### Folder Structure to Create

```
tools/catalog_pipeline_v2/
├── input/
│   └── schneider/
│       ├── Schneider_CANONICAL_TABLE_v3.xlsx
│       ├── Switching _Pricelist_WEF 15th Jul 25.xlsx
│       └── Switching & Controlling_Pricelist_WEF 15th Jul 25.pdf
├── scripts/
│   ├── build_l2_from_canonical.py
│   ├── derive_l1_from_l2.py
│   └── build_master_workbook.py
├── output/
│   └── NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
└── README.md
```

### Execution Commands

**Step 1 - Build L2 (SKU + price history):**
```bash
python tools/catalog_pipeline_v2/scripts/build_l2_from_canonical.py \
  --input tools/catalog_pipeline_v2/input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out tools/catalog_pipeline_v2/output/l2_tmp.xlsx
```

**Step 2 - Derive L1 (FULL combinations + accessories):**
```bash
python tools/catalog_pipeline_v2/scripts/derive_l1_from_l2.py \
  --l2 tools/catalog_pipeline_v2/output/l2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out tools/catalog_pipeline_v2/output/l1_tmp.xlsx
```

**Step 3 - Build final workbook:**
```bash
python tools/catalog_pipeline_v2/scripts/build_master_workbook.py \
  --l2 tools/catalog_pipeline_v2/output/l2_tmp.xlsx \
  --l1 tools/catalog_pipeline_v2/output/l1_tmp.xlsx \
  --out tools/catalog_pipeline_v2/output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
```

### Output Workbook Structure

**NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx**

1. **L2_SKU_MASTER**
   - Completed SKU only (Make + OEM Catalog No)
   - One row per completed SKU

2. **L2_PRICE_HISTORY**
   - Append-only price rows (per pricelist ref)

3. **L1_LINES**
   - BASE lines: full combinations (Duty × Voltage × any explicit variant)
   - FEATURE lines: accessories (SC_L4), linked to the BASE group

4. **L1_ATTRIBUTES_KVU**
   - KVU for each L1 line (duty, current, kW, HP, voltage etc.)

5. **EXTRACTION_LOG**
   - Page/table/row lineage + warnings

---

## Key Rules Locked for Script Implementation

### L2 Generation
- ✅ L2 rows = count(distinct (Make, Completed OEM_Catalog_No))
- ✅ Base reference + coil code = completed SKU
- ✅ Only generate completed SKUs where price exists

### L1 Generation
- ✅ Mode: `duty_x_voltage` (full combinations)
- ✅ BASE lines: Duty (AC1/AC3) × Voltage variants
- ✅ FEATURE lines: Accessories as SC_L4 (not multiplied per base)
- ✅ Many L1 lines can reference same L2 SKU (allowed)

### Accessories Handling
- ✅ Accessories appear as FEATURE lines (SC_L4)
- ✅ Each accessory has own SKU and price (if priced)
- ✅ NOT repeated per AC1/AC3 per voltage
- ✅ Engineer can mark policy later: INCLUDED / ADDON / BUNDLED

---

## Verification Complete

**Document:** `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.2.md`  
**Status:** ✅ **IMPLEMENTATION-SAFE**  
**Ready for:** Full catalog conversion script generation

**All consistency gaps fixed. Ready to proceed with script generation.**

---

**Next Action:** Generate the three Python scripts as specified in the execution plan.

