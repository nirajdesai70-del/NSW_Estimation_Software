# Catalog Governance SOP

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Applies From:** Phase-6 onward  
**Owner:** Catalog Engineering Team

---

## 1. Core Principle (Do NOT Violate)

**Catalog correctness > catalog completeness**

You are building a system, not typing a price list.

---

## 2. Why Series-Wise is Mandatory

OEM catalogs differ by:
- Voltage logic
- Duty logic
- Accessories behaviour
- SKU composition rules

Therefore:
- Each series is its own rule engine
- No global "one-script-fits-all"

---

## 3. Canonical Catalog Flow (Locked Process)

### Step 1: Select ONE Series

**Example:**
- LC1E
- LC1D
- NSX
- GV2

**Rule:** Never mix series.

---

### Step 2: Series Fundamentals Definition (Manual, Once)

Create **Series Canonical Definition:**

| Element | Required |
|---------|----------|
| Product Type | Contactor / MCCB / etc. |
| Subcategory | Power Contactor / Accessory |
| SC_L1 | Construction (Poles, Frame) |
| SC_L2 | Operation (AC / DC) |
| SC_L3 | Duty (AC1 / AC3 etc.) |
| SC_L4 | Accessories |
| Attribute set | Voltage, Current, kW, HP |
| SKU completion rules | Voltage suffix logic |
| Accessory behaviour | Add-on / bundled |

👉 **This is manual and intentional.**

---

### Step 3: Build Canonical XLSX (Per Series)

Each series gets its own canonical file.

**Sheets (minimum):**
1. **SERIES_METADATA**
2. **L2_SKU_MASTER**
3. **L2_PRICE_HISTORY**
4. **L1_RULES**
5. **ACCESSORY_RULES**
6. **ATTRIBUTE_MAP**

This is what Cursor/scripts consume.

---

### Step 4: Script Execution (Deterministic)

Scripts must:
- ❌ NOT guess
- ❌ NOT infer missing logic
- ✅ Only execute defined rules

**If rule missing → script fails loudly**

---

### Step 5: Engineer Review Gate (Mandatory)

**Checklist:**
- ✅ L2 SKU purity verified
- ✅ L1 → L2 mappings sensible
- ✅ Voltage logic correct
- ✅ Accessories not duplicated
- ✅ Price behaviour correct

**Only then → publish**

---

## 4. Accessory Handling Rule (Important)

**Accessories:**
- Are NOT contactors
- Must have:
  - Correct subcategory = Accessories
  - Series = same as parent series
  - Mapping type = ADDON / INCLUDED / BUNDLED

**Never mix accessories into base SKU logic.**

---

## 5. Versioning & Updates (Critical)

**When price list updates:**
- ❌ Do NOT touch structure
- ❌ Do NOT rebuild series rules
- ✅ Only update L2_PRICE_HISTORY

**Structure changes = new Phase / decision**

---

## 6. Anti-Patterns (Strictly Forbidden)

- ❌ Bulk pasting OEM tables
- ❌ Multi-series XLSX
- ❌ Letting scripts "figure it out"
- ❌ Completing catalogs before rules
- ❌ Treating accessories as attributes

---

## 7. Governance Rule (Lock This)

**Every catalog entry must be explainable by an engineer.**

If you can't explain it, it doesn't belong.

---

## 8. Series Execution Order (Recommended)

1. **LC1E** (Pilot - already in progress)
2. **LC1D** (Next)
3. **Accessories** (Separate from base series)
4. **Other series** (One at a time)

---

## 9. Parallel Work Safety

**Catalog work:**
- ✅ Runs in parallel with Phase-5 implementation
- ✅ Does NOT block Phase-5
- ✅ Feeds Phase-6 directly
- ✅ Can be incomplete during Phase-5

**Phase-5 implementation:**
- ✅ Assumes catalog schema exists
- ✅ Works with placeholder/partial catalog
- ✅ Does NOT depend on catalog completeness

---

## 10. Quality Gates

**Before publishing any series catalog:**

1. ✅ Series rules documented
2. ✅ Canonical XLSX validated
3. ✅ Scripts execute without errors
4. ✅ Engineer review complete
5. ✅ L2 SKU purity verified
6. ✅ L1 mappings validated
7. ✅ Accessories correctly separated
8. ✅ Price history correct

---

## 11. Change Management

**Structure changes** (L1 rules, attribute maps, etc.):
- Must be documented as series v2.0
- Must go through Decision Register if schema-impacting
- Must not break existing mappings

**Price updates:**
- Append-only (price history)
- No structure change
- Can be automated

---

## 12. Integration with Phase-5/6

**Phase-5:**
- Catalog schema exists
- Catalog content may be partial
- Implementation proceeds anyway

**Phase-6:**
- Catalog tooling built
- Series-by-series onboarding
- Validation workflows

**Phase-7:**
- Full catalog coverage
- Automated refresh
- Production hardening

---

## 📌 Key Rules Summary

1. **One series at a time**
2. **Manual rule definition first**
3. **Scripts execute, don't guess**
4. **Engineer review mandatory**
5. **Accessories separate**
6. **Price updates only**
7. **Explainable entries only**

---

**Last Updated:** 2025-01-27  
**Status:** CANONICAL  
**Next Review:** After LC1E completion

