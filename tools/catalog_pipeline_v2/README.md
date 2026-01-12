# NSW Phase-5 Catalog Pipeline v2

**Purpose:** Convert Schneider canonical table into Engineer Review workbook with L2 SKU Master, L2 Price History, L1 Lines, and L1 Attributes KVU.

**Status:** ✅ **VERIFICATION SYSTEM ACTIVE** (v2.1) - See `VERIFICATION_SYSTEM_ROLLOUT_COMPLETE.md`

---

## 🚀 Quick Start for New Series

**For converting a new catalog series (LC1D, LC1F, MCCB, etc.):**

1. **Read the operating model**: See [`OPERATING_MODEL.md`](OPERATING_MODEL.md)
2. **Use the bootstrap guide**: See [`NEXT_SERIES_BOOTSTRAP.md`](NEXT_SERIES_BOOTSTRAP.md)
3. **Copy templates**: Templates are in [`templates/`](templates/)

**Standard workflow:**
- **Cursor** = Execution (run pipeline, generate outputs)
- **ChatGPT** = Governance (review, approve freeze)

---

## Overview

This pipeline consists of 3 scripts that convert a canonical catalog table into a structured Engineer Review workbook:

1. **build_l2_from_canonical.py** - Converts canonical table to L2 SKU Master and Price History
2. **derive_l1_from_l2.py** - Derives L1 lines with duty×voltage combinations and accessories
3. **build_master_workbook.py** - Assembles final Engineer Review workbook

---

## Standard Folder Structure (Phase-5)

```
catalog_pipeline_v2/
├── active/                       # 🟡 Work in progress
│   └── schneider/
│       └── <SERIES>/            # Active series conversion
│           ├── 00_inputs/
│           ├── 01_working/
│           ├── 02_outputs/
│           ├── 03_qc/
│           ├── 04_docs/
│           ├── run_pipeline.sh
│           └── README.md
│
├── archives/                     # ✅ Frozen history
│   └── schneider/
│       └── <SERIES>/
│           └── <WEF_YYYY-MM-DD>/
│               ├── 00_inputs/
│               ├── 01_scripts/
│               ├── 02_outputs/
│               ├── 03_qc/
│               ├── 04_docs/
│               ├── 05_decisions/
│               └── README.md
│
├── scripts/                      # Shared pipeline scripts
├── templates/                    # Reusable templates
│   ├── QC_SUMMARY_TEMPLATE.md
│   ├── run_pipeline.sh
│   └── README_ACTIVE_SERIES.md
│
├── OPERATING_MODEL.md            # Operating model (Cursor + ChatGPT)
├── NEXT_SERIES_BOOTSTRAP.md     # Bootstrap guide for new series
└── README.md                     # This file
```

**Legacy folders** (still supported):
- `input/` - Legacy input location
- `output/` - Legacy output location

---

## Folder Structure (Legacy)

```
catalog_pipeline_v2/
├── input/
│   └── schneider/
│       └── Schneider_CANONICAL_TABLE_v3.xlsx
├── scripts/
│   ├── build_l2_from_canonical.py
│   ├── derive_l1_from_l2.py
│   └── build_master_workbook.py
├── output/
│   ├── l2_tmp.xlsx
│   ├── l1_tmp.xlsx
│   └── NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
├── logs/
└── README.md
```

---

## Setup

### 1. Prerequisites

- Python 3.7+
- Required packages:
  ```bash
  pip install pandas openpyxl
  ```

### 2. Prepare Input File

Copy your canonical table file to the input location:

```bash
cp "/path/to/Schneider_CANONICAL_TABLE_v3.xlsx" \
   "input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx"
```

If the file is already in the project root:

```bash
cp "/Users/nirajdesai/Projects/NSW_Estimation_Software/Schneider_CANONICAL_TABLE_v3.xlsx" \
   "input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx"
```

---

## Usage

### Step 1: Build L2 from Canonical Table

Converts canonical table into L2 SKU Master and Price History.

**Command:**

```bash
python scripts/build_l2_from_canonical.py \
  --input input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out output/l2_tmp.xlsx
```

**Parameters:**
- `--input`: Path to canonical table Excel file
- `--pricelist_ref`: Price list reference (e.g., "WEF 15 Jul 2025")
- `--effective_from`: Effective date in YYYY-MM-DD format
- `--currency`: Currency code (default: INR)
- `--region`: Region (default: INDIA)
- `--out`: Output Excel file path

