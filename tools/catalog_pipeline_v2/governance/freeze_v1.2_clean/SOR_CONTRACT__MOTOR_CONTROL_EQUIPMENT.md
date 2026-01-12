# System of Record (SoR) Contract — Motor Control Equipment

**Status:** 🟢 CANONICAL (Living Document)  
**Scope:** ALL Motor Control Equipment (MCE)  
**Catalog Phase:** Phase-5 (Catalog Pipeline)  
**Freeze Basis:** NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md  
**Last Updated:** 2026-01-03

---

## 📋 Document Purpose

This document defines the System of Record (SoR) for all Motor Control Equipment in NSW.

**Governance Model:** Rules are required, but when they become roadblocks, we review carefully and adopt what's useful.

**Review Trigger:** When real issues arise that require clarification or correction.

---

## 1. Purpose

Establishes:
- What data is authoritative
- What data is read-only
- What must never be inferred or modified downstream

**Applies uniformly to:**
- Power Contactors (LC1D, LC1E, etc.)
- Capacitor Duty Contactors
- K-Class Contactors
- MPCB, MCCB, ACB
- Overload Relays (OLR)
- All Motor Control Accessories (AUX, suppressors, interlocks, etc.)

---

## 2. Authoritative SoR Artifacts

**Pattern:**
```
NSW_<ITEM_OR_SERIES>_WEF_<DATE>_vX.xlsx
```

**Examples:**
- `NSW_LC1D_WEF_YYYY-MM-DD_vX.xlsx`
- `NSW_LC1E_WEF_YYYY-MM-DD_vX.xlsx`
- `NSW_MPCB_WEF_YYYY-MM-DD_vX.xlsx`

**Rule:**
- Each file is authoritative within its item scope
- All files obey this same umbrella contract
- No file may contradict this contract

**Exception Process:** If a real-world requirement contradicts this contract, document the issue and review for contract update.

---

## 3. Authoritative Sheet Set (Universal for MCE)

| Sheet | Authority |
|-------|-----------|
| `NSW_L2_PRODUCTS` | SKU identity (OEM truth) |
| `NSW_PRODUCT_VARIANTS` | Variant truth |
| `NSW_PRICE_MATRIX` | Pricing authority |
| `NSW_L1_CONFIG_LINES` | Configuration truth |
| `NSW_VARIANT_MASTER` | Variant structure |

**Reference-Only (Traceability):**
- `*_CANONICAL_ROWS`
- `*_COIL_CODE_PRICES`
- Any `_TEMPLATE` sheets

**Rule:** Reference sheets must never be consumed by UI or logic.

### 3.1. Sheet Name Normalization Rule

**Purpose:** Different scripts may output different sheet names. This rule ensures SoE consumers can depend on logical sheet roles, not hard-coded names.

**Recognized Equivalents:**

| Logical Role | Primary Name | Alternative Names |
|--------------|--------------|-------------------|
| SKU Identity | `NSW_L2_PRODUCTS` | `NSW_SKU_MASTER_CANONICAL` |
| Price Truth | `NSW_PRICE_MATRIX` | `NSW_PRICE_MATRIX_CANONICAL` |
| Configuration | `NSW_L1_CONFIG_LINES` | `NSW_L1_LINES` |
| Variants | `NSW_PRODUCT_VARIANTS` | `NSW_VARIANTS` |

**Rule:** SoE consumers should depend on logical sheet roles (via column presence or sheet metadata), not exact name matching. SoR scripts should prefer primary names, but alternative names are acceptable if they serve the same logical role.

**Exception Process:** If a new sheet name pattern emerges, document it here and review for normalization rule update.

---

## 4. Universal Level Discipline (Non-Negotiable)

**Engineering Levels:**
- **L0** → Intent (what the user wants)
- **L1** → Specification / configuration
- **L2** → OEM identity + SKU + price

**Rules:**
- Generic names exist only at L0/L1
- Make / Series / SKU exist only at L2
- Price exists only at L2

**Exception:** Identity fields (make, series_name) may appear in L1 sheets for traceability, but must not be used for logic.

---

## 5. Generic vs Identity Fields (Critical Separation)

### A. Generic Fields (STRICT)

**Must be vendor-neutral and series-neutral.**

**Examples:**
- `GenericDescriptor`
- `Item_ProductType`
- `Business_SubCategory`

**❌ Must NOT contain:**
- OEM names
- Series names
- Catalog codes

### B. Identity Fields (Allowed, Read-Only)

**Contain OEM identity for traceability only.**

**Examples:**
- `make`
- `series_name`
- `OEM_Catalog_No`
- `sku_code`

**Rules:**
- Allowed in L1 sheets
- Must NOT be used for logic
- Must NOT be scanned for generic-naming violations

---

## 6. Structural Classification (SC_Lx = SCL)

**Applies to all MCE items.**

**SC_Lx MAY contain:**
- Frame / size
- Poles
- Mounting
- Enclosure
- Terminal arrangement
- Physical construction

