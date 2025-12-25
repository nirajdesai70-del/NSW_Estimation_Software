# ADR-005 — Master Data Governance Firewall (No Auto-Create + Import Approval Queue)

**Status:** ACCEPTED  
**Date:** 2025-12-18  
**Decision Owner:** Phase-5 Governance Team  
**Applies To:** NSW (CIM / MASTER / Import Pipeline), all runtime controllers/services, all import handlers  
**Related Docs:** 
- `docs/PHASE_5/00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md`
- Phase-4 S2 isolation packs (CIM/SHARED/MBOM/FEED/MASTER/EMP)

---

## Context

Legacy NEPL/NSW baseline shows repeated semantic drift caused by:
- Runtime auto-creation of masters (Category/Subcategory/Item/Product/Attribute/Make/Series)
- Inconsistent naming/ID semantics, fuzzy matching, and silent defaults (e.g., FK=0)
- Imports creating new masters on-the-fly, producing duplication and long-term contamination

**Evidence:** Legacy `ImportController` patterns include:
- `Category::firstOrCreate(['Name' => $row['category']])`
- `SubCategory::firstOrCreate([...])`
- `Item::firstOrCreate([...])`
- `Product::firstOrCreate([...])`
- `Attribute::create([...])`

These patterns cause category explosion, semantic drift, and data quality degradation.

NSW is being rebuilt to support clean canonical meaning and a stable master-data layer. There is no cutover pressure requiring historical continuity.

---

## Decision

Adopt a **Master Data Governance Firewall** as a canonical architecture rule-set:

### 1. No Auto-Create Masters (Hard Constraint)

Runtime code (controllers/services/import handlers) must not create master entities during normal operations.

**Allowed pathways:**
- UI-only master creation forms (MASTER module, role-based access)
- Controlled import pipeline (pre-approved masters only)
- Admin-only API endpoints (explicit, audited)

**Forbidden patterns:**
- `Category::firstOrCreate(...)`
- `Item::create(...)` in import handlers
- Any runtime master creation outside MASTER module

### 2. Import Approval Queue Policy (Human-in-the-loop)

If an import references an unknown master:
- Reject row (or reject full import at Gate-0, depending on mode)
- Log rejection and context
- Queue unknown masters for admin approval/mapping
- Allow re-run only after master resolution

**Tables:**
- `import_pending_master_approval_queue` - Pending masters awaiting approval
- `import_decision_log` - Row-level accept/reject/queue decisions
- `import_run_log` - High-level import execution summary

### 3. Canonical Resolver Rules (Deterministic)

Master lookups must use strict canonical keys with explicit "not found" handling.

**Canonical keys:**
- Category: `Name` (unique)
- Subcategory: `Name` + `CategoryId` (unique within category)
- Item: `Name` + `CategoryId` (unique within category)
- Product (Generic): `Name` + `CategoryId` + `ProductType=1` (unique)
- Product (Specific): `SKU` (if present) OR `Name` + `CategoryId` + `MakeId` + `SeriesId` + `ProductType=2`
- Make: `Name` (unique)
- Series: `Name` + `MakeId` (unique within make)
- Attribute: `Name` (unique)

**No fuzzy matching, no silent defaults.**

### 4. Schema Enforcement

NSW schema must enforce:
- **FK integrity** - Optional = NULL, never 0
- **Unique constraints** - For canonical keys
- **Check constraints** - For enums/valid values

### 5. Auditability

Every master creation and import decision must be auditable:
- **Master creation audit** - Who/when/why/source
- **Import run log** - Summary (processed/rejected/queued counts)
- **Import decision log** - Row-level decisions
- **Pending master queue lifecycle** - Approve/map/reject tracking

---

## Rationale

- **Protects NSW canonical semantics** from legacy contamination
- **Prevents exponential master "explosion"** and duplicates
- **Makes imports predictable and reversible** (full audit trail)
- **Aligns with product-grade governance** and audit expectations
- **Enables clean schema design** and future multi-tenant scaling safely

---

## Consequences

### Positive

