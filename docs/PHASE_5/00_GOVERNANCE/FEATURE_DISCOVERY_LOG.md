# Feature Discovery Log

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose

Track new ideas, features, and improvements discovered during Phase 5 exploration. This log captures "better working" options without blocking progress.

## Entry Format

Each entry follows this structure:

| Field | Description | Required |
|-------|-------------|----------|
| **FD-ID** | Feature Discovery ID (FD-###) | Yes |
| **Date** | Discovery date (YYYY-MM-DD) | Yes |
| **Title** | Short descriptive title | Yes |
| **Idea** | Detailed description of the idea | Yes |
| **Why Better** | Rationale for why this is better than current/legacy | Yes |
| **Source** | Origin: user/legacy/fundamentals/features | Yes |
| **Impact Scope** | Modules/tables affected: AUTH/CIM/MBOM/QUO/PRICING/AUDIT/AI | Yes |
| **Schema Impact** | Specific tables/fields that would change | Yes |
| **Benefit** | Expected benefit or value | Yes |
| **Risk** | Potential risks or concerns | Yes |
| **Decision Needed?** | Y/N - does this require a decision? | Yes |
| **Status** | NEW/SHORTLIST/ACCEPT/REJECT/DEFERRED | Yes |
| **Linked Decision ID** | Decision Register ID if decisioned | No |
| **Notes** | Additional context or follow-up | No |

---

## Feature Discovery Entries

### FD-001: Enhanced Import Governance with Deduplication
**Date:** 2025-01-27  
**Title:** Import Governance Improvements  
**Idea:** Add approval workflow and deduplication logic to master data import process. Include import audit trail and validation gates.  
**Why Better:** Prevents duplicate entries, ensures data quality, provides traceability for imported data.  
**Source:** fundamentals  
**Impact Scope:** CIM/PRICING/AUDIT  
**Schema Impact:** 
- New table: `import_batches` (id, tenant_id, source, status, approved_by, approved_at, imported_at)
- New table: `import_audit_logs` (id, import_batch_id, record_type, record_id, action, details)
- Enhancement: Add `import_batch_id` to `products`, `price_lists`, `prices` tables
**Benefit:** Better data quality, auditability, prevents duplicate imports  
**Risk:** Adds complexity to import process, may slow down imports  
**Decision Needed?** Y  
**Status:** NEW  
**Linked Decision ID:** (pending)  
**Notes:** Aligns with Fundamentals v2.0 import expectations

---

### FD-002: Pricing Effective Dating Enhancement
**Date:** 2025-01-27  
**Title:** Pricing Effective Dating with Source Tracking  
**Idea:** Enhance pricing tables with effective dating (valid_from, valid_to) and explicit source tracking (source_type, source_reference).  
**Why Better:** Supports price versioning, historical price queries, and traceability to source price lists.  
**Source:** fundamentals  
**Impact Scope:** PRICING  
**Schema Impact:**
- Enhancement: Add `valid_from`, `valid_to` to `prices` table
- Enhancement: Add `source_type` (enum: MANUAL/OEM_IMPORT/ESTIMATED), `source_reference` (text) to `prices` table
**Benefit:** Historical price tracking, better auditability, supports price versioning rules  
**Risk:** Requires query logic changes, may impact performance  
**Decision Needed?** Y  
**Status:** NEW  
**Linked Decision ID:** (pending)  
**Notes:** Aligns with Fundamentals v2.0 pricing rules (insert new rows, never overwrite)

---

### FD-003: Multi-SKU Linkage Enhancement
**Date:** 2025-01-27  
**Title:** Enhanced Multi-SKU Explosion Tracking  
**Idea:** Use both `parent_line_id` and `metadata_json` for multi-SKU explosion items to support both relational queries and flexible metadata.  
**Why Better:** Provides both structured query capability and flexible metadata storage for complex explosion scenarios.  
**Source:** fundamentals  
**Impact Scope:** QUO  
**Schema Impact:**
- Enhancement: Ensure `quote_bom_items.parent_line_id` exists and is properly indexed
- Enhancement: Ensure `quote_bom_items.metadata_json` supports multi-SKU explosion data structure
**Benefit:** Better query performance, flexible metadata, supports complex explosion scenarios  
**Risk:** Requires careful design of metadata structure, potential for inconsistent data  
**Decision Needed?** Y  
**Status:** SHORTLIST  
**Linked Decision ID:** (pending - see D-007 in Decisions Register)  
**Notes:** This is a pending decision in Decisions Register, needs to be locked

---

### FD-004: Enhanced Audit/Logging Structure
**Date:** 2025-01-27  
**Title:** Comprehensive Audit Trail Enhancement  
**Idea:** Expand audit logging to cover all critical operations: BOM changes, price changes, import operations, user actions. Include before/after snapshots for key changes.  
**Why Better:** Provides complete auditability, supports compliance, enables troubleshooting and historical analysis.  
**Source:** fundamentals  
**Impact Scope:** AUDIT (all modules)  
**Schema Impact:**
- Enhancement: Expand `audit_logs` table with more granular event types
- New table: `bom_change_snapshots` (id, bom_id, snapshot_type, before_json, after_json, changed_by, changed_at)
- Enhancement: Add audit triggers or application-level logging for all write operations
**Benefit:** Complete audit trail, compliance support, troubleshooting capability  
**Risk:** Storage growth, performance impact on write operations  
**Decision Needed?** Y  
**Status:** NEW  
**Linked Decision ID:** (pending)  
**Notes:** Aligns with Fundamentals v2.0 audit trail requirements

---

### FD-005: L0/L1/L2 Clarity Improvements
**Date:** 2025-01-27  
**Title:** Resolution Level Clarity Enhancements  
**Idea:** Add explicit resolution level tracking and validation rules to ensure L0/L1/L2 semantics are clear and enforced. Include resolution level in audit logs.  
**Why Better:** Ensures correct resolution level semantics, prevents confusion, supports validation.  
**Source:** fundamentals  
**Impact Scope:** CIM/MBOM/QUO  
**Schema Impact:**
- Enhancement: Add `resolution_level` enum field to relevant tables (already exists, verify clarity)
- Enhancement: Add validation constraints to ensure resolution level consistency
- Enhancement: Add resolution level to audit logs
**Benefit:** Clearer semantics, better validation, prevents errors  
**Risk:** May require data migration if existing data doesn't match  
**Decision Needed?** Y  
**Status:** NEW  
**Linked Decision ID:** (pending)  
**Notes:** Aligns with Fundamentals v2.0 L0/L1/L2 definitions

---

## Status Definitions

- **NEW:** Recently discovered, not yet evaluated
- **SHORTLIST:** Under active consideration, being evaluated
- **ACCEPT:** Approved for inclusion (decision made, implementation planned)
- **REJECT:** Evaluated and rejected (rationale documented)
- **DEFERRED:** Accepted but deferred to post-freeze or post-implementation

---

## Change Log

- **v1.0 (2025-01-27):** Initial feature discovery log created with sample entries

---

**END OF FEATURE DISCOVERY LOG**

