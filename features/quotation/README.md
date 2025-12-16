---
title: "Quotation"
feature: "Quotation"
module: "Quotation"
status: "active"
source: "NEPL V2"
last_verified: "2025-12-17"
owners: ["Niraj", "DevTeam"]
---

# Quotation

**Sidebar Label:** Quotation  
**Purpose:** Core business module managing complete quotation lifecycle from creation to PDF generation.

## Baseline Status
- **Status:** ✅ Frozen
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 03–04
- **Total Files:** 14 (12 features + 2 changes)

## Sub-Modules (Areas)

1. `_general/` — **General Overview** (module overview, cross-cutting concepts)
2. `v2/` — **Quotation V2** (panel/feeder/BOM hierarchy, V2 implementation)
3. `discount_rules/` — **Discount Rules** (discount logic, V2 discount editor)
4. `costing/` — **Costing & Pricing** (pricing calculations, costing system)
5. `workflows/` — **Workflows** (creation, revision, panel workflow)
6. `reports/` — **Reports & Exports** (PDF generation, exports)
7. `legacy/` — **Legacy Quotation** (legacy references, read-only)

## Rules (Documentation Governance)

- Folder names are **system-safe slugs** (no spaces, stable).
- This is a **shadow structure** (documentation-only). It does not affect application routing.
- Files can be **copied** into these folders without deleting originals.
- V2 documentation takes priority over legacy.
- Change history (RCA, fixes, progress) goes to `changes/quotation/`.

## Cross-links
- Related feature areas: Component/Item Master, Master BOM, Feeder Library (to be linked later)
- Change history: `changes/quotation/v2/`, `changes/quotation/legacy/`

