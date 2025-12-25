# Panel BOM Gates Tracker

**File:** PLANNING/PANEL_BOM/GATES_TRACKER.md  
**Version:** v1.0  
**Date:** 2025-12-23  
**Status:** 📋 PLANNING ONLY (Execution deferred until approval)  
**Purpose:** Define Panel BOM verification gates (Gate-0 through Gate-5) with evidence stubs and stop-rule enforcement

---

## ⚠️ CRITICAL: PLANNING MODE

**MODE:** 📋 PLANNING ONLY  
**EXECUTION:** ⛔ DEFERRED until execution windows + evidence + stop-rule  
**IMPLEMENTATION STATUS:** ⚠️ Unknown until verified during execution window

This tracker defines the verification gates that will be executed during the Panel BOM execution window. All gates follow the same governance pattern as Feeder BOM (Gate-0/R1/S1/R2/S2 approach).

**Stop Rule:** If any gate/check fails → STOP → capture evidence → no patching in same window unless explicitly approved.

---

## Gate Structure Overview

| Gate | Name | Purpose | Evidence Location | Status |
|------|------|---------|-------------------|--------|
| **Gate-0** | Panel Source Readiness | Verify panel has valid feeders/BOMs | `evidence/PANEL_BOM/G0_panel_readiness.txt` | ⏳ PENDING (Planning) |
| **Gate-1** | Schema + History Readiness | Verify tables and history support | `evidence/PANEL_BOM/G1_schema_history.txt` | ⏳ PENDING (Planning) |
| **Gate-2** | Controller/Route Wiring Proof | Verify thin controller + BomEngine integration | `evidence/PANEL_BOM/G2_controller_wiring.txt` | ⏳ PENDING (Planning) |
| **Gate-3** | R1/S1/R2/S2 Sequence | Panel copy verification (idempotent, reuse detection) | `evidence/PANEL_BOM/R1_S1_S2/` | ⏳ PENDING (Planning) |
| **Gate-4** | Rollup Verification | Quantity contract verification (already locked) | `evidence/PANEL_BOM/G4_rollup_verification.txt` | ⏳ PENDING (Planning) |
| **Gate-5** | Lookup Integrity | Panel → Feeder → Item lookup chain | `evidence/PANEL_BOM/G5_lookup_integrity.txt` | ⏳ PENDING (Planning) |

---

## Gate-0: Panel Source Readiness

**Status:** ⏳ PENDING (Planning)  
**Purpose:** Verify Panel Master has valid structure (feeders, BOMs) before copy operation  
**Execution:** Pre-flight check (read-only verification)

### Entry Criteria
- [ ] Panel Master design documents reviewed
- [ ] Panel Master data structure understood
- [ ] Feeder reference structure validated

### Verification Checks

**G0.1: Panel Master has Feeders**
- [ ] Panel Master has N>0 feeder references
- [ ] Feeder references are valid (FeederMasterId present OR FeederName present)
- [ ] Feeder references have valid Quantity, Sequence, Status fields
- **Verification Method:** SQL query or data inspection
- **Expected Result:** Panel Master has at least one valid feeder reference

**G0.2: Feeder Templates Valid (if FeederMasterId present)**
- [ ] FeederMasterId references valid Feeder Master templates
- [ ] Feeder Master templates have valid structure
- [ ] Feeder Master templates have items/BOMs
- **Verification Method:** SQL JOIN query or data inspection
- **Expected Result:** All FeederMasterId references resolve to valid templates

**G0.3: Direct Feeder References Valid (if FeederName present)**
- [ ] FeederName references existing feeder instances (if applicable)
- [ ] Direct feeder references have valid structure
- **Verification Method:** Data inspection or SQL query
- **Expected Result:** All direct feeder references are valid

### Evidence Requirements
- [ ] SQL query output (if applicable)
- [ ] Panel Master structure summary
- [ ] Feeder reference count and validation results
- **Evidence File:** `evidence/PANEL_BOM/G0_panel_readiness.txt`

### Exit Criteria
- ✅ All checks pass
- ✅ Panel Master is ready for copy operation
- ✅ Evidence captured

