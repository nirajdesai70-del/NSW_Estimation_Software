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

## Pending Decisions

### D-005: IsLocked Scope
**Date:** TBD  
**Decision:** TBD - Which tables should have `is_locked` field?  
**Options:**
- Option A: Line-item only (`quote_bom_items`)
- Option B: All quotation levels (`quotations`, `quote_panels`, `quote_boms`, `quote_bom_items`)
**Status:** ⏳ PENDING

### D-006: CostHead Product Default
**Date:** TBD  
**Decision:** TBD - Should `products` table have `cost_head_id` for defaults?  
**Options:**
- Option A: Add `products.cost_head_id`
- Option B: CostHead only at line-item level
**Status:** ⏳ PENDING

### D-007: Multi-SKU Linkage Strategy
**Date:** TBD  
**Decision:** TBD - How to link multi-SKU explosion items?  
**Options:**
- Option A: `parent_line_id` only
- Option B: `metadata_json` only
- Option C: Both (recommended)
**Status:** ⏳ PENDING

---

## Change Log
- v1.0: Created decisions register with initial decisions

