# Fundamentals Source of Truth

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
This document establishes the authoritative source of truth for Fundamentals baseline used in Phase 5 design work.

## Canonical File

**Path:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`

**Canonical Version:** v2.0

**Canonical Commit:** (To be updated when file is committed to git)

**File Status:** DRAFT FOR FREEZE

**Title:** Master Fundamentals + Catalog & Resolution Standard

## Scope Covered

This authoritative fundamentals file covers:

- **Master catalog structure**
  - Category/SubCategory/Item(ProductType) hierarchy
  - Generic vs Specific product definitions
  - L0/L1/L2 resolution levels

- **Reuse standards / reuse rules**
  - BOM editability principles
  - Copy/reuse behavior standards
  - Multi-SKU explosion rules

- **L0/L1/L2 definitions**
  - L0: Functional intent (device + feature composition, no ratings)
  - L1: Technical spec (adds ratings/specs, still non-specific)
  - L2: Specific OEM (resolves to Make + OEM Catalog No + PriceListRef + price)
  - Inheritance-based resolution model

- **BOM editability principles**
  - Copy/reuse must stay editable
  - Audit trail requirements
  - Validation rules

- **Import expectations (catalog/price)**
  - OEM price list mapping standards
  - Price versioning rules (insert new rows, never overwrite)
  - Catalog import templates and validation

- **Master hierarchy rules**
  - Category ≠ Item/ProductType (even if names match)
  - SubCategories are additive (multiple can apply)
  - Attribute mapping (definition at Type, values at Product)

- **Legacy vs NSW semantic boundary**
  - NSW canonical semantics for Phase 5
  - Explicit separation from legacy semantics
  - Mapping requirements

## Governance Rule

**All Phase-5 specs must reference this file only. Older fundamentals become reference-only.**

### Enforcement

1. **Phase 5 Data Dictionary** (`docs/PHASE_5/03_DATA_DICTIONARY/`) must align with this fundamentals baseline
2. **Phase 5 Schema Design** (`docs/PHASE_5/04_SCHEMA_CANON/`) must implement rules defined in this fundamentals file
3. **All Phase 5 governance documents** must reference this source of truth when discussing fundamentals
4. **Older fundamentals files** (v1.x or earlier) are reference-only and should not be used as authoritative sources for Phase 5 work

## References

- **Primary File:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Phase 5 Gap Analysis:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`
- **BOM Hierarchy Rules:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/CANONICAL_BOM_HIERARCHY_v1.0.md`

## Change Log

- v1.0: Created to establish Fundamentals v2.0 as authoritative source of truth for Phase 5