**Blocking:** Gate-1, Gate-2, Gate-3

---

## Gate-1: Schema + History Readiness

**Status:** ⏳ PENDING (Planning)  
**Purpose:** Verify database schema supports Panel BOM operations (tables, columns, history)  
**Execution:** Pre-flight check (read-only schema inspection)

### Entry Criteria
- [ ] Gate-0 passed
- [ ] Database access available (read-only)

### Verification Checks

**G1.1: Panel Tables Exist**
- [ ] `panel_masters` table exists (or logical entity confirmed)
- [ ] `panel_master_feeders` table exists (or logical entity confirmed)
- [ ] `quotation_sales` table exists (Proposal Panel storage)
- [ ] Required columns exist (PanelMasterId, PanelQty, etc.)
- **Verification Method:** `SHOW TABLES` or schema inspection
- **Expected Result:** All required tables/entities exist with correct structure

**G1.2: bom_copy_history Supports Panel Copy**
- [ ] `bom_copy_history` table exists (shared with Feeder BOM)
- [ ] Columns support panel copy: SourceType='PANEL_MASTER', TargetType='PROPOSAL_PANEL'
- [ ] ID mapping structure supports panel → panel, feeder → feeder, BOM → BOM mappings
- [ ] History recording pattern compatible with Panel copy flow
- **Verification Method:** Schema inspection, verify column definitions
- **Expected Result:** bom_copy_history can record Panel copy operations

**G1.3: Runtime BOM Tables Support Panel Structure**
- [ ] `quotation_sale_boms` table supports Level=0 (feeders), Level>=1 (BOMs)
- [ ] `ParentBomId` column supports parent-child relationships
- [ ] `Status` column supports soft delete (0=active, 1=deleted)
- [ ] `quotation_sale_bom_items` table supports item storage
- **Verification Method:** Schema inspection
- **Expected Result:** Runtime tables support Panel → Feeder → BOM → Item hierarchy

### Evidence Requirements
- [ ] Schema verification queries/output
- [ ] Table structure confirmation
- [ ] Column definitions documented
- **Evidence File:** `evidence/PANEL_BOM/G1_schema_history.txt`

### Exit Criteria
- ✅ All schema checks pass
- ✅ History recording structure confirmed
- ✅ Evidence captured

**Blocking:** Gate-2, Gate-3

---

## Gate-2: Controller/Route Wiring Proof

**Status:** ⏳ PENDING (Planning)  
**Purpose:** Verify thin controller contract + BomEngine integration for Panel copy  
**Execution:** Code inspection (no runtime execution)

### Entry Criteria
- [ ] Gate-1 passed
- [ ] Codebase access available

### Verification Checks

**G2.1: Controller Method Exists**
- [ ] Controller method exists for Panel copy operation
- [ ] Method accepts required parameters (PanelMasterId, QuotationId, etc.)
- [ ] Method follows thin controller pattern (no direct DB writes)
- **Verification Method:** Code inspection
- **Expected Result:** Controller method exists and is thin (delegates to service)

**G2.2: Route Exists**
- [ ] API route exists for Panel copy endpoint
- [ ] Route points to controller method
- [ ] Route method (POST/PUT) appropriate for copy operation
- **Verification Method:** Route inspection (routes file, API documentation)
- **Expected Result:** Route exists and is properly configured

**G2.3: BomEngine::copyPanelTree() Called**
- [ ] Controller calls `BomEngine::copyPanelTree()` (or equivalent method)
- [ ] Method signature matches Panel copy requirements
- [ ] Method returns structured response with evidence fields
- **Verification Method:** Code inspection (trace controller → service call)
- **Expected Result:** BomEngine method is called, not direct DB writes

**G2.4: Thin Controller Contract Verified**
- [ ] No direct DB writes in controller
- [ ] No business logic in controller
- [ ] Controller only validates input, calls service, returns response
- **Verification Method:** Code inspection
- **Expected Result:** Controller is thin (all logic in BomEngine)

