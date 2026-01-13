# Phase-6 Cost Adders - Task Inserts for Execution Plan

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ✅ READY TO INSERT  
**Purpose:** Exact task inserts for Phase-6 Execution Plan (Track D0 and Track D)

---

## 📋 How to Use This Document

1. Open `PHASE_6_EXECUTION_PLAN.md`
2. Find the section indicated below
3. Insert the tasks in the exact location specified
4. Update task numbering if needed (these follow existing P6-XXX-XXX pattern)

---

## 🔧 Track D0 - Costing Engine Foundations (Weeks 3-6)

### Insert Location: After P6-COST-D0-003 (Week 3)

**Insert these tasks:**

```markdown
#### Week 3: Cost Heads Seeding (NEW)

- [ ] **P6-COST-D0-008:** Seed generic cost heads for cost adders
  - Seed cost heads in `cost_heads` table:
    - MATERIAL (already exists via BOM)
    - BUSBAR
    - FABRICATION
    - LABOUR
    - TRANSPORTATION
    - ERECTION
    - COMMISSIONING
    - MISC
  - Set CostBucket mapping (for summary roll-up lines):
    - BUSBAR → MATERIAL
    - FABRICATION → MATERIAL (summary line bucket; detail lines can be MATERIAL/LABOUR/OTHER)
    - LABOUR → LABOUR
    - TRANSPORTATION → OTHER
    - ERECTION → LABOUR
    - COMMISSIONING → OTHER
  - **Note:** Summary bucket comes from cost_heads.category; detail line buckets set in template lines
  - Tenant-scoped seed data
  - **File:** `docs/PHASE_6/COSTING/COST_HEADS_SEED.md`
  - **Dependency:** After cost_heads table exists (Track E, Week 0-1)
```

---

### Insert Location: After P6-COST-D0-004 (Week 4)

**Insert these tasks:**

```markdown
#### Week 4: Cost Template & Sheet Tables (NEW)

- [ ] **P6-COST-D0-009:** Create cost template master tables
  - `cost_templates` table (one per cost head)
  - `cost_template_lines` table (rows per template)
  - Migration script
  - Fields:
    - cost_templates: id, tenant_id, cost_head_id, name, version, is_active
    - cost_template_lines: id, cost_template_id, line_name, calc_mode, default_uom, default_rate, line_cost_bucket (MATERIAL/LABOUR/OTHER, nullable), sort_order
  - **Note:** `line_cost_bucket` allows each template line to have its own CostBucket (e.g., Fabrication sheet: steel=MATERIAL, coating=OTHER, manpower=LABOUR)
  - **File:** `docs/PHASE_6/COSTING/COST_TEMPLATE_SCHEMA.md`
  - **Dependency:** After cost heads seeded (P6-COST-D0-008)

- [ ] **P6-COST-D0-010:** Create cost sheet runtime tables
  - `quote_cost_sheets` table (one per panel per cost head)
  - `quote_cost_sheet_lines` table (instantiated template lines)
    - Include `line_cost_bucket` field (inherited from template, can override)
  - `quote_cost_adders` table (summary roll-up, one per panel per cost head)
    - Summary bucket comes from `cost_heads.category` (not aggregated from lines)
  - Migration script
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_SCHEMA.md`
  - **Dependency:** After template tables (P6-COST-D0-009)
```

---

### Insert Location: After P6-COST-D0-005 (Week 5)

**Insert these tasks:**

```markdown
#### Week 5: Cost Sheet Calculation & Roll-Up (NEW)

- [ ] **P6-COST-D0-011:** Implement cost sheet calculation engine
  - Row-level calculation:
    - LUMP_SUM: amount = rate
    - QTY_RATE: amount = qty × rate
    - KG_RATE: amount = qty × rate (qty in kg)
    - METER_RATE: amount = qty × rate (qty in meters)
    - HOUR_RATE: amount = qty × rate (qty in hours)
    - PERCENT_OF_BASE: amount = base_cost × (rate / 100) (Commissioning only)
  - Sheet total calculation: SUM(all line amounts)
  - Validation (no negative values, locked rows)
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_CALCULATION.md`
  - **Dependency:** After runtime tables (P6-COST-D0-010)

- [ ] **P6-COST-D0-012:** Implement cost adder roll-up generator
  - When cost sheet saved/approved:
    - Calculate sheet total: SUM(quote_cost_sheet_lines.amount)
    - Upsert row in quote_cost_adders:
      - quotation_id, quote_panel_id, cost_head_id
      - amount = sheet_total × PanelQty (per-panel multiplication)
      - status = sheet status
      - source_sheet_id = sheet.id
      - **Note:** Summary bucket comes from cost_heads.category (not aggregated from line buckets)
  - Auto-recalculate on sheet line changes
  - **File:** `docs/PHASE_6/COSTING/COST_ADDER_ROLLUP.md`
  - **Dependency:** After calculation engine (P6-COST-D0-011)

- [ ] **P6-COST-D0-013:** Implement QCA (Quote Cost Adders) dataset
  - QCA = canonical dataset from quote_cost_adders table
  - One row per panel per cost head (summary)
  - JSON export endpoint: `/quotation/{id}/export/cost-adders/json`
  - QCA schema definition
  - **Note:** QCD remains BOM-only (stable contract)
  - **File:** `docs/PHASE_6/COSTING/QCA_CONTRACT_v1.0.md`
  - **Dependency:** After roll-up generator (P6-COST-D0-012)
```

