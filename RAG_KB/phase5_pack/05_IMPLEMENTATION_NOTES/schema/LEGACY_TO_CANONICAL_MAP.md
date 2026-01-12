---
Source: docs/PHASE_5/05_TRACEABILITY/LEGACY_TO_CANONICAL_MAP.md
KB_Namespace: phase5_docs
Status: CANONICAL
Last_Updated: 2025-12-25T17:46:11.059491
KB_Path: phase5_pack/05_IMPLEMENTATION_NOTES/schema/LEGACY_TO_CANONICAL_MAP.md
---

# Legacy to Canonical Mapping

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT  
**Owner:** Phase 5 Senate  

## Purpose
Map legacy system features/behaviors to canonical decisions, documenting what we will NOT reuse and why.

## Source of Truth
- **Reference:** This is a reference document (not canonical truth)
- **Purpose:** Document legacy analysis outcomes

## Mapping Format

Each mapping follows this structure:
- **Legacy Feature/Behavior:** What exists in legacy
- **Risk/Problem:** Why it's problematic
- **Canonical Decision:** What we will do instead
- **Canonical Reference:** Where this is documented

---

## Mappings

### L2C-001: Legacy BOM Linking
**Legacy Feature/Behavior:** Legacy system may link BOMs directly (reference-based)  
**Risk/Problem:** Breaks independence, causes cascading changes, violates copy-never-link rule  
**Canonical Decision:** Always copy, never link. Quote BOMs are independent instances.  
**Canonical Reference:** Data Dictionary: BOM Copy semantics, Decision D-002

### L2C-002: Legacy Auto-Create Masters
**Legacy Feature/Behavior:** Legacy may auto-create product masters during import  
**Risk/Problem:** Data quality issues, governance bypass, inconsistent masters  
**Canonical Decision:** No auto-create. All masters go through approval queue.  
**Canonical Reference:** Data Dictionary: Master data governance, ADR-005

### L2C-003: Legacy Resolution Level Mixing
**Legacy Feature/Behavior:** Legacy may mix resolution levels inconsistently  
**Risk/Problem:** Unclear semantics, pricing errors, validation gaps  
**Canonical Decision:** Explicit L0/L1/L2 support with clear rules at all levels  
**Canonical Reference:** Data Dictionary: Resolution levels, Schema: Constraints

### L2C-004: Legacy Missing BOM Tracking
**Legacy Feature/Behavior:** Legacy may not track BOM origin and modifications  
**Risk/Problem:** No audit trail, can't trace changes, governance gaps  
**Canonical Decision:** Full tracking: origin_master_bom_id, instance_sequence_no, is_modified, modified_by, modified_at  
**Canonical Reference:** Data Dictionary: BOM tracking, Schema: quote_boms table

### L2C-005: Legacy Missing CostHead System
**Legacy Feature/Behavior:** Legacy may not have structured CostHead system  
**Risk/Problem:** Costing engine can't categorize costs properly  
**Canonical Decision:** Full CostHead system with tables, FKs, and resolution order  
**Canonical Reference:** Data Dictionary: CostHead entity, Schema: cost_heads table

---

## Change Log
- v1.0: Created legacy-to-canonical mapping template