### Evidence Requirements
- [ ] Code snippets showing controller structure
- [ ] Route definition
- [ ] BomEngine method signature (if exists)
- [ ] Thin controller verification (no direct DB writes)
- **Evidence File:** `evidence/PANEL_BOM/G2_controller_wiring.txt`

### Exit Criteria
- ✅ All wiring checks pass
- ✅ Thin controller contract verified
- ✅ Evidence captured

**Blocking:** Gate-3

---

## Gate-3: R1/S1/R2/S2 Sequence

**Status:** ⏳ PENDING (Planning)  
**Purpose:** Verify Panel copy operation (idempotent, reuse detection, clear-before-copy)  
**Execution:** Runtime verification (deferred until execution window)

### Entry Criteria
- [ ] Gate-2 passed
- [ ] Test fixtures available (QuotationId, PanelMasterId, etc.)
- [ ] Execution window approved

### Verification Sequence

**R1: First Panel Copy API Call**
- [ ] Execute Panel copy API call (first time)
- [ ] Capture API response (JSON)
- [ ] Verify response structure (success, evidence fields)
- [ ] Verify Proposal Panel created (new QuotationSaleId)
- [ ] Verify Feeders created (new QuotationSaleBomId, Level=0)
- [ ] Verify BOMs created (new QuotationSaleBomId, Level>=1)
- [ ] Verify Items created (new QuotationSaleBomItemId)
- **Evidence File:** `evidence/PANEL_BOM/R1_S1_S2/R1.json`

**S1: First Verification SQL**
- [ ] Query copy history (bom_copy_history where SourceType='PANEL_MASTER')
- [ ] Verify history record created for Panel copy
- [ ] Verify ID mappings correct (Panel → Panel, Feeder → Feeder, BOM → BOM, Item → Item)
- [ ] Query structure integrity (verify parent-child relationships)
- [ ] Verify Status=0 (active) for all created instances
- [ ] Verify PanelMasterId stored (reference-only, never mutated)
- **Evidence File:** `evidence/PANEL_BOM/R1_S1_S2/S1_sql_output.txt`

**R2: Re-Apply Panel Copy (Idempotent)**
- [ ] Execute Panel copy API call again (same PanelMasterId, QuotationId)
- [ ] Capture API response (JSON)
- [ ] Verify response indicates reuse detection (if applicable)
- [ ] Verify no duplicate instances created
- [ ] Verify clear-before-copy behavior (if applicable)
- **Evidence File:** `evidence/PANEL_BOM/R1_S1_S2/R2.json`

**S2: Second Verification SQL**
- [ ] Query copy history (verify reuse detection or new copy)
- [ ] Verify no duplicate instances (count verification)
- [ ] Verify clear-before-copy behavior (if Status=1 for cleared instances)
- [ ] Verify structure integrity maintained
- [ ] Verify copy-never-link rule (independent instances)
- **Evidence File:** `evidence/PANEL_BOM/R1_S1_S2/S2_sql_output.txt`

### Verification Checks

**G3.1: Copy History Recorded**
- [ ] bom_copy_history has record for Panel copy
- [ ] Source/target snapshots correct
- [ ] ID mappings correct (JSON structure)
- **Expected Result:** History record exists with correct structure

**G3.2: Structure Integrity**
- [ ] Parent-child relationships correct (ParentBomId points to valid parents)
- [ ] Level hierarchy correct (Level=0 for feeders, Level>=1 for BOMs)
- [ ] Item → BOM relationships correct
- **Expected Result:** Structure matches Panel Master structure

**G3.3: Copy-Never-Link Rule**
- [ ] New instances created (new IDs)
- [ ] PanelMasterId stored but never mutated
- [ ] No direct references back to master (except PanelMasterId tracking)
- **Expected Result:** All instances are independent copies

**G3.4: Reuse Detection (R2)**
- [ ] Reuse detection works (if same panel copied twice)
- [ ] Or clear-before-copy works (if applicable)
- [ ] No duplicate stacking
- **Expected Result:** Idempotent behavior verified

