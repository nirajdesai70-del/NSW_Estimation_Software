# Legacy vs NSW Semantic Boundary Note

**Status:** FROZEN  
**Date:** 2025-12-24  
**Applies To:** S4 Propagation, Phase-5 NSW Dictionary, All Master Data Work  
**Authority:** S4-GOV-001, ADR-005, Phase-5 Scope Separation

---

## Purpose

This document establishes the **semantic boundary** between:
- **Legacy/NEPL lookup contracts** (S4 standardization work)
- **NSW canonical contracts** (Phase-5 dictionary and governance)

**Critical Rule:** These are **two different truth layers**. S4 does not redefine masters; it only standardizes how legacy lookups are consumed.

---

## 1. Two Truth Layers (Explicit Separation)

### 1.1 Legacy/NEPL Layer (Current Production App)

**What it is:**
- Current production database and UI behavior
- Category/Subcategory/Item/Product/Make/Series/Attributes mean whatever the current DB + UI uses today
- Not clean, but running production work
- Contains semantic drift, duplicates, and inconsistencies

**S4's role:**
- **Standardizes lookup consumption** (reduces duplicate lookup logic across modules)
- **Centralizes lookup behavior** (one SHARED contract surface instead of module-local endpoints)
- **Makes legacy safer and more maintainable** (prevents further semantic drift)
- **Does NOT redefine masters** (does not change what Category/Item/etc. mean)

**S4 SHARED Contracts:**
- `CatalogLookupContract` = **Legacy CatalogLookupContract v1**
- `ReuseSearchContract` = **Legacy ReuseSearchContract v1**
- These are **legacy lookup contracts**, not NSW canonical contracts

### 1.2 NSW Layer (Future Canonical Model)

**What it is:**
- Clean rebuild with redefined semantics
- Category/Subcategory/Type/Attributes/L0-L2 will be redefined and enforced
- Firewall rules: no auto-create, approval queue, canonical resolver
- Separate schema and governance (per ADR-005)

**Phase-5's role:**
- Define NSW canonical data dictionary
- Define NSW canonical contracts (separate from legacy contracts)
- Establish firewall governance (no legacy contamination)
- Build NSW separately without touching legacy flows

**NSW Canonical Contracts:**
- Will be defined in Phase-5
- Will be **separate** from S4 legacy contracts
- Will have different semantics, different schema, different governance

---

## 2. What S4 Actually Helps With (Even If NSW Definitions Change Later)

### 2.1 Stops Further Semantic Drift in Legacy

**Problem:** Duplicate lookup logic across modules causes "same dropdown, different rules" bugs and hidden assumptions.

**S4 Solution:** Converge all consumers to one SHARED lookup surface.

**Benefit:** Fewer inconsistencies, fewer bugs, easier to maintain legacy while NSW is built.

### 2.2 Makes the App Modular (Easier to Freeze/Deprecate Later)

**Problem:** Legacy and NSW need to coexist during transition.

**S4 Solution:** Once CIM/MBOM/etc. all pull lookups via SHARED endpoints, you can:
- Keep legacy running as-is (for business continuity)
- Build NSW separately without touching legacy flows
- Optionally swap the lookup backend later behind the SHARED contract if ever needed

**Benefit:** Clean separation allows parallel development and safe deprecation.

### 2.3 Supports "No Legacy Migration" Stance

**Decision:** Do not migrate legacy masters into NSW because they're contaminated (per ADR-005).

**S4 Alignment:** S4 keeps legacy stable and prevents the mess from growing.

**Benefit:** Legacy remains functional while NSW is built clean from scratch.

---

## 3. Preventing Mapping Confusion

### 3.1 The Risk

**Confusion occurs if:** Someone assumes "legacy Category = NSW Category" or "S4 SHARED contract = NSW canonical contract".

**Why this is wrong:**
- Legacy masters have semantic drift and inconsistencies
- NSW masters will have clean, redefined semantics
- S4 contracts are legacy lookup contracts, not NSW canonical contracts

### 3.2 The Rule

**Explicit Naming Convention:**

| Contract | Internal Name (Docs) | File Name | Layer | Purpose |
|----------|----------------------|-----------|-------|---------|
| `CatalogLookupContract` | **Legacy CatalogLookupContract v1** | `CatalogLookupContract.php` | Legacy/NEPL | Standardize legacy lookup consumption |
| `ReuseSearchContract` | **Legacy ReuseSearchContract v1** | `ReuseSearchContract.php` | Legacy/NEPL | Standardize legacy reuse search |
| NSW Catalog Contract | **NSW Canonical Catalog Contract** | TBD (Phase-5) | NSW | Clean canonical lookup for NSW |