**Output:**
- Creates `output/l2_tmp.xlsx` with sheets:
  - `L2_SKU_MASTER`: Distinct completed SKUs only
  - `L2_PRICE_HISTORY`: Price rows per SKU

---

### Step 2: Derive L1 from L2

Creates L1 lines with full combinations (Duty × Voltage) and accessories as FEATURE lines.

**Command:**

```bash
python scripts/derive_l1_from_l2.py \
  --l2 output/l2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out output/l1_tmp.xlsx
```

**Parameters:**
- `--l2`: Input L2 Excel file (from Step 1)
- `--l1_mode`: L1 creation mode (`duty_x_voltage` or `base_only`)
- `--include_accessories`: Include accessories as FEATURE L1 lines (`true` or `false`)
- `--out`: Output Excel file path

**Output:**
- Creates `output/l1_tmp.xlsx` with sheets:
  - `L1_LINES`: BASE lines (duty×voltage combinations) + FEATURE lines (accessories)
  - `L1_ATTRIBUTES_KVU`: KVU attributes per L1 line

**Rules Applied:**
- Duty AC1/AC3: SC_L3 labels on L1. Ratings (Current A, kW, HP) are KVU attributes.
- Voltage: KVU attribute on L1. Creates multiple L1 lines in full-combination mode.
- Accessories: FEATURE L1 lines (SC_L4), linked to BASE group, NOT multiplied per duty/voltage.

---

### Step 3: Build Master Workbook

Assembles final Engineer Review workbook with all sheets.

**Command:**

```bash
python scripts/build_master_workbook.py \
  --l2 output/l2_tmp.xlsx \
  --l1 output/l1_tmp.xlsx \
  --out output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
```

**Parameters:**
- `--l2`: Input L2 Excel file (from Step 1)
- `--l1`: Input L1 Excel file (from Step 2)
- `--out`: Output Engineer Review workbook path

**Output:**
- Creates final workbook with sheets:
  1. `L2_SKU_MASTER`: Distinct completed SKUs only
  2. `L2_PRICE_HISTORY`: Price history rows per SKU
  3. `L1_LINES`: BASE lines (full combinations) + FEATURE lines (accessories)
  4. `L1_ATTRIBUTES_KVU`: KVU attributes per L1 line

---

## Complete Pipeline (One Command)

Run all three steps in sequence:

```bash
# Step 1: Build L2
python scripts/build_l2_from_canonical.py \
  --input input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out output/l2_tmp.xlsx

# Step 2: Derive L1
python scripts/derive_l1_from_l2.py \
  --l2 output/l2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out output/l1_tmp.xlsx

# Step 3: Build Master Workbook
python scripts/build_master_workbook.py \
  --l2 output/l2_tmp.xlsx \
  --l1 output/l1_tmp.xlsx \
  --out output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
```

---

## Rules (LOCKED)

### L2 Generation Rules

1. **L2 row = distinct (Make + Completed OEM_Catalog_No)** present in catalog
2. **Completed SKU rule:** Base reference with '*' must be completed using coil code columns (M7/N7/F7/B7 and BD/FD/MD etc.) **ONLY when a numeric price exists**
3. **No combinatorial multiplication** - only SKUs with prices create L2 rows

### L1 Generation Rules

1. **Duty AC1/AC3:** SC_L3 labels on L1. Ratings (Current A, kW, HP) are KVU attributes on L1.
2. **Voltage:** KVU attribute on L1. Voltage creates multiple L1 lines in full-combination mode.
3. **Accessories:** Create FEATURE L1 lines (SC_L4) once per base group; **DO NOT multiply** accessories per duty/voltage combinations.
4. **Frame:** Derived classification only; never multiplies.

---

## Output Structure

### Sheet: L2_SKU_MASTER

| Column | Description | Example |
|--------|-------------|---------|
| Make | OEM manufacturer | Schneider |
| OEM_Catalog_No | Completed SKU | LC1E0601M7 |
| OEM_Series_Range | Series name | Easy TeSys |
| SeriesBucket | Series code | LC1E |
| Item_ProductType | Product type | Contactor |
| Business_SubCategory | Business subcategory | Power Contactor |
| UOM | Unit of measure | EA |
| IsActive | Active status | TRUE |

### Sheet: L2_PRICE_HISTORY