**SC_Lx MUST NOT contain:**
- ❌ Duty (AC1, AC3, Capacitor, K-class)
- ❌ Ratings (A, kW, HP)
- ❌ Voltage / coil type
- ❌ Capabilities (AUX, UV, SHUNT, OLR, etc.)

**Rule:** SC_Lx = Structural Classification Layer ONLY

**Exception Process:** If a real-world requirement needs duty/rating in SC_Lx, document and review for contract update.

---

## 7. Duty, Rating & Protection Logic (All MCE)

| Aspect | Where It Belongs |
|--------|------------------|
| Duty class | `SC_L3_FeatureClass` |
| Ratings (A / kW / HP) | `L1_ATTRIBUTES_KVU` |
| Voltage | KVU attributes |
| Protection logic | ❌ Not in Phase-5 |

**Applies equally to:**
- Contactors
- Capacitor duty
- K-class
- MPCB / MCCB / ACB

---

## 8. Accessories (Universal Rule)

**Accessories:**
- Are L1 FEATURE lines
- Live in separate accessory groups
- Do NOT multiply across duty / voltage

**Phase-5 Rule:**
- No compatibility enforcement
- No automatic inclusion
- Mapping deferred to engineering / Phase-6

**Future Review:** When Phase-6 rules engine is implemented, review if compatibility mapping should be added to SoR.

---

## 9. Capability Separation (Universal)

**Capabilities must exist only in:**
- `capability_codes`

**❌ No SC_Lx inference**  
**❌ No name-based inference**  
**❌ No UI-derived inference**

---

## 10. Pricing Authority (All MCE)

**Prices exist only in:**
- `NSW_PRICE_MATRIX`

**Applies to:**
- Base devices
- Variants
- Accessories

**❌ No price in L0/L1**  
**❌ No UI overrides**

**Exception Process:** If pricing logic requires L1-level pricing, document and review for contract update.

---

## 11. SoR Artifact Registry (Required)

**Purpose:** Maintain a registry of all frozen SoR artifacts to prevent teams from accidentally using wrong versions.

**Registry Format:**

| Series / Item | WEF Date | File Name | Status | File_Size (bytes) | SHA256 | Notes |
|---------------|----------|-----------|--------|-------------------|--------|-------|
| LC1E | 2025-07-15 | `NSW_LC1E_WEF_2025-07-15_v1.xlsx` | QC-Passed | 35058 | 965772ef5e18ee81d52dc05deca4c9006ac05ec2abc290525da712e54b3185a9 | Phase-5 catalog pipeline, v1.2 CLEAN compliant. Location: `active/schneider/LC1E/02_outputs/` |

**Note:** `File_Size` and `SHA256` columns are optional but recommended. They help prevent "someone edited the file after QC" issues and enable integrity verification. Use `-` if not yet calculated.

**Status Values:**
- **Draft** — In progress, not yet validated
- **QC-Passed** — Validated, ready for governance review
- **Frozen** — Approved and locked (no further changes)

**Maintenance:** Update this registry when:
- New artifact is created
- Status changes (Draft → QC-Passed → Frozen)
- New version is created (add new row, archive old)

**Location:** This registry is maintained in this contract document. For large-scale operations, consider a separate registry file.

---

## 12. Change & Versioning Policy

| Action | Allowed |
|--------|---------|
| Edit frozen file | ❌ |
| UI-driven change | ❌ |
| Rule injection | ❌ |
| Regenerate new version | ✅ |
| Archive old version | ✅ |

**Exception Process:** If a critical correction is needed post-freeze, create new version with clear rationale.

---

## 13. Review & Correction Mechanism

**When a rule becomes a roadblock:**

1. **Document the issue** (what rule, what requirement, why it blocks)
2. **Review carefully** with:
   - Freeze docs (v1.2 CLEAN)
   - Implementation reality
   - Business requirement
3. **Propose correction:**
   - Rule update (if freeze doc needs change)
   - Implementation fix (if script needs change)
   - Contract clarification (if interpretation is unclear)
4. **Update this contract** with resolution
5. **Commit change** with clear rationale

**Principle:** Rules are required, but when they block progress, we review and adopt what's useful.

---

## 14. Final Authority Statement

**For all Motor Control Equipment, this SoR defines truth. Anything outside it does not exist.**

**Exception:** When real issues arise, we review and correct, then update this contract.

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-01-03 | Initial contract created | Phase-5 LC1E execution complete |
| 2026-01-03 | Added SoR Artifact Registry (Section 11) | Prevent wrong version usage |
| 2026-01-03 | Added Sheet Name Normalization Rule (Section 3.1) | Handle script name variations |
| 2026-01-03 | Moved to shared governance folder | Prevent divergence across series |
| 2026-01-03 | Added File_Size and SHA256 columns to Artifact Registry | Integrity verification support |
| 2026-01-03 | Updated LC1E registry entry with size/hash | Gate I validation complete |

---

**Next Review:** When next series is processed, or when real issues arise that require contract clarification.