**Documentation Rule:**
- In S4 docs, refer to SHARED contracts as "Legacy CatalogLookupContract v1" (even if file name stays the same)
- In Phase-5 docs, define NSW canonical contracts separately
- Never equate legacy contracts to NSW canonical contracts

### 3.3 The Boundary

**Legacy Layer (S4):**
- ✅ Standardize how legacy lookups are consumed
- ✅ Reduce duplicate lookup logic
- ✅ Centralize lookup behavior
- ❌ Does NOT redefine master semantics
- ❌ Does NOT create NSW canonical contracts

**NSW Layer (Phase-5):**
- ✅ Define clean canonical data dictionary
- ✅ Define NSW canonical contracts
- ✅ Establish firewall governance
- ❌ Does NOT migrate legacy masters
- ❌ Does NOT reuse legacy contracts

---

## 4. Simple Mental Model

### 4.1 S4 Work: "Make Legacy App Consistent and Safe"

**What S4 does:**
- Standardizes lookup consumption across modules
- Reduces semantic drift in legacy
- Makes legacy more maintainable
- Keeps legacy stable during NSW development

**What S4 does NOT do:**
- Redefine master semantics
- Create NSW canonical contracts
- Migrate legacy data
- Change what Category/Item/etc. mean in legacy

### 4.2 Phase-5 Work: "Define the Clean Truth Model"

**What Phase-5 does:**
- Defines NSW canonical data dictionary
- Defines NSW canonical contracts
- Establishes firewall governance
- Builds NSW separately from legacy

**What Phase-5 does NOT do:**
- Migrate legacy masters into NSW
- Reuse legacy contracts
- Touch legacy flows

### 4.3 Migration (Optional Future): "If Ever Needed, Map Legacy → NSW Through Staging + Approvals"

**If migration is ever needed:**
- Map legacy → NSW through staging + approvals
- Never direct migration (per ADR-005)
- Separate project, not part of S4 or Phase-5

---

## 5. Implementation Checklist

### 5.1 S4 Documentation Updates

- [x] This boundary note created
- [ ] S4-GOV-001 updated with boundary note reference
- [ ] S3_SHARED_ALIGNMENT.md updated to clarify "Legacy CatalogLookupContract v1"
- [ ] S3_CIM_ALIGNMENT.md updated to clarify legacy lookup context
- [ ] All S4 evidence packs reference "Legacy CatalogLookupContract v1"

### 5.2 Phase-5 Documentation Updates

- [ ] Phase-5 data dictionary explicitly separates from legacy semantics
- [ ] Phase-5 canonical contracts defined separately from legacy contracts
- [ ] ADR-005 references this boundary note
- [ ] Phase-5 scope separation docs reference this boundary note

### 5.3 Code Comments (If Needed)

- [ ] Service classes document "Legacy CatalogLookupContract v1" in class comments
- [ ] Contract interfaces document legacy layer context
- [ ] No code changes required (naming is documentation-only)

---

## 6. Authority References

**S4 Governance:**
- `docs/PHASE_4/S4_GOV_001_PROPAGATION_ORDER.md` - S4 propagation order and rules
- `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` - Legacy SHARED contract alignment
- `docs/PHASE_4/S3_CIM_ALIGNMENT.md` - Legacy CIM alignment

**Phase-5 Governance:**
- `docs/PHASE_5/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` - Firewall rules and no auto-create policy
- `docs/PHASE_5/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md` - Full governance document
- `docs/PHASE_5/SCOPE_SEPARATION.md` - Phase-5 scope separation

**Decision Authority:**
- S4 work: Legacy standardization only (no semantic redefinition)
- Phase-5 work: NSW canonical model (separate from legacy)
- Migration: Optional future project (not part of S4 or Phase-5)

---

## 7. Summary Statement

**S4 SHARED contracts are Legacy Lookup Contracts v1, not NSW Canonical Contracts.**

- S4 standardizes how legacy lookups are consumed (reduces drift, centralizes behavior)
- Phase-5 defines NSW canonical contracts separately (clean rebuild, firewall governance)
- Legacy and NSW are two different truth layers (explicit separation)
- No mapping confusion if this boundary is respected (documentation and naming conventions)

**This boundary must be maintained throughout S4 and Phase-5 work to prevent semantic confusion.**

---

**Document Status:** FROZEN  
**Last Updated:** 2025-12-24  
**Next Review:** After Phase-5 Step-1 completion (Data Dictionary freeze)

