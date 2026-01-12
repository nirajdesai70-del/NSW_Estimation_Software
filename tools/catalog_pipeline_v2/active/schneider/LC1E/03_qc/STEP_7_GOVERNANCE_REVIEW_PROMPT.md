# Step-7 Governance Review Prompt — LC1E Phase-5 (v1.2 CLEAN Replacement)

## Purpose of This Review

You are reviewing a new Phase-5 catalog pipeline output for the LC1E Contactor series.

👉 **This output is intended to REPLACE all previous LC1E outputs.**  
👉 **No alignment or migration with old files is required.**  
👉 **Old LC1E workbooks are treated as archived / non-canonical.**

The only question to answer is:

**Is this new LC1E output compliant with NSW v1.2 CLEAN rules and ready to be frozen as the single canonical source?**

---

## Authoritative Rules (ONLY these apply)

Use only the following documents for validation:
- `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md`
- `NSW_SHEET_SET_INDEX_v1.2_CLEAN.md`

❌ **Do not reference older versions**  
❌ **Do not compare with previous LC1E outputs**

---

## Artifacts Provided

1. **Primary Freeze Artifact (Excel)**
   - `NSW_LC1E_WEF_2025-07-15_v1.xlsx`

2. **Quality Control Summary**
   - `QC_SUMMARY.md`

3. **Historical Reference (Optional)**
   - `QC_PAGE8_VALIDATION.md` — Historical "golden vs rebuilt" comparison shows FAIL; not a gating requirement because this release replaces the old baseline.

This Excel file is the intended canonical replacement.

---

## Review Scope (Strict)

### 1. Structural Semantics (MANDATORY)

Confirm that:
- SC_Lx columns represent Structural Construction Layers (SCL) only
- SC_Lx does NOT contain:
  - Coil voltage
  - AC1 / AC3 duty
  - kW / HP
  - Capability tokens (WITH_*, AUX, SHUNT, UV, DRAWOUT)
- Capabilities (if any) are expressed only via `capability_codes`
- There is no SC_Lx → capability mapping

---

### 2. Generic Naming (MANDATORY)

Confirm that:
- All generic names / descriptors (L0/L1) are:
  - Vendor-neutral
  - Series-neutral
  - No OEM names (Schneider, ABB, Siemens, etc.) appear in generic fields
  - No series names (LC1E, NSX, GZ1E, etc.) appear in generic fields
- Make / Series / SKU appear only in L2 identity fields

ℹ️ **Identity fields** such as `series_name`, `make`, `sku_code` are explicitly allowed.

---

### 3. Layer Discipline (MANDATORY)

Confirm that:
- L0 / L1 / L2 separation is respected
- Make / Series / Price exist only at L2
- No BOM explosion or dependency enforcement is applied
- This remains a catalog pipeline artifact, not an estimation runtime model

---

### 4. Sheet-Set Integrity

Confirm that the workbook structure matches v1.2 CLEAN intent:
- `NSW_L2_PRODUCTS`
- `NSW_PRICE_MATRIX`
- `NSW_L1_CONFIG_LINES`
- `NSW_CATALOG_CHAIN_MASTER` (if applicable)
- `NSW_VARIANT_MASTER`

Row counts and notes should match `QC_SUMMARY.md`.

---

## Explicit Non-Goals

❌ **Do NOT request alignment with old LC1E files**  
❌ **Do NOT suggest repairing or migrating old outputs**  
❌ **Do NOT propose doctrine or semantic changes**  
❌ **Do NOT introduce BOM / estimation logic**

Old LC1E files are out of scope.

---

## Expected Response Format

Please respond with one clear outcome only:

### ✅ APPROVED — READY TO FREEZE

"This LC1E Phase-5 output complies with NSW v1.2 CLEAN rules and can replace all previous LC1E catalog outputs as the canonical source."

**OR**

### ❌ CHANGES REQUIRED

List only:
- Sheet name
- Column / row (if applicable)
- v1.2 CLEAN rule violated
- Required correction

---

## Decision Impact

- **APPROVED** → Proceed to archive old LC1E files and freeze this version
- **CHANGES REQUIRED** → Fix pipeline, regenerate, and re-review

---

**This review determines the canonical LC1E catalog baseline going forward.**




