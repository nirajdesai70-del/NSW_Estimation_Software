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

---

## Change Log
- **v1.0 (2025-01-27):** Created decisions register with initial decisions
- **v1.1 (2025-01-27):** Approved D-005, D-006, D-007 to match schema canon implementation

