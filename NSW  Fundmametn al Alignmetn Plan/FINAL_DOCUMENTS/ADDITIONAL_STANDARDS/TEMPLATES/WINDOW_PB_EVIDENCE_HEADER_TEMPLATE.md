# Window-PB Evidence Header Template

**File:** PLANNING/PANEL_BOM/WINDOW_PB_EVIDENCE_HEADER_TEMPLATE.md  
**Version:** v1.0  
**Date:** 2025-12-23  
**Status:** ✅ FROZEN  
**Purpose:** Canonical evidence header template for all Window-PB evidence files

---

## ⚠️ CANONICAL TEMPLATE (DO NOT MODIFY)

This is the **single source of truth** for Window-PB evidence headers. All evidence files must use this exact header format to ensure consistency during execution windows.

---

## Standard Evidence Header (Gate-0, Gate-1, Gate-2)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** Gate-0, Gate-1, Gate-2 evidence files

---

## Gate-0 Specific Header (Panel Readiness)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
QuotationId: <QuotationId>
PanelMasterId: <PanelMasterId>
Panel Master Name: <PanelMasterName>
Panel Master Status: <Status>
Active Feeder Count (N): <N>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** `evidence/PANEL_BOM/G0_panel_readiness.txt`

---

## Gate-1 Specific Header (Schema/History)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
Database: <database_name>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** `evidence/PANEL_BOM/G1_schema_history.txt`

---

## Gate-2 Specific Header (Controller Wiring)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** `evidence/PANEL_BOM/G2_controller_wiring.txt`

---

## Gate-3 Specific Header (R1/S1/R2/S2 Sequence)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
QuotationId: <QuotationId>
PanelId: <PanelId>
PanelMasterId: <PanelMasterId>
Active Feeder Count (N): <N>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** 
- `evidence/PANEL_BOM/R1_S1_S2/S1_sql_output.txt`
- `evidence/PANEL_BOM/R1_S1_S2/S2_sql_output.txt`

---

## Gate-4 Specific Header (Rollup Verification)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
QuotationId: <QuotationId>
PanelId: <PanelId>
PanelMasterId: <PanelMasterId>
PanelQty: <PanelQty>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** `evidence/PANEL_BOM/G4_rollup_verification.txt`

---

## Gate-5 Specific Header (Lookup Integrity)

```
=== Window-PB Evidence Header ===

Execution Window: Window-PB
Date/Time: <datetime>
Operator: <operator>
QuotationId: <QuotationId>
PanelId: <PanelId>
PanelMasterId: <PanelMasterId>
Stop-Rule Applied: <stop-rule line>

---
```

**Usage:** `evidence/PANEL_BOM/G5_lookup_integrity.txt`

---

## Stop-Rule Reference

**Standard Stop-Rule Text:**
```
If any Gate fails → STOP → capture evidence → no patching in same window unless explicitly approved.
```

---

## Evidence File Footer

All evidence files should end with:

```
---

**END OF EVIDENCE FILE**
```

---

## Usage Instructions

1. **Copy the appropriate header** from this template based on the gate type
2. **Replace placeholders** with actual values during execution
3. **Do not modify** the header structure or field names
4. **Maintain consistency** across all evidence files in the same execution window

---

**END OF TEMPLATE**

