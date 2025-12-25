# Legacy vs NSW — Coexistence Policy

**Version:** 1.0  
**Date:** 2025-12-24  
**Status:** ✅ **ACTIVE POLICY**  
**Authority:** Phase-4 S4-GOV-001, Phase-5 ADR-005, LEGACY_VS_NSW_SEMANTIC_BOUNDARY.md

---

## Purpose

This document clarifies how **Phase-4 (Legacy Stabilization)** and **Phase-5 (NSW Canonical Definition)** coexist without semantic contamination. It answers the question: *"If NSW will redefine Category/Subcategory/Type/Attribute semantics, why are we standardizing legacy lookups in Phase-4?"*

---

## ⚠️ Two Truth Layers Disclaimer

**CRITICAL RULE:** Legacy and NSW operate as **two separate truth layers**. No semantic equivalence may be assumed without explicit mapping documentation.

### Legacy Truth (Operational Truth for Current App/Runtime Only)

- **Scope:** Current production database and UI behavior
- **Semantics:** Category/Subcategory/Item/Attribute mean whatever the current DB + UI uses today
- **Status:** Operational truth for legacy/V2 runtime only
- **Contains:** Semantic drift, duplicates, and inconsistencies (acknowledged and tolerated)

### NSW Truth (Future Canonical Truth for NSW Only)

- **Scope:** Clean rebuild with redefined semantics
- **Semantics:** Category/Subcategory/Type/Attributes/L0-L2 will be redefined and enforced
- **Status:** Future canonical truth for NSW only
- **Contains:** Clean, enforceable definitions with governance firewall

### Explicit Rule

**❌ FORBIDDEN:** No one may claim "legacy category/subcategory/type = NSW category/subcategory/type" without an explicit mapping document (separate project, not part of Phase-4 or Phase-5).

**✅ REQUIRED:** Any semantic equivalence claims must be documented in a separate mapping project with explicit transformation rules and approval gates.

---

## 1. The Core Question: Will NSW Definitions Conflict with Legacy?

**Short Answer:** ✅ **No conflict** — controlled coexistence with a clean exit path.

**Why this works:**
- **Legacy reality:** Category/Subcategory/Item/Attribute semantics are inconsistent and overloaded (single endpoints returning mixed payloads, attributes piggybacked, fuzzy meanings).
- **NSW definition:** Category → structural grouping, Subcategory → optional refinement, Item (Product Type) → behavioral/type definition, Attribute → type-driven schema (not category-driven payload noise).
- **What Phase-4 achieves:** Legacy definitions are tolerated, not trusted. Legacy is consumed, not copied forward. New logic is not built on top of broken semantics.

**This is the exact correct industrial migration pattern.**

---

## 2. What Phase-4 Work Actually Does (Not Defining NSW Semantics)

Phase-4/S4 work is **not** defining NSW semantics. It is doing two practical things:

### 2.1 Stabilize the Current Running Product (Legacy/V2)

**Goals:**
- Make dropdown pipelines, reuse search, and apply flows stay predictable
- Reduce duplication of logic by moving shared behaviors behind SHARED services/contracts
- Improve testability and rollback confidence

**What this means:**
- All consumers (CIM, MBOM, FEED, PBOM) call the same SHARED `/api/*` endpoints
- One standardized interface instead of many `product.get*` / `masterbom.get*` paths
- Legacy remains functional and stable while NSW is built

### 2.2 Create Clean "Adapter Seams"

**Goals:**
- SHARED `/api/*` endpoints become the single standardized interface for catalog lookups inside the legacy system
- Later, NSW can implement its own canonical endpoints/contracts without breaking all consumers at once

**What this means:**
- Phase-4 standardizes the **transport layer** and **call paths**, not the final meaning
- NSW can later swap the lookup backend behind the SHARED contract if ever needed
- Clean separation allows parallel development and safe deprecation

### 2.3 Contract Naming Clarification (Critical)

**⚠️ IMPORTANT:** S4 "SHARED contracts" are **legacy transport contracts** (interface stability), **NOT NSW canonical contracts**.

**Explicit Naming Convention:**

