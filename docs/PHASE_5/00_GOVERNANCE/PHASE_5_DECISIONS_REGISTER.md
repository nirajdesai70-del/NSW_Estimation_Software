# Phase 5 Decisions Register

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
Record all architectural and design decisions made during Phase 5, including rationale and alternatives considered.

## Source of Truth
- **Canonical:** This is the authoritative decisions register

## Decision Format

Each decision follows this structure:
- **Decision ID:** D-XXX
- **Date:** YYYY-MM-DD
- **Decision:** Clear statement of what was decided
- **Rationale:** Why this decision was made
- **Alternatives Considered:** Other options evaluated
- **Impact:** What this affects
- **Status:** PENDING / APPROVED / SUPERSEDED

---

## Decisions

### D-001: Phase 5 Scope - Analysis Only
**Date:** 2025-12-18  
**Decision:** Phase 5 is limited to canonical data definition and schema design only. No implementation, no legacy migration.  
**Rationale:** Ensures clean canonical definitions without legacy constraints.  
**Alternatives Considered:** Include legacy migration in Phase 5 (rejected - too complex, different objectives)  
**Impact:** All Phase 5 work is documentation/design only  
**Status:** ✅ APPROVED

### D-002: Legacy Reference Policy
**Date:** 2025-12-18  
**Decision:** `project/nish/` is read-only reference. No code reuse, no schema copying.  
**Rationale:** Prevents contamination of canonical design with legacy patterns.  
**Alternatives Considered:** Reuse legacy code (rejected - would compromise canonical design)  
**Impact:** All legacy study must result in "what not to do" documentation  
**Status:** ✅ APPROVED

### D-003: Three-Truth Model
**Date:** 2025-01-27  
**Decision:** Establish three layers: Truth-A (Canonical), Truth-B (Legacy Reference), Truth-C (Implementation)  
**Rationale:** Clear separation prevents confusion and contamination  
**Alternatives Considered:** Single source (rejected - legacy and canonical must be separate)  
**Impact:** All documents must declare their truth layer  
**Status:** ✅ APPROVED

### D-004: Master Plan Alignment
**Date:** 2025-01-27  
**Decision:** Phase 5 (Data Dictionary + Schema) aligns with Master Plan P1 + P2. Master Plan P5 is post-implementation.  
**Rationale:** Clear positioning in overall project structure  
**Alternatives Considered:** Rename Phase 5 (rejected - too disruptive)  
**Impact:** Phase 5 scope remains analysis-only, implementation is post-Phase 5  
**Status:** ✅ APPROVED

### D-008: Exploration Mode Policy
**Date:** 2025-01-27  
**Decision:** Phase 5 operates in OPEN_GATE_EXPLORATION mode with controlled decision capture. Gates remain open to allow learning and discovery, but all changes must be logged in Decision Register or Feature Discovery Log.  
**Rationale:** For greenfield rebuild, early freezes would lock sub-optimal decisions and force rework. Exploration mode allows intentional discovery while maintaining auditability through decision capture.  
**Alternatives Considered:** 
- Option A: Close gates immediately (rejected - too early, locks assumptions before reality understood)
- Option B: No governance (rejected - loses traceability and auditability)
- Option C: Open gates with controlled capture (selected - balances flexibility with governance)
**Impact:** All Phase 5 governance, operating mode, decision capture process  
**Fundamentals Citation:** N/A (governance decision)  
**Alignment Status:** N/A  
**Status:** ✅ APPROVED

---

### D-005: IsLocked Scope
**Date:** 2025-01-27  
**Decision:** Locking applies at line-item level only (`quote_bom_items.is_locked`) for MVP. No locking at quotation, panel, or BOM levels in MVP.  
**Rationale:** Simplest implementation, sufficient for MVP deletion protection, can be extended later if needed. Aligns with MVP scope to keep initial implementation focused.  
**Alternatives Considered:** 
- Option A: Line-item only (selected - MVP scope)
- Option B: All quotation levels (rejected - too complex for MVP, can be added in future phases)
**Impact:** QUO module, `quote_bom_items` table, deletion protection logic  
**Fundamentals Citation:** 
- LOCKING_POLICY.md Section "MVP Scope: Line-Item Level Locking"
- MASTER_FUNDAMENTALS_v2.0.md (locking semantics for workflow control)
**Alignment Status:** ALIGNED  
**Schema Reference:** `04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` Section "quote_bom_items" table (line 700-754), field `is_locked` (line 718)  
**Schema Impact:** `quote_bom_items.is_locked` (BOOLEAN NOT NULL DEFAULT false) - only table with locking field  
**Status:** ✅ APPROVED