| Column | Description | Example |
|--------|-------------|---------|
| Make | OEM manufacturer | Schneider |
| OEM_Catalog_No | SKU | LC1E0601M7 |
| PriceListRef | Price list reference | WEF 15 Jul 2025 |
| EffectiveFrom | Effective date | 2025-07-15 |
| Currency | Currency code | INR |
| Region | Region | INDIA |
| Rate | Price | 2875.00 |

### Sheet: L1_LINES

| Column | Description | Example |
|--------|-------------|---------|
| L1_Id | L1 line identifier | L1-000001 |
| L1_Group_Id | Group identifier | GRP-Schneider-LC1E0601 |
| L1_Line_Type | BASE or FEATURE | BASE |
| SC_L2_Operation | Operation type | AC Coil |
| SC_L3_FeatureClass | Duty class | AC1 / AC3 |
| L2_OEM_Catalog_No | Reference to L2 SKU | LC1E0601M7 |

### Sheet: L1_ATTRIBUTES_KVU

| Column | Description | Example |
|--------|-------------|---------|
| L1_Id | Reference to L1 line | L1-000001 |
| AttributeCode | Attribute code | VOLTAGE / AC1_CURRENT_A |
| AttributeValue | Attribute value | 220 / 20 |
| AttributeUnit | Attribute unit | V / A |

---

## Engineer Review Checklist

After running the pipeline, engineers should review:

- ✅ **L2_SKU_MASTER:** Distinct completed SKUs only (no duplicates)
- ✅ **L2_PRICE_HISTORY:** Price history rows per SKU (append-only)
- ✅ **L1_LINES:** BASE lines expanded (AC1/AC3 × voltage variants)
- ✅ **L1_LINES:** FEATURE lines for accessories (SC_L4), not multiplied
- ✅ **L1_ATTRIBUTES_KVU:** KVU completeness (voltage, current, kW, HP)

---

## Troubleshooting

### Error: "No completed SKUs found"

- Check that the canonical table has the expected column structure
- Verify that base references with '*' have corresponding coil code columns (M7, N7, F7, etc.)
- Ensure price columns contain numeric values

### Error: "L1 references SKUs not in L2_SKU_MASTER"

- Verify that Step 1 (build_l2_from_canonical.py) completed successfully
- Check that all SKUs in the canonical table have valid prices

### Warning: "L1_ATTRIBUTES_KVU contains L1 IDs not in L1_LINES"

- This indicates orphaned attribute rows
- Review the attribute generation logic in derive_l1_from_l2.py

---

## 🔍 Verification Requirements

**⚠️ STANDING INSTRUCTION:** All new builds and features MUST be verified in **PARALLEL** against **BOTH:**
1. **Legacy project** (`project/nish/`) - For functionality preservation and improvement
2. **NSW Fundamental Alignment Plan** (`NSW Fundamental Alignment Plan/`) - For Phase 4/4.5 standards and fundamentals compliance

**Required Documents:**
- **Standing Verification Instruction:** [`STANDING_VERIFICATION_INSTRUCTION.md`](STANDING_VERIFICATION_INSTRUCTION.md) - Complete dual verification process
- **Quick Reference Checklist:** [`VERIFICATION_CHECKLIST_QUICK_REFERENCE.md`](VERIFICATION_CHECKLIST_QUICK_REFERENCE.md) - Fast checklist for each build

### Dual Verification Process:

**Track A: Legacy Project Verification**
1. Identify legacy components related to new build
2. Map legacy features → new implementation
3. Verify no functionality loss
4. Verify improvements over legacy
5. Verify data integrity (if applicable)

**Track B: NSW Fundamental Alignment Plan Verification**
1. Review Master Fundamentals v2.0 compliance
2. Verify L0/L1/L2 canonical rules compliance
3. Check governance standards compliance
4. Review design document alignment
5. Verify gap register closure
6. Run verification queries and checklists

**Combined Verification:**
- Both tracks must pass
- Standards compliance verified
- Complete verification report and get sign-off

**This dual verification requirement is active until end-to-end software development is complete.**

---

## References

- **Schneider L1/L2 Expansion Logic:** `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L1_L2_EXPANSION_LOGIC_v1.0.md`
- **Schneider Catalog Interpretation Rules:** `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.2.md`
- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Legacy Project Reference:** `project/nish/README.md`

---

**Status:** ✅ Ready for use


