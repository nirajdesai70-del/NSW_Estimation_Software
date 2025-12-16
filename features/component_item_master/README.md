---
title: "Component / Item Master"
feature: "Component / Item Master"
module: "Catalog"
status: "active"
source: "NEPL V2"
last_verified: "2025-12-17"
owners: ["Niraj", "DevTeam"]
---

# Component / Item Master

**Sidebar Label:** Component / Item Master  
**Purpose:** Manage the complete catalog foundation: classification, attributes, makes/series, generic/specific products, pricing, imports, and catalog health.

## Baseline Status
- **Status:** ✅ Frozen
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 01–02
- **Primary Cross-Tab Reference:** `_general/08_PRODUCT_MODULE.md`

## Sub-Modules (Sidebar Tabs)

1. `category/` — **Category**
2. `subcategory/` — **Sub Category**
3. `product_type/` — **Type / Product Type**
4. `attributes/` — **Attributes**
5. `make/` — **Make**
6. `series/` — **Series**
7. `generic_product/` — **Generic Product**
8. `specific_product/` — **Specific Product**
9. `price_list/` — **Price List**
10. `import_export/` — **Import / Export**
11. `catalog_health/` — **Catalog Health**
12. `catalog_cleanup/` — **Catalog Cleanup**

## Rules (Documentation Governance)

- Folder names are **system-safe slugs** (no spaces, stable).
- UI tab labels are recorded inside each tab `README.md`.
- This is a **shadow structure** (documentation-only). It does not affect application routing.
- Files can be **copied** into these folders without deleting originals.

## Cross-links
- Related feature areas: Quotation, Master BOM, Feeder Library (to be linked later)
- Change history for catalog fixes: `changes/component_item_master/catalog_health/`