---

### Insert Location: After P6-COST-D0-006 (Week 6)

**Insert this task:**

```markdown
#### Week 6: Cost Adders Integration & Gate (NEW)

- [ ] **P6-COST-D0-014:** Update D0 Gate checklist to include cost adders
  - QCD generator functional (BOM-only, unchanged)
  - QCA generator functional (cost adders summary)
  - Cost sheet calculation engine working
  - Roll-up generator working
  - Performance acceptable with cost adders (< 5 seconds for typical quotation)
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md` (update)
  - **Gate:** Must pass before Track D (Costing & Reporting) can proceed
```

---

## 🎨 Track D - Costing & Reporting (Weeks 7-10)

### Insert Location: After P6-COST-004 (Week 7)

**Insert these tasks:**

```markdown
#### Week 7: Cost Adders UI Foundation (NEW)

- [ ] **P6-COST-019:** Add Cost Adders section to Panel Detail page
  - Display existing cost adders (one row per cost head):
    - FABRICATION (status, amount, "Edit" button)
    - BUSBAR (status, amount, "Edit" button)
    - LABOUR (status, amount, "Edit" button)
    - TRANSPORTATION (status, amount, "Edit" button)
    - ERECTION (status, amount, "Edit" button)
    - COMMISSIONING (status, amount, "Edit" button)
  - Status indicators: Draft/Approved/Locked badges
  - "Add Cost Adder" button (select cost head type)
  - Navigation to cost sheet editor
  - **File:** `docs/PHASE_6/UI/PANEL_COST_ADDERS_DESIGN.md`
  - **Dependency:** Track A Panel UI complete (Week 2)

- [ ] **P6-COST-020:** Implement cost sheet editor UI
  - Create route: `/quotation/{id}/panel/{panelId}/cost-sheet/{sheetId}`
  - Create view: `resources/views/quotation/v2/cost-sheet.blade.php`
  - Table view with editable rows:
    - Line name (read-only, from template)
    - Qty (editable)
    - UOM (read-only, from template)
    - Rate (editable)
    - Amount (auto-calculated, read-only)
  - Total at bottom (auto-calculated)
  - Buttons: Save, Approve, Lock
  - Status display (Draft/Approved/Locked)
  - **File:** `docs/PHASE_6/UI/COST_SHEET_EDITOR_DESIGN.md`
  - **Dependency:** After cost sheet calculation engine (P6-COST-D0-011)
```

---

### Insert Location: Update P6-COST-003 (Week 7)

**Replace existing task with:**

```markdown
- [ ] **P6-COST-003:** Implement quotation costing snapshot
  - Create route: `/quotation/{id}/costing/snapshot`
  - Create view: `resources/views/quotation/costing/snapshot.blade.php`
  - Display quotation-level costing summary:
    - Total BOM Cost (from QCD)
    - Total Cost Adders (from QCA)
    - Combined Total Cost
    - Margin calculation
    - Hit rate
  - **Data source: QCD aggregates + QCA aggregates**
```

---

### Insert Location: Update P6-COST-004 (Week 7)

**Replace existing task with:**

```markdown
- [ ] **P6-COST-004:** Implement panel summary view
  - Create route: `/quotation/{id}/costing/panels`
  - Create view: `resources/views/quotation/costing/panels.blade.php`
  - Display panel-level costing breakdown:
    - Panel BOM Cost (from QCD, filtered by panel)
    - Panel Cost Adders breakdown (by cost head, from QCA)
      - FABRICATION
      - BUSBAR
      - LABOUR
      - TRANSPORTATION
      - ERECTION
      - COMMISSIONING
    - Panel Total Cost = BOM + Adders
    - Panel cost per unit
  - **Data source: QCD aggregates + QCA aggregates**
```

---

### Insert Location: Update P6-COST-006 (Week 8)

**Replace existing task with:**

```markdown
- [ ] **P6-COST-006:** Implement CostHead grouping (now mandatory)
  - CostHead category display
  - CostHead-based cost aggregation:
    - MATERIAL (from QCD, drill by Make)
    - BUSBAR (from QCA, drill to sheet details)
    - FABRICATION (from QCA, drill to sheet details)
    - LABOUR (from QCA, drill to sheet details)
    - TRANSPORTATION (from QCA, drill to sheet details)
    - ERECTION (from QCA, drill to sheet details)
    - COMMISSIONING (from QCA, drill to sheet details)
  - CostBucket mappings (MATERIAL/LABOUR/OTHER)
  - CostHead pivot view
  - Integration with Phase-5 CostHead system
  - **Data source: QCD (BOM) + QCA (Adders)**
