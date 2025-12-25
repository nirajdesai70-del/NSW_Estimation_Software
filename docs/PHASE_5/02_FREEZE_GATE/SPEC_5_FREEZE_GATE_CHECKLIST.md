# SPEC-5 Freeze Gate Checklist - Pending Upgrades Compliance Matrix

**Date:** 2025-01-27  
**Status:** 📋 MANDATORY VERIFICATION BEFORE FREEZE  
**Purpose:** Verify SPEC-5 v1.0 compliance with Phase 5 requirements from `PHASE_5_PENDING_UPGRADES_INTEGRATION.md`

---

## 🎯 Freeze Gate Rule

**SPEC-5 v1.0 CANNOT be frozen until ALL items in this checklist are verified and documented.**

This checklist ensures no governance fields or business rules are missed, preventing rework during implementation.

---

## 📊 Compliance Matrix

| Required Component | SPEC-5 Status | Verification Location | Action Required | Status |
|-------------------|---------------|----------------------|-----------------|--------|
| **1. BOM Tracking Fields** | ⚠️ **VERIFY** | Schema DDL: `quote_boms` table | Check for fields below | ⏳ PENDING |
| 1.1 `origin_master_bom_id` | ⚠️ | `quote_boms` table | Verify FK to `master_boms.id` | ⏳ |
| 1.2 `origin_master_bom_version` | ⚠️ | `quote_boms` table | Verify varchar/timestamp field | ⏳ |
| 1.3 `instance_sequence_no` | ⚠️ | `quote_boms` table | Verify integer field, composite uniqueness | ⏳ |
| 1.4 `is_modified` | ⚠️ | `quote_boms` table | Verify boolean field, default false | ⏳ |
| 1.5 `modified_by` | ⚠️ | `quote_boms` table | Verify FK to `users.id` | ⏳ |
| 1.6 `modified_at` | ⚠️ | `quote_boms` table | Verify timestamp field | ⏳ |
| **2. IsLocked Fields** | ⚠️ **VERIFY** | Quotation tables | Verify coverage scope | ⏳ PENDING |
| 2.1 `quote_bom_items.is_locked` | ⚠️ | `quote_bom_items` table | Verify boolean field exists | ⏳ |
| 2.2 `quote_panels.is_locked` | ⚠️ | `quote_panels` table | **DECIDE:** Add or explicitly exclude | ⏳ |
| 2.3 `quote_boms.is_locked` | ⚠️ | `quote_boms` table | **DECIDE:** Add or explicitly exclude | ⏳ |
| 2.4 `quotations.is_locked` | ⚠️ | `quotations` table | **DECIDE:** Add or explicitly exclude | ⏳ |
| 2.5 Locking scope declaration | ❌ | Data Dictionary | **REQUIRED:** Document locking scope (line-item only or all levels) | ❌ |
| **3. CostHead System** | ⚠️ **VERIFY** | Schema DDL + Data Dictionary | Verify table + FKs + resolution rules | ⏳ PENDING |
| 3.1 `cost_heads` table | ⚠️ | Schema DDL | Verify table exists with: id, code, name, category, priority | ⏳ |
| 3.2 `quote_bom_items.cost_head_id` | ⚠️ | `quote_bom_items` table | Verify FK to `cost_heads.id` | ⏳ |
| 3.3 `products.cost_head_id` (optional) | ⚠️ | `products` table | **DECIDE:** Add for default CostHead or exclude | ⏳ |
| 3.4 CostHead resolution order | ❌ | Data Dictionary | **REQUIRED:** Document precedence (item override → product default → system default) | ❌ |
| **4. Validation Guardrails G1-G7** | ❌ **MISSING** | Data Dictionary + Schema notes | **REQUIRED:** Document all 7 guardrails explicitly | ❌ PENDING |
| 4.1 G1: Master BOM rejects ProductId | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| 4.2 G2: Production BOM requires ProductId | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| 4.3 G3: IsPriceMissing normalizes Amount | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| 4.4 G4: RateSource consistency | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| 4.5 G5: UNRESOLVED normalizes values | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| 4.6 G6: FIXED_NO_DISCOUNT forces Discount=0 | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| 4.7 G7: All discounts are percentage-based | ❌ | Data Dictionary rules | **REQUIRED:** Explicit business rule | ❌ |
| **5. AI Entities** | ✅ **COVERED** | Schema DDL | Verify tables exist | ✅ VERIFIED |
| 5.1 `ai_call_logs` table | ✅ | Schema DDL | Table exists with required fields | ✅ |
| 5.2 AI scope declaration | ⚠️ | Data Dictionary | **REQUIRED:** Label as Phase-5 schema reservation, Post-Phase-5 implementation | ⏳ |
| **6. Module Ownership Mapping** | ❌ **MISSING** | Data Dictionary | **REQUIRED:** Map every table to owner module | ❌ PENDING |
| 6.1 Auth module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (tenants, users, roles, etc.) | ❌ |
| 6.2 CIM module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (categories, products, etc.) | ❌ |
| 6.3 MBOM module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (master_boms, master_bom_items) | ❌ |
| 6.4 QUO module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (quotations, panels, boms, items) | ❌ |
| 6.5 PRICING module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (price_lists, prices) | ❌ |
| 6.6 AUDIT module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (audit_log, bom_change_logs) | ❌ |
| 6.7 AI module tables | ❌ | Module ownership matrix | **REQUIRED:** List tables (ai_call_logs, etc.) | ❌ |
| **7. Naming Conventions** | ❌ **MISSING** | Data Dictionary | **REQUIRED:** Document naming standards | ❌ PENDING |
| 7.1 Table naming | ❌ | Naming conventions | **REQUIRED:** Document standard (snake_case, plural, etc.) | ❌ |
| 7.2 Column naming | ❌ | Naming conventions | **REQUIRED:** Document standard | ❌ |
| 7.3 FK naming | ❌ | Naming conventions | **REQUIRED:** Document pattern (table_id, etc.) | ❌ |
| 7.4 Enum naming | ❌ | Naming conventions | **REQUIRED:** Document standard | ❌ |
| 7.5 Timestamp naming | ❌ | Naming conventions | **REQUIRED:** Document (created_at, updated_at, etc.) | ❌ |
| 7.6 ID strategy | ❌ | Naming conventions | **REQUIRED:** Document (bigserial vs UUID) | ❌ |
| 7.7 Tenant isolation convention | ❌ | Naming conventions | **REQUIRED:** Document (tenant_id everywhere) | ❌ |
| **8. Design Decisions** | ⚠️ **LOCK NEEDED** | Schema Design | Lock 3 critical decisions | ⏳ PENDING |
| 8.1 Multi-SKU linkage | ⚠️ | Schema DDL | **LOCK:** parent_line_id + metadata_json (both) | ⏳ |
| 8.2 Customer normalization | ⚠️ | Schema DDL | **LOCK:** customer_name (text) + customer_id (optional FK) | ⏳ |
| 8.3 Resolution level constraints | ⚠️ | Schema DDL + Data Dictionary | **LOCK:** L0/L1/L2 allowed everywhere with explicit rules | ⏳ |