| Contract Name | Layer | Purpose | Status |
|---|---|---|---|
| `CatalogLookupContract` (S4) | **Legacy Transport Contract** | Interface stability for legacy lookup consumption | ✅ Active in Phase-4 |
| `ReuseSearchContract` (S4) | **Legacy Transport Contract** | Interface stability for legacy reuse search | ✅ Active in Phase-4 |
| NSW Canonical Catalog Contract | **NSW Canonical Contract** | Clean canonical lookup for NSW | 📋 To be defined in Phase-5 |

**Rule:** 
- ❌ **FORBIDDEN:** Assuming "CatalogLookupContract = NSW canonical contract"
- ✅ **REQUIRED:** Treating S4 SHARED contracts as legacy transport contracts only
- ✅ **REQUIRED:** Defining NSW canonical contracts separately in Phase-5

**Why this matters:**
- Prevents teams from conflating legacy interface stability with NSW canonical semantics
- Ensures NSW canonical contracts are defined cleanly without legacy contamination
- Maintains clear separation between transport layer (Phase-4) and semantic layer (Phase-5)

---

## 3. How This Helps NSW Phase-5 (Even If Definitions Change)

Because Phase-4 reduces chaos, NSW Phase-5 will have:

### 3.1 Clean Contract/Adapter Boundary

**What NSW needs:** A standardized interface that all UI and modules call.

**What Phase-4 provides:** All legacy consumers already rely on one interface (`CatalogLookupContract`), instead of many scattered paths.

**Benefit:** When NSW defines its canonical contracts, the migration surface is clear and bounded.

### 3.2 Controlled Import/Master Creation Governance Firewall

**What NSW needs:** No runtime master auto-creation, approval queues, canonical resolver.

**What Phase-4 enforces:** No new masters auto-created during runtime dropdowns (only GET lookups). COMPAT endpoints remain only as fallback, not as the "truth".

**Benefit:** Phase-4 prevents legacy contamination from growing, making NSW firewall rules easier to enforce.

### 3.3 Safe Migration Strategy (Optional Later)

**What NSW needs:** A controlled path to map old → new with human approval + transformation rules.

**What Phase-4 provides:** All legacy consumers use standardized interfaces, so migration surface is predictable and testable.

**Benefit:** If migration is ever needed, the mapping surface is clear and bounded.

---

## 4. How We Prevent "Semantic Contamination" Today

In Phase-4 (S4), we enforce:

### 4.1 No New Masters Auto-Created During Runtime

**Rule:** Only GET lookups during dropdown selection. No POST auto-creates.

**Enforcement:** All SHARED endpoints are GET-only. COMPAT endpoints remain GET-only.

**Benefit:** Legacy data quality issues remain visible (good), but new logic is not built on top of broken semantics (critical).

### 4.2 COMPAT Endpoints Remain Only as Fallback

**Rule:** COMPAT endpoints (`product.get*`, `masterbom.get*`) remain alive but are not the "truth".

**Enforcement:** COMPAT endpoints serve as fallback for gaps (like attributes), not as the primary lookup path.

**Benefit:** Legacy pain is contained, not spread. New consumers use SHARED endpoints.

### 4.3 No Payload Meaning Changes During S4

**Rule:** Payload shapes remain stable. We're changing callers, not meaning.

**Enforcement:** All SHARED endpoints return stable payload shapes. No field additions/removals during S4.

**Benefit:** Legacy semantics remain frozen, preventing further drift while NSW is defined.

---

## 5. Simple Mental Model

### 5.1 Legacy Phase-4 (S4): "Make the Current System Stable and Modular"

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

### 5.2 NSW Phase-5: "Define the New Truth (Canonical Meaning + Schema) and Enforce It"

**What Phase-5 does:**
- Defines NSW canonical data dictionary
- Defines NSW canonical contracts (separate from legacy contracts)
- Establishes firewall governance (no legacy contamination)
- Builds NSW separately from legacy

**What Phase-5 does NOT do:**
- Migrate legacy masters into NSW
- Reuse legacy contracts
- Touch legacy flows

### 5.3 Later Migration (Optional): "Map Old → New With Human Approval + Transformation Rules"