```

---

### Insert Location: Update P6-COST-007 (Week 8)

**Replace existing task with:**

```markdown
- [ ] **P6-COST-007:** Implement pivot tables
  - Panel × CostHead pivot (includes BOM + Adders)
  - Feeder × Component pivot (BOM only)
  - CostHead × Panel pivot (includes BOM + Adders)
  - **Must include CostHead pivot + Category/Make/RateSource**
  - Interactive pivot controls
  - Export pivot data
  - **Data source: QCD (BOM) + QCA (Adders)**
```

---

### Insert Location: Update P6-COST-015 (Week 10)

**Replace existing task with:**

```markdown
- [ ] **P6-COST-015:** Implement Costing Pack Excel export (engine-first)
  - Export should be engine-first
  - Sheet 1: Panel summary (BOM + Cost Adders totals)
  - Sheet 2: Detailed BOM (QCD - BOM items only)
  - Sheet 3: Cost Adders detail (QCA - summary lines, with drill-down to sheet lines)
  - Sheet 4: Pivot shells (optional)
  - Excel formatting (headers, formulas)
  - **Note:** Charts/graphs optional unless requested
  - **Data source: QCD (BOM) + QCA (Adders)**
```

---

## 🔧 Track E - Canon Implementation (Weeks 0-6)

### Insert Location: After P6-DB-004 (Week 1-2)

**Insert this task:**

```markdown
#### Week 1-2: Cost Template Seed Data (NEW)

- [ ] **P6-DB-005:** Seed cost template master data
  - Create minimal templates for each cost head:
    - FABRICATION template (3 lines):
      - Steel Sheet (QTY_RATE, CostBucket: MATERIAL)
      - Powder Coating/Jobwork (QTY_RATE, CostBucket: OTHER)
      - Fabrication Manpower (HOUR_RATE, CostBucket: LABOUR)
    - BUSBAR template (2 lines):
      - Copper busbar material (KG_RATE, CostBucket: MATERIAL)
      - Busbar fabrication (HOUR_RATE, CostBucket: LABOUR)
    - LABOUR template (3 lines):
      - Wiring labour (HOUR_RATE, CostBucket: LABOUR)
      - Assembly labour (HOUR_RATE, CostBucket: LABOUR)
      - Testing labour (HOUR_RATE, CostBucket: LABOUR)
    - TRANSPORTATION template (2 lines):
      - Transport (LUMP_SUM, CostBucket: OTHER)
      - Packing (LUMP_SUM, CostBucket: OTHER)
    - ERECTION template (1 line):
      - Site erection labour (HOUR_RATE, CostBucket: LABOUR)
    - COMMISSIONING template (1 line):
      - Commissioning (PERCENT_OF_BASE or LUMP_SUM, CostBucket: OTHER)
  - Set calc_mode and line_cost_bucket per line
  - Default qty/rate = blank (user enters)
  - Tenant-scoped seed data
  - **File:** `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`
  - **Dependency:** After cost_templates table created (P6-COST-D0-009)
```

---

## 📊 Track A - Panel UI (Weeks 1-6)

### Insert Location: Update P6-UI-004 (Week 2)

**Add to existing task:**

```markdown
- [ ] **P6-UI-004:** Implement panel details page
  - Create route: `/quotation/{id}/panel/{panelId}`
  - Create view: `resources/views/quotation/v2/panel.blade.php`
  - Display feeder list with hierarchy
  - **NEW:** Add Cost Adders section (placeholder, full implementation in Track D, Week 7)
    - Display section header
    - "Add Cost Adder" button (disabled until Track D)
  - **Note:** Full Cost Adders UI implemented in P6-COST-019 (Track D, Week 7)
```

---

## 📋 Summary of Changes

### New Tasks Added
- **Track D0:** 7 new tasks (P6-COST-D0-008 through P6-COST-D0-014)
- **Track D:** 2 new tasks (P6-COST-019, P6-COST-020)
- **Track E:** 1 new task (P6-DB-005)
- **Track A:** 1 task updated (P6-UI-004)

### Tasks Updated
- **Track D:** 4 tasks updated (P6-COST-003, P6-COST-004, P6-COST-006, P6-COST-007, P6-COST-015)

### Total Impact
- **New Tasks:** 10 tasks
- **Updated Tasks:** 5 tasks
- **Timeline Impact:** +1 week to Track D0 (Week 7 becomes part of D0), +1 week to Track D (Week 11 becomes part of D)

---

## ✅ Verification Checklist

Before inserting, verify:
- [ ] All task IDs follow existing P6-XXX-XXX pattern
- [ ] Dependencies are correctly identified
- [ ] File paths match existing documentation structure
- [ ] Week assignments align with track timelines
- [ ] No conflicts with existing task numbers

---

**Document Status:** ✅ READY FOR INSERTION  
**Last Updated:** 2025-01-27  
**Next Action:** Insert tasks into Phase-6 Execution Plan