### D-006: CostHead Product Default
**Date:** 2025-01-27  
**Decision:** `products` table includes `cost_head_id` (nullable FK) to provide default CostHead for products. CostHead resolution uses precedence: line-item override → product default → system default.  
**Rationale:** Enables product-level CostHead defaults, reducing manual assignment at line-item level. Nullable field allows products without defaults to fall back to system default. Supports efficient CostHead resolution in costing engine.  
**Alternatives Considered:** 
- Option A: Add `products.cost_head_id` (selected - provides useful defaults)
- Option B: CostHead only at line-item level (rejected - requires manual assignment for every item)
**Impact:** CIM module, PRICING module, `products` table, CostHead resolution logic  
**Fundamentals Citation:** 
- COSTHEAD_RULES.md Section "CostHead Resolution Precedence" (line-item → product → system)
- MASTER_FUNDAMENTALS_v2.0.md (costing engine requirements)
**Alignment Status:** ALIGNED  
**Schema Reference:** `04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` Section "products" table (line 355-389), field `cost_head_id` (line 367, FK line 378, index line 389)  
**Schema Impact:** `products.cost_head_id` (BIGINT NULL, FK to `cost_heads.id`)  
**Status:** ✅ APPROVED

### D-007: Multi-SKU Linkage Strategy
**Date:** 2025-01-27  
**Decision:** Use both `parent_line_id` and `metadata_json` for multi-SKU explosion items. `parent_line_id` provides relational query capability, `metadata_json` provides flexible metadata storage.  
**Rationale:** Provides both structured query capability (via FK relationship) and flexible metadata storage for complex explosion scenarios. Supports efficient relational queries while allowing extensible metadata without schema changes.  
**Alternatives Considered:** 
- Option A: `parent_line_id` only (rejected - loses flexible metadata capability)
- Option B: `metadata_json` only (rejected - loses efficient relational query capability)
- Option C: Both (selected - best of both approaches)
**Impact:** QUO module, `quote_bom_items` table, multi-SKU explosion logic  
**Fundamentals Citation:** 
- MASTER_FUNDAMENTALS_v2.0.md (multi-SKU explosion requirements)
- FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md (if relevant gap items addressed)
**Alignment Status:** ALIGNED  
**Schema Reference:** `04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` Section "quote_bom_items" table (line 700-754), fields `parent_line_id` (line 706, FK line 730, index line 749) and `metadata_json` (line 722). See also design notes section (line 999-1014).  
**Schema Impact:** `quote_bom_items.parent_line_id` (BIGINT NULL, self-referencing FK), `quote_bom_items.metadata_json` (JSONB)  
**Status:** ✅ APPROVED

### D-009: Customer Normalization Strategy
**Date:** 2025-01-27  
**Decision:** Support both `customer_id` (nullable FK) and `customer_name_snapshot` (text field) in `quotations` table. `customer_id` provides structured reference for future customer master table integration, while `customer_name_snapshot` preserves historical customer name at quotation creation time.  
**Rationale:** Dual approach ensures both structured data and historical accuracy. `customer_id` enables future normalization without breaking historical quotations. `customer_name_snapshot` preserves exact customer name at quotation time, preventing historical data corruption if customer master data changes. Forward compatibility without forcing business standard decision on Day-1.  
**Alternatives Considered:** 
- Option A: `customer_id` only (rejected - loses historical accuracy, breaks if customer master changes)
- Option B: `customer_name_snapshot` only (rejected - loses structured reference capability)
- Option C: Both (selected - best of both approaches, staged normalization)
**Impact:** QUO module, `quotations` table, customer data model  
**Fundamentals Citation:** 
- MASTER_FUNDAMENTALS_v2.0.md (customer data requirements)
**Alignment Status:** ALIGNED  
**Schema Reference:** `04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` Section "quotations" table (lines 779-802), fields `customer_id` (line 784, FK line 792) and `customer_name_snapshot` (line 785). See also "customers" table (lines 754-768).  
**Schema Impact:** `quotations.customer_id` (BIGINT NULL, FK to `customers.id`), `quotations.customer_name_snapshot` (VARCHAR(255) NULL)  
**Status:** ✅ APPROVED

