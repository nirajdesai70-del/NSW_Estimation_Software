# Legacy Gaps & Anti-Patterns

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** REFERENCE  
**Owner:** Phase 5 Senate  

## Purpose
Document legacy system gaps and anti-patterns to ensure canonical design avoids them.

## Source of Truth
- **Reference:** This is read-only reference material (Truth-B)
- **Purpose:** "What not to do" guide for canonical design

## Anti-Patterns

### AP-001: BOM Linking (Reference-Based)
**Legacy Behavior:** May link BOMs directly  
**Problem:** Breaks independence, causes cascading changes  
**Canonical Decision:** Always copy, never link (see Decision D-002)

### AP-002: Auto-Create Masters
**Legacy Behavior:** May auto-create product masters during import  
**Problem:** Data quality issues, governance bypass  
**Canonical Decision:** No auto-create, approval queue required (see ADR-005)

### AP-003: Resolution Level Mixing
**Legacy Behavior:** May mix resolution levels inconsistently  
**Problem:** Unclear semantics, pricing errors  
**Canonical Decision:** Explicit L0/L1/L2 support with clear rules

## Gaps

### GAP-001: Missing BOM Tracking
**Legacy Gap:** May not track BOM origin and modifications  
**Canonical Solution:** Full tracking (origin_master_bom_id, instance_sequence_no, is_modified, etc.)

### GAP-002: Missing CostHead System
**Legacy Gap:** May not have structured CostHead system  
**Canonical Solution:** Full CostHead system with tables, FKs, resolution order

## Change Log
- v1.0: Created legacy gaps & anti-patterns template

