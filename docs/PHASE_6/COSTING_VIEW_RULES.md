# Phase-6 Costing View Rules (Week-0 Lock)

**Status:** WEEK-0 LOCK (Rules only, no UI implementation)
**Scope:** Commercial quotation display vs internal cost sheets
**Canon:** Phase-5 Schema Canon v1.0 + Phase-6 Cost Adders model

---

## 1) Datasets

### QCD (BOM-only)
- Source: `quote_boms`, `quote_bom_items`
- Meaning: Material line items only (including priced components) + pricing metadata
- QCD is stable; it does not store Cost Adders.

### QCA (Cost Adders summary)
- Source: `quote_cost_adders`
- Meaning: Additive cost heads captured per panel, summarized for quotation.

---

## 2) Quotation Commercial View (Summary Only)

### Rule: One line per Cost Head
Quotation view MUST show exactly one line per cost head:
- FABRICATION
- BUSBAR
- LABOUR
- TRANSPORTATION
- ERECTION
- COMMISSIONING

Breakups are not visible in quotation view.

### Rule: QCA is additive
QCA adds to totals but never modifies BOM semantics.

---

## 3) Cost Sheet View (Internal Breakup Allowed)
- Detailed breakups are allowed only in cost sheets (internal view).
- Cost sheets may store analytic breakdowns, but quotation view remains summary-only.

---

## 4) Fabrication Special Rule (LOCKED)

### Commercial rule
FABRICATION appears as a single MATERIAL line in quotation summary.

### Internal breakup (analytics only)
Fabrication may be internally split, e.g.:
- ~60% Steel → MATERIAL
- ~25% Powder coating → OTHER (job work)
- ~15% Labour → LABOUR

But quotation summary bucket remains MATERIAL.

---

## 5) Enforcement Rules (Week-0)

- BOM (QCD) tables must not store cost head adders.
- `quote_cost_adders` must enforce uniqueness: one row per panel × cost head.
- Quotation UI must not expose breakup fields.
- Any future costing implementation must comply with these rules.
