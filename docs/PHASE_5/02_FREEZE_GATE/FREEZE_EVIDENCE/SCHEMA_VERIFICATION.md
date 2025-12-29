# Schema Verification Evidence

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT  
**Owner:** Phase 5 Senate  

## Purpose
Document verification evidence for schema compliance with Phase 5 requirements.

## Source of Truth
- **Evidence:** This is verification evidence (not canonical schema)

## Verification Checklist

### BOM Tracking Fields
- [ ] `quote_boms.origin_master_bom_id` - FK to `master_boms.id` ✅ / ❌
- [ ] `quote_boms.origin_master_bom_version` - varchar/timestamp ✅ / ❌
- [ ] `quote_boms.instance_sequence_no` - integer, composite uniqueness ✅ / ❌
- [ ] `quote_boms.is_modified` - boolean, default false ✅ / ❌
- [ ] `quote_boms.modified_by` - FK to `users.id` ✅ / ❌
- [ ] `quote_boms.modified_at` - timestamp ✅ / ❌

### IsLocked Fields
- [ ] `quote_bom_items.is_locked` - boolean ✅ / ❌
- [ ] `quote_panels.is_locked` - boolean (if included) ✅ / ❌ / N/A
- [ ] `quote_boms.is_locked` - boolean (if included) ✅ / ❌ / N/A
- [ ] `quotations.is_locked` - boolean (if included) ✅ / ❌ / N/A
- [ ] Locking scope explicitly declared in Data Dictionary ✅ / ❌

### CostHead System
- [ ] `cost_heads` table exists with: id, code, name, category, priority ✅ / ❌
- [ ] `quote_bom_items.cost_head_id` - FK to `cost_heads.id` ✅ / ❌
- [ ] `products.cost_head_id` - FK to `cost_heads.id` (if included) ✅ / ❌ / N/A
- [ ] CostHead resolution order documented in Data Dictionary ✅ / ❌

### Validation Guardrails
- [ ] G1: Master BOM rejects ProductId - constraint/rule documented ✅ / ❌
- [ ] G2: Production BOM requires ProductId - constraint/rule documented ✅ / ❌
- [ ] G3: IsPriceMissing normalizes Amount - rule documented ✅ / ❌
- [ ] G4: RateSource consistency - rule documented ✅ / ❌
- [ ] G5: UNRESOLVED normalizes values - rule documented ✅ / ❌
- [ ] G6: FIXED_NO_DISCOUNT forces Discount=0 - rule documented ✅ / ❌
- [ ] G7: All discounts are percentage-based - rule documented ✅ / ❌

### AI Entities
- [ ] `ai_call_logs` table exists with required fields ✅ / ❌
- [ ] AI scope declared (Phase-5 schema reservation, Post-Phase-5 implementation) ✅ / ❌

### Module Ownership
- [ ] All tables mapped to owner modules ✅ / ❌
- [ ] Module Ownership Matrix complete ✅ / ❌

### Naming Conventions
- [ ] Table naming standard documented ✅ / ❌
- [ ] Column naming standard documented ✅ / ❌
- [ ] FK naming pattern documented ✅ / ❌
- [ ] Enum naming standard documented ✅ / ❌
- [ ] Timestamp naming documented ✅ / ❌
- [ ] ID strategy documented ✅ / ❌
- [ ] Tenant isolation convention documented ✅ / ❌

## Verification Notes

_Add verification notes here as schema is reviewed..._

## Change Log
- v1.0: Created schema verification template