### Evidence Requirements
- [ ] R1 API response (JSON)
- [ ] S1 SQL queries and outputs
- [ ] R2 API response (JSON)
- [ ] S2 SQL queries and outputs
- [ ] Verification summary
- **Evidence Directory:** `evidence/PANEL_BOM/R1_S1_S2/`

### Exit Criteria
- ✅ All R1/S1/R2/S2 checks pass
- ✅ Copy operation verified (idempotent, reuse detection)
- ✅ Evidence captured

**Blocking:** Gate-4, Gate-5

---

## Gate-4: Rollup Verification

**Status:** ⏳ PENDING (Planning)  
**Purpose:** Verify quantity contract (Panel qty multiply happens once)  
**Execution:** Runtime verification (deferred until execution window)  
**Note:** Quantity contract already verified and locked per user confirmation  
**Detailed Document:** `PLANNING/PANEL_BOM/GATE4_ROLLUP.md`

### Entry Criteria
- [ ] Gate-3 passed
- [ ] Quantity contract already verified (locked)

### Verification Checks

**G4.1: Quantity Contract Verified**
- [ ] Panel qty multiply happens once (inside quotationAmount())
- [ ] Component level: ItemQty × BOMQty (standard multiplication)
- [ ] Panel level: multiply once by PanelQty
- [ ] No double multiplication
- [ ] No additional multipliers in rollup
- **Verification Method:** Calculation verification, code inspection
- **Expected Result:** Quantity contract confirmed (already verified)

**G4.2: Rollup Calculations Correct**
- [ ] Item → BOM rollup correct
- [ ] BOM → Feeder rollup correct
- [ ] Feeder → Panel rollup correct
- [ ] Panel → Proposal amount correct
- **Verification Method:** Calculation verification, SQL rollup queries
- **Expected Result:** All rollup calculations correct

### Evidence Requirements
- [ ] Quantity contract verification (already locked)
- [ ] Rollup calculation verification
- [ ] quotationAmount() method review (if applicable)
- **Evidence File:** `evidence/PANEL_BOM/G4_rollup_verification.txt`

### Exit Criteria
- ✅ Quantity contract verified (already locked)
- ✅ Rollup calculations correct
- ✅ Evidence captured

**Blocking:** Gate-5

---

## Gate-5: Lookup Integrity

**Status:** ⏳ PENDING (Planning)  
**Purpose:** Verify Panel → Feeder → Item lookup chain integrity  
**Execution:** Runtime verification (deferred until execution window)  
**Note:** Reuses Phase-4 lookup integrity rules from Feeder BOM  
**Detailed Document:** `PLANNING/PANEL_BOM/GATE5_LOOKUP_INTEGRITY.md`

### Entry Criteria
- [ ] Gate-4 passed
- [ ] Lookup integrity rules from Feeder BOM available

### Verification Checks

**G5.1: Panel → Feeder Lookup**
- [ ] Panel can resolve to Feeders (via QuotationSaleBom, Level=0)
- [ ] Feeder references valid (FeederMasterId or FeederName)
- [ ] Lookup chain: Panel → Feeders → Items
- **Verification Method:** SQL JOIN queries, data inspection
- **Expected Result:** Panel → Feeder lookup chain works

**G5.2: Feeder → BOM Lookup**
- [ ] Feeder can resolve to nested BOMs (via QuotationSaleBom, Level>=1)
- [ ] Parent-child relationships correct (ParentBomId)
- [ ] Lookup chain: Feeder → BOMs → Items
- **Verification Method:** SQL JOIN queries
- **Expected Result:** Feeder → BOM lookup chain works

**G5.3: BOM → Item Lookup**
- [ ] BOM can resolve to Items (via QuotationSaleBomItem)
- [ ] Item → Item Master resolution works
- [ ] Lookup chain: BOM → Items → Item Master
- **Verification Method:** SQL JOIN queries
- **Expected Result:** BOM → Item lookup chain works

**G5.4: End-to-End Lookup Chain**
- [ ] Panel → Feeder → BOM → Item → Item Master chain works
- [ ] All lookups resolve correctly
- [ ] No broken references
- **Verification Method:** End-to-end SQL query or data inspection
- **Expected Result:** Complete lookup chain works