- Canonical structure stays clean and defensible
- Controlled data onboarding with full traceability
- Less downstream rework in pricing/BOM/quotation logic due to cleaner masters
- Audit-ready for compliance requirements

### Trade-offs

- Imports may be slower initially due to approval queue
- Requires admin review workflow and discipline
- Some legacy "it just works" behavior is intentionally removed (this is a feature, not a bug)

---

## Implementation Notes (Non-Exhaustive)

### Code Bans

- `firstOrCreate` for masters in import/controllers (except MASTER UI/admin APIs)
- Runtime `create()` for masters in import handlers
- Default FK=0 (use NULL for optional)
- Silent fallbacks on master lookup failure

### Required Patterns

- Gate-0: Pre-import validation of master references
- Row-level validation: Each row validates masters before processing
- Exceptions: `CanonicalMasterNotFoundException`, `CanonicalAmbiguityException`
- Lookup pattern: `where()->first()` with explicit "not found" handling

### Tables (Design Targets)

- `import_run_log` - Import execution summary
- `import_decision_log` - Row-level decisions
- `import_pending_master_approval_queue` - Pending masters
- `master_creation_audit` - Master creation audit trail

### Database Constraints

- Foreign keys: NULL for optional (never 0)
- Unique constraints on canonical keys
- Check constraints for enums (ProductType, Status, etc.)
- Referential integrity enforced

---

## Alternatives Considered

### 1. Migrate legacy data as-is

**Rejected because:**
- Reintroduces semantic drift
- Breaks canonical model
- Permanent contamination of NSW structure

### 2. Fuzzy match + auto-map

**Rejected because:**
- Causes silent wrong mappings
- Non-auditable
- Guesses business meaning (unreliable)

### 3. Allow runtime auto-create with cleanup later

**Rejected because:**
- Cleanup never ends
- Data becomes untrustworthy
- Exponential technical debt

---

## Validation / Acceptance Criteria

- [ ] No runtime path can create masters without explicit admin action
- [ ] Unknown master references are rejected/queued, never silently created
- [ ] Database prevents FK=0 and prevents canonical duplicates
- [ ] Audit logs can answer: "Why does this master exist?" and "Why was this row rejected?"
- [ ] Code review checklist catches forbidden patterns
- [ ] Schema constraints enforce rules at database level

---

## Legacy vs NSW Semantic Boundary

### Critical Distinction

**S4 SHARED contracts (CatalogLookupContract, ReuseSearchContract) are Legacy Lookup Contracts v1, not NSW Canonical Contracts.**

- **S4 work:** Standardizes how legacy lookups are consumed (reduces drift, centralizes behavior)
- **Phase-5 work:** Defines NSW canonical contracts separately (clean rebuild, firewall governance)
- **Legacy and NSW are two different truth layers** (explicit separation)

**Rule:** S4 does NOT redefine master semantics. Phase-5 defines NSW canonical model separately.

### Full Boundary Document

**Reference:** `docs/PHASE_4/LEGACY_VS_NSW_SEMANTIC_BOUNDARY.md`

This document provides:
- Complete explanation of two truth layers (Legacy vs NSW)
- Naming conventions (Legacy CatalogLookupContract v1 vs NSW Canonical Catalog Contract)
- What S4 does vs what Phase-5 does
- Mental model to prevent semantic confusion

**All Phase-5 work must respect this boundary to prevent mapping legacy masters to NSW canonical entities.**

---

## References

- **Full Governance Document:** `docs/PHASE_5/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md`
- **Phase 4 Isolation:** S2 isolation packs (CIM/SHARED/MBOM/FEED/MASTER/EMP)
- **Legacy Evidence:** `source_snapshot/app/Http/Controllers/ImportController.php`
- **Phase 5 Scope:** `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md`
- **Legacy vs NSW Boundary:** `docs/PHASE_4/LEGACY_VS_NSW_SEMANTIC_BOUNDARY.md` ⭐

---

**Document Status:** ACCEPTED - Frozen Policy  
**Last Updated:** 2025-12-24 (added Legacy vs NSW boundary reference)  
**Next Review:** After Phase 5 Step-1 completion (Data Dictionary freeze)

