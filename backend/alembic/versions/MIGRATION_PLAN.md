# Phase-5 Schema Canon Migration Plan

**Date:** 2026-01-04  
**Status:** 📋 PLANNING  
**Source:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`

---

## Migration Order

1. **AUTH Module** - tenants, users, roles, user_roles, permissions, role_permissions
2. **CIM Module** - categories, subcategories, product_types, attributes, category_attributes, makes, series, products, product_attributes
3. **L1/L2 Module** - l1_line_groups, l1_intent_lines, l1_attributes, catalog_skus (update), l1_l2_mappings
4. **SHARED Module** - cost_heads
5. **CUSTOMER Module** - customers
6. **MBOM Module** - master_boms, master_bom_items
7. **QUO Module** - quotations, quote_panels, quote_boms, quote_bom_items, quote_bom_item_history
8. **PRICING Module** - price_lists, prices, sku_prices, import_batches, import_approval_queue
9. **AUDIT Module** - audit_logs, bom_change_logs
10. **AI Module** - ai_call_logs
11. **Additions** - sc_struct_jsonb to catalog_skus, accessory_compatibility table

---

## Existing Migrations

- `f43171814116_create_catalog_tables.py` - Has some catalog tables (needs review/update)
- `6fbca98f32b1_catalog_current_price_skuprice_audit_make_.py` - Updates to catalog_skus

---

## Migration Strategy

Since existing migrations have some catalog tables, we'll:
1. Create new migrations that build on existing ones
2. Update catalog_skus to match Schema Canon exactly
3. Add missing tables
4. Add sc_struct_jsonb and accessory_compatibility

---

**Status:** Ready for migration creation