### D-P5-001: Source of Truth Priority
**Date:** 2026-01-04  
**Decision:** Establish priority order: MASTER_FUNDAMENTALS_v2.0.md = semantic truth (what things mean), Backend behavior = operational baseline (what system currently does), Rulebook/Markdown docs = validation/clarification, Excel/historical sheets = reference only. If backend contradicts Fundamentals, raise Decision Register entry and fix code (or explicitly carve out exception).  
**Rationale:** Preserves stabilization goal and prevents "silent reinterpretation." Ensures Fundamentals define semantics while backend provides regression baseline.  
**Alternatives Considered:** 
- Option A: Code is truth (rejected - creates un-auditable spec split)
- Option B: Fundamentals only (rejected - ignores operational reality)
- Option C: Priority order with conflict resolution (selected - balances both needs)
**Impact:** All Phase-5 specs, implementation alignment, regression testing strategy  
**Fundamentals Citation:** MASTER_FUNDAMENTALS_v2.0.md Section Z.1, Z.2 (Governance Freeze Statements)  
**Alignment Status:** ALIGNED  
**Governance Rule:** G-01 (Source of Truth Priority)  
**Status:** ✅ APPROVED

### D-P5-002: L1/L2 Semantics Correction
**Date:** 2026-01-04  
**Decision:** L1 = engineering intent layer (no price ownership), L2 = commercial SKU layer (price ownership at SKU/price table). Manual override is NOT L2 - it is quotation-context rate override tracked via RateSource + override fields.  
**Rationale:** Prevents semantic drift and confusion. Manual override is separate concept from L2 resolution. Ensures correct understanding of pricing ownership (L2 owns price, L1 does not).  
**Alternatives Considered:** 
- Option A: Override as L2 (rejected - breaks Fundamentals semantics)
- Option B: L1/L2 with override as separate concept (selected - correct semantics)
**Impact:** Data dictionary, schema design, code implementation, documentation  
**Fundamentals Citation:** MASTER_FUNDAMENTALS_v2.0.md Section U (Pricing Ownership), Section T (L1→L2 Explosion)  
**Alignment Status:** ALIGNED  
**Governance Rule:** G-02 (L1 vs L2 Semantics)  
**Status:** ✅ APPROVED

### D-P5-003: Manual Override Governance
**Date:** 2026-01-04  
**Decision:** Manual override rate is frozen during price refresh/recompute flows, but totals can recalculate using frozen override rate. System must store: RateSource=MANUAL, ManualOverrideReason (required), OverriddenAtStep, OverriddenBy, OverriddenAt, L1DerivedRate and L2SelectedRate snapshots. Role restriction: Reviewer/Approver only.  
**Rationale:** Balances requested behavior (recalc allowed but deviation flagged) with Fundamentals behavior (overrides not refreshed). Ensures overrides are explicit, audited, and permissioned.  
**Alternatives Considered:** 
- Option A: Override frozen completely (rejected - too restrictive)
- Option B: Override refreshed on price update (rejected - contradicts Fundamentals)
- Option C: Override frozen but totals recalc (selected - satisfies both requirements)
**Impact:** QUO module, pricing logic, override flows, audit logging  
**Fundamentals Citation:** MASTER_FUNDAMENTALS_v2.0.md Section M.4 Step 4 ("Manual overrides remain untouched"), Section Y.1 (Price Override in Quotations)  
**Alignment Status:** ALIGNED  
**Governance Rule:** G-03 (Manual Override Behavior)  
**Status:** ✅ APPROVED

### D-P5-004: Discount Levels Scope
**Date:** 2026-01-04  
**Decision:** Phase-5 supports Item-level and Quotation-level discounts only. BOM-level and Feeder-level discounts are NOT in Phase-5 scope. Record "BOM/Feeder discount pipeline" as Phase-6+ enhancement (or Phase-5 extension only if approved as change request).  
**Rationale:** Current schema/docs indicate only Item + Quotation levels exist. Adding BOM/Feeder discounts would require schema migration + UI updates + test coverage, expanding Phase-5 scope.  
**Alternatives Considered:** 
- Option A: Add BOM/Feeder discounts now (rejected - expands scope, not in current implementation)
- Option B: Item + Quote only, defer BOM/Feeder (selected - aligns with current implementation)
**Impact:** Discount logic, schema design, UI design, Phase-5 scope  
**Fundamentals Citation:** features/quotation/discount_rules/31_DISCOUNT_LOGIC.md, features/quotation/costing/20_PRICING_CALCULATION_FLOW.md  
**Alignment Status:** ALIGNED (with current implementation)  
**Governance Rule:** G-04 (Discount Order)  
**Status:** ✅ APPROVED

