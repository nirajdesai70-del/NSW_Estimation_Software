# Phase-6 Cost Adders - Final Specification (Locked)

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ✅ LOCKED - READY FOR IMPLEMENTATION  
**Purpose:** Final locked specification for Cost Adders feature integration

---

## ✅ Corrections Applied

### 1. Cost Heads (Not Cost Categories)
- ✅ Use existing `cost_heads` table (already in Schema Canon)
- ✅ Seed generic cost heads: MATERIAL, BUSBAR, FABRICATION, LABOUR, TRANSPORTATION, ERECTION, COMMISSIONING, MISC
- ✅ No separate "cost categories" master table

### 2. QCD Contract Stability
- ✅ Keep QCD as BOM-only canonical dataset (stable contract)
- ✅ Create separate QCA (Quote Cost Adders) dataset for cost adder summary lines
- ✅ Costing Pack aggregates consume: QCD + QCA together
- ✅ No unioning into QCD contract (prevents breaking changes)

---

## 🔒 Locked Decisions

### Calc Modes
- ✅ LUMP_SUM
- ✅ QTY_RATE
- ✅ KG_RATE
- ✅ METER_RATE
- ✅ HOUR_RATE
- ✅ PERCENT_OF_BASE (optional, Commissioning template only in Phase-6)

### Default Values
- ✅ Template lines: qty/rate = blank by default (user enters)
- ✅ Optional defaults for "standard rates" deferred to Phase-7

### Approval Workflow
- ✅ Phase-6: Simple status field (DRAFT → APPROVED → LOCKED)
- ✅ Manual "Approve" button (no approval queue)
- ✅ Full approval workflow deferred to Phase-7

### Panel Qty Multiplication
- ✅ Cost sheet lines treated as per-panel unit by default
- ✅ Auto-compute total: PanelQty × per-panel cost sheet total
- ✅ Matches estimation scaling behavior

### Summary Line Behavior
- ✅ **Option 1 CONFIRMED:** One summary line per cost head (Fabrication, Busbar, Labour, etc.)
- ✅ Details stay inside cost sheet (not shown as multiple lines in quotation costing)
- ✅ Consistent behavior across all cost adders

---

## 📋 CostBucket Mapping (Two-Layer Approach)

### Layer 1: Summary Level (Quotation/Panel View)
**Uses:** `cost_heads.category` (default bucket for summary roll-up line)

| Cost Head | Summary CostBucket | Rationale |
|-----------|-------------------|-----------|
| MATERIAL | MATERIAL | BOM materials |
| BUSBAR | MATERIAL | Copper/aluminium material |
| FABRICATION | MATERIAL | Fabrication summary treated as material (dominant portion) |
| LABOUR | LABOUR | Direct labour costs |
| TRANSPORTATION | OTHER | Logistics/transport |
| ERECTION | LABOUR | Site erection is labour |
| COMMISSIONING | OTHER | Testing/commissioning services |
| MISC | OTHER | Miscellaneous costs |

**Behavior:** Single summary line in quotation/panel costing uses this bucket.

### Layer 2: Detail Level (Inside Cost Sheet)
**Uses:** `line_cost_bucket` field in `cost_template_lines` and `quote_cost_sheet_lines`

Each template line can have its own CostBucket:
- **FABRICATION sheet example:**
  - Steel Sheet → MATERIAL
  - Powder Coating (Jobwork) → OTHER
  - Fabrication Manpower → LABOUR
- **BUSBAR sheet example:**
  - Copper busbar material → MATERIAL
  - Busbar fabrication labour → LABOUR

**Behavior:** Detailed lines inside sheets carry their own buckets for accurate internal costing analysis.

**Roll-Up Logic:**
- Summary line bucket = `cost_heads.category` (from cost head default)
- Detail line buckets = `line_cost_bucket` (per line, for drill-down analysis)

---

## 📋 Minimal Template Lines (Phase-6 v1)

### FABRICATION Template
1. **Steel Sheet** (QTY_RATE, CostBucket: MATERIAL) - ~60% of total
2. **Powder Coating (Jobwork)** (QTY_RATE or LUMP_SUM, CostBucket: OTHER) - ~25% of total
3. **Fabrication Manpower** (HOUR_RATE, CostBucket: LABOUR) - ~15% of total

**Note:** Summary line shows as MATERIAL (from cost_heads.category), but internal breakdown captures the real split.

