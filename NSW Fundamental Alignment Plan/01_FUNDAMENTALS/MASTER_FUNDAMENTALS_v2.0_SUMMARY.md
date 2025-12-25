# Master Fundamentals v2.0 — Creation Summary

**Date:** 2025-01-XX  
**Status:** Documentation Complete  
**Related Document:** [MASTER_FUNDAMENTALS_v2.0.md](./MASTER_FUNDAMENTALS_v2.0.md)

---

## What Was Created

A comprehensive, consolidated master fundamentals document (v2.0) that integrates:

1. **Complete fundamentals doctrine** (L0/L1/L2 hierarchy, Category vs Item, SubCategory model)
2. **Catalog & resolution standard** (Generic vs Specific products, OEM price list compatibility)
3. **Pricing ownership clarification** (L1 does NOT own price; all price truth at L2/SKU level)
4. **L1 feature lines standard** (features as separate L1 lines, not flags on base item)
5. **Multi-SKU explosion logic** (L1→L2 explosion, vendor variability, feature policy)
6. **Attribute set model** (value/unit separation, UX control)
7. **Governance and validation rules** (mandatory fields, hard validation gates)

---

## Key Corrections Integrated

### 1. Pricing Ownership (Section: 🔁 Pricing Ownership)

**Clarification:** L1 does NOT own or store price. All price truth lives at L2 (SKU) level only.

- L1 may display derived summaries in UI for convenience
- BOM totals are computed roll-ups, not stored L1 price values
- No price value at L1 is ever stored, persisted, or treated as truth

### 2. L1 Feature Lines Standard (Section: 🔁 L1 Feature Lines Standard)

**Change:** Features are represented as separate L1 lines (base + feature lines grouped), not as flags on the base item.

**Why:** This standardizes estimator intent representation across vendors, making vendor differences transparent at L2 resolution only.

**Structure:**
- One Base L1 line = main item (engineering/spec intent)
- Separate L1 feature lines = UV/OV/Shunt/Aux/etc. (each as its own line)
- Features grouped by `l1_group_id`

**L2 Resolution:**
- INCLUDED_IN_BASE → no separate L2 SKU line
- ADDON_SKU_REQUIRED → separate L2 SKU line with price
- BUNDLED_ALTERNATE_BASE → base SKU changes to bundled variant

---

## Document Structure

The master document is organized into major sections:

- **A-Q:** Core catalog & resolution fundamentals
- **R-AI:** General NSW estimation fundamentals layer
- **🔁 Sections:** Critical clarifications (pricing, feature lines)
- **Final sections:** Governance freeze statements

All sections are cross-referenced and traceable.

---

## Integration Status

✅ **Master Document:** Created as `MASTER_FUNDAMENTALS_v2.0.md`  
✅ **Index Updated:** `FUNDAMENTALS_INDEX.md` now references the new master  
✅ **README Updated:** `README.md` highlights the new master as authoritative source  
✅ **Excel Layout v1.3.2:** Added as Part 1 (feature-as-separate-L1 structure)  
✅ **L2 Explosion Service Pseudocode:** Added as Part 2 (idempotent, vendor-aware)

---

## Implementation Deliverables Status

### ✅ COMPLETED

1. ✅ **Excel Layout v1.3.2** (Part 1)
   - GENERIC_MASTER sheet structure (L1 intent layer with BASE/FEATURE lines)
   - GENERIC_ATTRIBUTES sheet structure (KVU model)
   - ATTRIBUTE_MASTER sheet structure
   - Complete column definitions and examples

2. ✅ **L2 Explosion Service Pseudocode** (Part 2)
   - Complete function specification
   - Step-by-step logic with all handling types (INCLUDED_IN_BASE, ADDON_SKU_REQUIRED, BUNDLED_ALTERNATE_BASE)
   - Idempotency guarantees
   - Audit-safe operations

### 📋 PENDING (Next Steps)

1. **DB schema** (tables + fields + keys + indexes) — derived from Excel layout
2. **CSV templates**
   - SKU price import (SKU-only, versioned)
   - Feature policy import (engineering controlled)
3. **Migration rules** (v1.3 Excel → v1.3.2)

All deliverables reference section numbers of the master document for traceability.

---

## Status

**Current Status:** DRAFT FOR FREEZE  
**Ready for:** Review and freeze approval

---

**END OF SUMMARY**