### D-P5-005: RAG Boundary
**Date:** 2026-01-04  
**Decision:** RAG is advisory only, cannot modify totals automatically, failure must not block estimation. RAG output must be tagged advice_only=true. Any "apply suggestion" action becomes explicit user action that triggers audit logs.  
**Rationale:** RAG is enhancement, not dependency. Estimation is core business function and must work independently. RAG suggestions require explicit user approval to ensure business control.  
**Alternatives Considered:** 
- Option A: RAG authoritative (rejected - loses business control)
- Option B: RAG advisory with explicit actions (selected - safe and controlled)
**Impact:** RAG integration, estimation flows, audit logging  
**Fundamentals Citation:** RAG_KB/RAG_RULEBOOK.md  
**Alignment Status:** N/A (New requirement, not in Fundamentals)  
**Governance Rule:** G-06 (RAG Boundary)  
**Status:** ✅ APPROVED

### D-P5-006: Regression & Migration Policy
**Date:** 2026-01-04  
**Decision:** Policy-1 adopted: Preserve old totals unless user explicitly "Recalculate with fixes." Existing saved quotations must recompute identically unless bug-fix explicitly declared. New quotations follow corrected rules. Bug-fix protocol: Every bug fix changing totals must have Bug ID/Decision ID, Before/After examples, Scope of impacted quotations, Migration policy.  
**Rationale:** Zero financial surprises, clean governance, better workflow. Ensures historical quotations don't suddenly change totals. Every change becomes intentional action with audit trail.  
**Alternatives Considered:** 
- Option A: Always recompute (rejected - causes financial surprises)
- Option B: Lock old quotes permanently (rejected - too restrictive)
- Option C: Policy-1 with explicit recalculation (selected - safe and controlled)
**Impact:** Regression testing, migration strategy, recalculation flows, audit logging  
**Fundamentals Citation:** N/A (New requirement, not in Fundamentals)  
**Alignment Status:** N/A  
**Governance Rule:** G-07 (Regression Baseline)  
**Status:** ✅ APPROVED

### D-P5-007: Tax Inclusion (Phase-5)
**Date:** 2026-01-04  
**Decision:** Taxes included in Phase-5 with safe design: post-discount, post-override, quote-level only. Percentage-based taxes (GST), multiple tax components (CGST/SGST/IGST as config). Tax rate snapshot at calculation time. Existing quotations: tax_amount=0 (no retroactive application). Explicitly excluded: item-specific tax rules, jurisdiction auto-detection, tax exemptions, reverse charge logic (Phase-6+).  
**Rationale:** Basic tax support needed for Phase-5 completeness, but scope-limited to prevent expansion. Quote-level only avoids complex item-level logic. Snapshot preserves calculation-time state. No retroactive application preserves regression baseline.  
**Alternatives Considered:** 
- Option A: No taxes in Phase-5 (rejected - incomplete for production)
- Option B: Full tax logic in Phase-5 (rejected - expands scope too much)
- Option C: Basic quote-level taxes only (selected - balanced approach)
**Impact:** Tax calculation logic, schema design, calculation pipeline  
**Fundamentals Citation:** N/A (New requirement, not in Fundamentals)  
**Alignment Status:** N/A  
**Governance Rule:** G-08 (Tax Handling Rule)  
**Status:** ✅ APPROVED

---

## Change Log
- **v1.0 (2025-01-27):** Created decisions register with initial decisions
- **v1.1 (2025-01-27):** Approved D-005, D-006, D-007 to match schema canon implementation
- **v1.2 (2025-01-27):** Added D-009 (Customer Normalization Strategy) - approved to match schema canon implementation
- **v1.3 (2026-01-04):** Added D-P5-001 through D-P5-007 (Phase-5 pricing/estimation logic decisions) - approved per Phase-5 Governance Rules v1.0