### BUSBAR Template
1. **Copper busbar material** (KG_RATE)
2. **Busbar fabrication** (HOUR_RATE or QTY_RATE)

### LABOUR Template
1. **Wiring labour** (HOUR_RATE)
2. **Assembly labour** (HOUR_RATE)
3. **Testing labour** (HOUR_RATE)

### TRANSPORTATION Template
1. **Transport** (LUMP_SUM or QTY_RATE)
2. **Packing** (LUMP_SUM)

### ERECTION Template
1. **Site erection labour** (HOUR_RATE or LUMP_SUM)

### COMMISSIONING Template
1. **Commissioning** (PERCENT_OF_BASE or LUMP_SUM)

**Note:** These are minimal Phase-6 templates. Can be expanded in Phase-7 based on usage.

---

## 🏗️ Data Model (Final)

### Master Tables
- `cost_heads` (existing, seed new heads)
  - `category` field = default CostBucket for summary roll-up
- `cost_templates` (one per cost head)
- `cost_template_lines` (rows per template)
  - `line_cost_bucket` field = CostBucket per line (MATERIAL/LABOUR/OTHER, nullable)

### Runtime Tables
- `quote_cost_sheets` (one per panel per cost head)
- `quote_cost_sheet_lines` (detailed rows inside sheet)
  - `line_cost_bucket` field = CostBucket per line (inherited from template, can override)
- `quote_cost_adders` (NEW - summary roll-up, one per panel per cost head)
  - Uses `cost_heads.category` for summary bucket (not aggregated from lines)

### quote_cost_adders Table Structure

```sql
CREATE TABLE quote_cost_adders (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quotation_id BIGINT NOT NULL,
    quote_panel_id BIGINT NOT NULL,
    cost_head_id BIGINT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'APPROVED', 'LOCKED')),
    source_sheet_id BIGINT NULL,  -- FK to quote_cost_sheets
    created_by BIGINT NULL,
    approved_by BIGINT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE,
    FOREIGN KEY (quote_panel_id) REFERENCES quote_panels(id) ON DELETE CASCADE,
    FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id) ON DELETE RESTRICT,
    FOREIGN KEY (source_sheet_id) REFERENCES quote_cost_sheets(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (quotation_id, quote_panel_id, cost_head_id)
);

CREATE INDEX idx_quote_cost_adders_tenant_id ON quote_cost_adders(tenant_id);
CREATE INDEX idx_quote_cost_adders_quotation_id ON quote_cost_adders(quotation_id);
CREATE INDEX idx_quote_cost_adders_panel_id ON quote_cost_adders(quote_panel_id);
CREATE INDEX idx_quote_cost_adders_cost_head_id ON quote_cost_adders(cost_head_id);
CREATE INDEX idx_quote_cost_adders_status ON quote_cost_adders(status);
```

**Key Behavior:**
- One row per panel per cost head (summary)
- Amount = SUM(all lines in source_sheet)
- Auto-upserted when sheet saved/approved
- Used by Costing Pack for fast aggregation

---

## 🔄 Costing Aggregation Model

### Layer 1: Canonical Datasets
- **QCD (QuotationCostDetail):** BOM-only, stable contract
- **QCA (Quote Cost Adders):** Summary lines from `quote_cost_adders` table

### Layer 2: Costing Pack Aggregation
- Panel Total Cost = QCD_BOM_total + QCA_total
- CostHead Pivot = QCD_BOM (by CostHead) + QCA (by CostHead)
- Dashboard = Aggregate QCD + QCA across quotations

### Layer 3: Drill-Down
- Click Fabrication line → Open Fabrication sheet (detailed lines with bucket split)
  - Shows: Material portion, Labour portion, Other portion
- Click Busbar line → Open Busbar sheet (detailed lines)
- MATERIAL by Make → QCD_BOM filtered by CostHead=MATERIAL, grouped by Make
- **Optional:** CostBucket drill-down within Fabrication (Material vs Labour vs Other)

---

## ✅ Phase-5 Compliance

- ✅ No schema meaning changes (additive tables only)
- ✅ QCD contract remains stable (v1.0)
- ✅ No guardrail changes
- ✅ No API contract violations
- ✅ Fully compliant with Phase-6 rule

---

**Document Status:** ✅ LOCKED  
**Next Action:** Generate Phase-6 Execution Plan task inserts  
**Owner:** Product + Engineering  
**Last Updated:** 2025-01-27