### Evidence Requirements
- [ ] Lookup integrity queries (reuse Phase-4 rules)
- [ ] Lookup chain verification results
- [ ] Reference integrity confirmation
- **Evidence File:** `evidence/PANEL_BOM/G5_lookup_integrity.txt`

### Exit Criteria
- ✅ All lookup checks pass
- ✅ Lookup chain integrity verified
- ✅ Evidence captured

**Blocking:** Panel BOM PASS declaration

---

## Panel BOM PASS Declaration

**Only declare after all gates (Gate-0 through Gate-5) pass:**

```
Panel BOM PASS — Copy engine live (panel verified).

Evidence:
- Gate-0: Panel source readiness verified
- Gate-1: Schema + history readiness verified
- Gate-2: Controller/route wiring verified (thin controller)
- Gate-3: R1/S1/R2/S2 verification passed (idempotent, reuse detection)
- Gate-4: Rollup verification passed (quantity contract locked)
- Gate-5: Lookup integrity verified (Panel → Feeder → Item chain)
```

**Then update gap register:**
- Panel BOM gaps → CLOSED (if any)
- Related gaps → CLOSED (if applicable)

---

## Evidence Directory Structure

```
evidence/PANEL_BOM/
├── G0_panel_readiness.txt
├── G1_schema_history.txt
├── G2_controller_wiring.txt
├── R1_S1_S2/
│   ├── R1.json (optional)
│   ├── S1_sql_output.txt
│   ├── R2.json (optional)
│   └── S2_sql_output.txt
├── G4_rollup_verification.txt
└── G5_lookup_integrity.txt
```

---

## Stop Rule Enforcement

**If any gate/check fails:**

1. **STOP** immediately
2. **Capture evidence** (failure details, SQL outputs, error messages)
3. **Document failure** in evidence file
4. **Do NOT patch** in same window unless explicitly approved
5. **Report failure** and wait for approval before proceeding

**Exception:** Only proceed if failure is documented as acceptable deviation and approved.

---

## Alignment with Feeder BOM

| Feeder BOM Gate | Panel BOM Gate | Alignment |
|-----------------|----------------|-----------|
| Gate-0 (Source Readiness) | Gate-0 (Panel Source Readiness) | ✅ Same pattern |
| Gate-1 (Schema/History) | Gate-1 (Schema + History Readiness) | ✅ Same pattern |
| Gate-2 (Wiring) | Gate-2 (Controller/Route Wiring) | ✅ Same pattern |
| Gate-3 (R1/S1/R2/S2) | Gate-3 (R1/S1/R2/S2 Sequence) | ✅ Same pattern |
| Gate-4 (Rollup) | Gate-4 (Rollup Verification) | ✅ Same pattern (Panel-specific) |
| Gate-5 (Lookup) | Gate-5 (Lookup Integrity) | ✅ Same pattern (Panel chain) |

---

## References

### Internal Documents
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` - Main planning track
- `PLANNING/PANEL_BOM/CANONICAL_FLOW.md` - Canonical flow (PB0.1)
- `PLANNING/PANEL_BOM/COPY_RULES.md` - Copy rules (PB0.2)
- `PLANNING/PANEL_BOM/QUANTITY_CONTRACT.md` - Quantity contract (PB0.3)
- `PLANNING/PANEL_BOM/GATE4_ROLLUP.md` - Gate-4 detailed verification plan
- `PLANNING/PANEL_BOM/GATE5_LOOKUP_INTEGRITY.md` - Gate-5 detailed verification plan

### External References
- `docs/FEEDER_BOM/PHASE2_EXECUTION_CHECKLIST.md` - Feeder BOM gate pattern
- `docs/FEEDER_BOM/PHASE2_2_VERIFICATION_SQL.md` - Verification SQL pattern
- `PLANNING/FEEDER_BOM/FEEDER_BOM_PLAN_NORMALIZATION.md` - Feeder BOM governance

---

**END OF DOCUMENT**