**If migration is ever needed:**
- Map legacy → NSW through staging + approvals
- Never direct migration (per ADR-005)
- Separate project, not part of S4 or Phase-5

---

## 6. Practical Benefits of This Approach

### 6.1 Reduces Rework When NSW Semantics Change

**Problem:** If legacy consumers rely on many scattered lookup paths, changing NSW semantics would require updating all paths.

**Solution:** Phase-4 converges all consumers to one SHARED interface.

**Benefit:** When NSW defines new semantics, only the SHARED contract needs to be considered (or swapped behind the interface).

### 6.2 Enables Parallel Development

**Problem:** Legacy and NSW need to coexist during transition.

**Solution:** Phase-4 keeps legacy stable and modular. Phase-5 builds NSW separately.

**Benefit:** Legacy remains functional while NSW is built clean from scratch.

### 6.3 Supports "No Legacy Migration" Stance

**Decision:** Do not migrate legacy masters into NSW because they're contaminated (per ADR-005).

**Phase-4 Alignment:** S4 keeps legacy stable and prevents the mess from growing.

**Benefit:** Legacy remains functional while NSW is built clean from scratch.

---

## 7. Key Rules for Team

### 7.1 Phase-4 (S4) Rules

✅ **Allowed:**
- Standardize lookup consumption (move consumers to SHARED endpoints)
- Keep COMPAT endpoints alive as fallback
- Preserve payload shapes (no meaning changes)
- Improve testability and rollback confidence

❌ **Forbidden:**
- Redefine master semantics
- Create NSW canonical contracts
- Migrate legacy data
- Change what Category/Item/etc. mean in legacy

### 7.2 Phase-5 Rules

✅ **Allowed:**
- Define NSW canonical data dictionary
- Define NSW canonical contracts (separate from legacy)
- Establish firewall governance
- Build NSW separately from legacy

❌ **Forbidden:**
- Migrate legacy masters into NSW
- Reuse legacy contracts
- Touch legacy flows
- Assume legacy semantics = NSW semantics

### 7.3 Coexistence Rules

✅ **Allowed:**
- Legacy and NSW run in parallel
- Legacy remains functional during NSW development
- NSW builds clean from scratch

❌ **Forbidden:**
- Legacy contamination of NSW definitions
- NSW contamination of legacy flows
- Direct migration without staging + approvals

---

## 8. Authority References

**Phase-4 Governance:**
- `docs/PHASE_4/S4_GOV_001_PROPAGATION_ORDER.md` - S4 propagation order and rules
- `docs/PHASE_4/LEGACY_VS_NSW_SEMANTIC_BOUNDARY.md` - Semantic boundary definition
- `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` - Legacy SHARED contract alignment

**Phase-5 Governance:**
- `docs/PHASE_5/00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` - Firewall rules and no auto-create policy
- `docs/PHASE_5/00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md` - Full governance document
- `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md` - Phase-5 scope separation

**Related Documents:**
- `docs/PHASE_5/00_GOVERNANCE/STAKEHOLDER_BRIEF_WHY_NO_LEGACY_MIGRATION.md` - Migration decision rationale

---

## 9. Summary Statement

**Phase-4 (S4) standardizes the transport layer and call paths, not the final meaning.**

- Phase-4 makes legacy stable and modular (reduces drift, centralizes behavior)
- Phase-5 defines NSW canonical contracts separately (clean rebuild, firewall governance)
- Legacy and NSW are two different truth layers (explicit separation - see Section "Two Truth Layers Disclaimer")
- S4 SHARED contracts are legacy transport contracts, NOT NSW canonical contracts (see Section 2.3)
- No semantic equivalence may be assumed without explicit mapping documentation (separate project)
- No semantic contamination if this policy is respected

**This coexistence policy must be maintained throughout Phase-4 and Phase-5 work to prevent confusion and ensure clean separation.**

---

**Document Status:** ✅ **ACTIVE POLICY**  
**Last Updated:** 2025-12-24  
**Next Review:** After Phase-5 Step-1 completion (Data Dictionary freeze)  
**Owner:** Phase-4/Phase-5 Governance Team