---

## ✅ Verification Steps

### Step 1: Schema DDL Verification
- [ ] Open SPEC-5 schema DDL section
- [ ] For each item in compliance matrix, verify field/table exists
- [ ] Check data types, constraints, FKs are correct
- [ ] Mark status in compliance matrix

### Step 2: Data Dictionary Verification
- [ ] Open SPEC-5 Data Dictionary section (or create if missing)
- [ ] Verify business rules are documented
- [ ] Verify Validation Guardrails G1-G7 are explicitly listed
- [ ] Verify CostHead resolution order is documented
- [ ] Verify IsLocked scope is explicitly declared

### Step 3: Module Ownership & Naming
- [ ] Create Module Ownership Matrix (if missing)
- [ ] Create Naming Conventions section (if missing)
- [ ] Map all tables to owner modules
- [ ] Document all naming standards

### Step 4: Design Decision Lock
- [ ] Lock Multi-SKU linkage strategy (parent_line_id + metadata_json)
- [ ] Lock Customer normalization approach (customer_name + optional customer_id)
- [ ] Lock Resolution level constraints (L0/L1/L2 at all levels with rules)

### Step 5: Documentation Patch
- [ ] Add missing sections to SPEC-5
- [ ] Update compliance matrix with final status
- [ ] Mark all items as ✅ VERIFIED or document exceptions

---

## 🚦 Freeze Gate Criteria

**SPEC-5 v1.0 can be frozen ONLY when:**

1. ✅ All BOM tracking fields verified in schema
2. ✅ IsLocked scope explicitly declared (added fields or explicit exclusion)
3. ✅ CostHead system verified + resolution order documented
4. ✅ Validation Guardrails G1-G7 explicitly documented in Data Dictionary
5. ✅ AI scope explicitly declared (schema reservation vs implementation)
6. ✅ Module ownership matrix complete (all tables mapped)
7. ✅ Naming conventions documented (all standards written)
8. ✅ Three design decisions locked (Multi-SKU, Customer, Resolution levels)

---

## 📝 Action Items

### Immediate (Before Freeze)

1. [ ] **Verify schema DDL** against compliance matrix
2. [ ] **Document Validation Guardrails G1-G7** in Data Dictionary section
3. [ ] **Create Module Ownership Matrix** mapping all tables to modules
4. [ ] **Create Naming Conventions** section with all standards
5. [ ] **Declare IsLocked scope** (which tables have is_locked, or explicit exclusion)
6. [ ] **Document CostHead resolution order** (item → product → system default)
7. [ ] **Declare AI scope** (Phase-5 schema reservation, Post-Phase-5 implementation)
8. [ ] **Lock 3 design decisions** (Multi-SKU, Customer, Resolution levels)
9. [ ] **Update compliance matrix** with final verification status
10. [ ] **Get stakeholder approval** for freeze gate criteria

### Post-Freeze (Phase 5 Execution)

- [ ] Use compliance matrix as reference during Phase 5 Step 1 (Data Dictionary)
- [ ] Use compliance matrix as reference during Phase 5 Step 2 (Schema Design)
- [ ] Verify all items are covered in frozen deliverables

---

## 📌 Notes

### IsLocked Scope Decision

**Option A:** Add `is_locked` to all quotation tables (panels, boms, quotations)
- Pros: Full deletion protection at all levels
- Cons: More fields to manage

**Option B:** IsLocked only at line-item level (MVP)
- Pros: Simpler, sufficient for MVP
- Cons: May need to extend later

**Recommendation:** Document explicit decision in Data Dictionary, either:
- "IsLocked applies only at line-item level in MVP (quote_bom_items)"
- OR "IsLocked applies at all quotation levels (quotations, panels, boms, items)"

### CostHead Product Default

**Option A:** Add `products.cost_head_id` for default CostHead
- Pros: Product-level defaults, cleaner resolution
- Cons: Additional field

**Option B:** CostHead only at line-item level
- Pros: Simpler, explicit per item
- Cons: No product defaults

**Recommendation:** Document decision in Data Dictionary

---

**Last Updated:** 2025-01-27  
**Status:** ⏳ AWAITING VERIFICATION  
**Next Action:** Complete schema DDL verification and mark compliance matrix

