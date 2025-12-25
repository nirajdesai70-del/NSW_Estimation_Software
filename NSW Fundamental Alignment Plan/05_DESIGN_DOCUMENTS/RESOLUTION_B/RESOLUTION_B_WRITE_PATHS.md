# Resolution-B Write Paths Inventory

**File:** docs/RESOLUTION_B/RESOLUTION_B_WRITE_PATHS.md  
**Version:** v1.0_2025-12-19  
**Status:** 📋 INVENTORY (Analysis Phase, No Code Changes)  
**Source:** Live DB audit report + Code Evidence Pack

---

## Purpose

Inventory ALL locations where `QuotationSaleBomItem` is written (create/update/insert) to identify:
- Write path locations and contexts
- Risk patterns (DEFAULT_ZERO, RAW_INSERT, DUPLICATE_STACK, NO_PRODUCTTYPE_CHECK)
- Required fixes for Phase-4 implementation

**Note:** This is INVENTORY ONLY. No refactoring or code changes performed.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Write Paths** | 13 |
| **Create Operations** | 13 |
| **Update Operations** | (Not inventoried - see notes) |
| **Raw DB Inserts** | 2 |
| **Apply/Copy Flows** | 2 |
| **High-Risk Paths** | 15+ (multiple risks per path possible) |

---

## A. QuotationV2Controller.php Write Paths

### A1. applyMasterBom() — Copy from Master BOM
- **File:** `app/Http/Controllers/QuotationV2Controller.php`
- **Line:** ~1027 (method definition)
- **Method:** `applyMasterBom()`
- **Context:** Copy-from-Master BOM operation (L1→L2 resolution)
- **Risk Tags:**
  - ❌ **NO_PRODUCTTYPE_CHECK** — No forced conversion to ProductType=2
  - ❌ **DEFAULT_ZERO** — Sets MakeId=0, SeriesId=0
  - ⚠️ **DUPLICATE_STACK** — Risk if called multiple times without clearing
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Gap Reference:** PB-GAP-001, PB-GAP-002
- **Findings:**
  - Creates `QuotationSaleBomItem` records with ProductId copied directly from MasterBomItem (generic products allowed)
  - Sets MakeId=0, SeriesId=0
  - No forced conversion to ProductType=2
  - Transitional state may persist as final

### A2. applyFeederTemplate() — Copy from Feeder Template
- **File:** `app/Http/Controllers/QuotationV2Controller.php`
- **Line:** ~3114 (method definition)
- **Method:** `applyFeederTemplate()`
- **Context:** Copy-from-Feeder template operation (L1→L2 resolution)
- **Risk Tags:**
  - ❌ **NO_PRODUCTTYPE_CHECK** — Copies ProductId without enforcing ProductType=2
  - ❌ **DEFAULT_ZERO** — Likely defaults MakeId/SeriesId to 0
  - ⚠️ **DUPLICATE_STACK** — Risk if called multiple times without clearing
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Gap Reference:** PB-GAP-001, PB-GAP-002
- **Findings:**
  - Copies ProductId from template items without enforcing ProductType=2
  - Same pattern as applyMasterBom()

### A3-A11. QuotationV2Controller.php Create Calls (9 instances)
- **File:** `app/Http/Controllers/QuotationV2Controller.php`
- **Lines:** 909, 1124, 1196, 1360, 1633, 1793, 1835, 1877, 3223
- **Method:** Various controller methods (not all identified)
- **Context:** Various Proposal BOM item creation operations
- **Risk Tags:**
  - ❌ **DEFAULT_ZERO** — Multiple instances use `MakeId => 0 ?? 0` or `SeriesId => 0 ?? 0` patterns
  - ❌ **NO_PRODUCTTYPE_CHECK** — Likely missing ProductType=2 validation
- **Evidence:** Live DB audit report (2025-12-19)
- **Action Required:** Each location must be reviewed individually to determine exact context and validation needs

---

## B. QuotationController.php Write Paths

### B1-B3. QuotationController.php Create Calls (3 instances)
- **File:** `app/Http/Controllers/QuotationController.php`
- **Lines:** 525, 863, 1075
- **Method:** Various controller methods (not all identified)
- **Context:** Various Proposal BOM item creation operations
- **Risk Tags:**
  - ❌ **DEFAULT_ZERO** — Likely use `MakeId => 0 ?? 0` or `SeriesId => 0 ?? 0` patterns
  - ❌ **NO_PRODUCTTYPE_CHECK** — Likely missing ProductType=2 validation
- **Evidence:** Live DB audit report (2025-12-19)
- **Action Required:** Each location must be reviewed individually to determine exact context and validation needs

---

## C. Import Command Write Paths

### C1. ImportBomJson.php Create Call
- **File:** `app/Console/Commands/ImportBomJson.php` (or similar path)
- **Line:** 354
- **Method:** Import command execution method
- **Context:** JSON import operation
- **Risk Tags:**
  - ❌ **DEFAULT_ZERO** — Likely defaults MakeId/SeriesId to 0 during import
  - ❌ **NO_PRODUCTTYPE_CHECK** — Import may not validate ProductType=2
  - ⚠️ **DUPLICATE_STACK** — Import may not clear existing items before import
- **Evidence:** Live DB audit report (2025-12-19)
- **Action Required:** Import logic must enforce L2 requirements

### C2. ImportProposalBoms.php Raw DB Insert
- **File:** `app/Console/Commands/ImportProposalBoms.php` (or similar path)
- **Line:** 282
- **Method:** Import command execution method
- **Context:** Proposal BOM import operation
- **Operation:** `DB::table('quotation_sale_bom_items')->insert()`
- **Risk Tags:**
  - 🚨 **RAW_INSERT** — Bypasses Eloquent model validation
  - ❌ **NO_PRODUCTTYPE_CHECK** — No application-level validation
  - ❌ **DEFAULT_ZERO** — Likely inserts with MakeId=0, SeriesId=0
- **Evidence:** Live DB audit report (2025-12-19)
- **Action Required:** Convert to Eloquent model or centralized write gateway
- **Severity:** HIGH — Raw inserts bypass all application validation

### C3. ImportLegacyOffers.php Raw DB Insert
- **File:** `app/Console/Commands/ImportLegacyOffers.php` (or similar path)
- **Line:** 371
- **Method:** Import command execution method
- **Context:** Legacy offer import operation
- **Operation:** `DB::table('quotation_sale_bom_items')->insert()`
- **Risk Tags:**
  - 🚨 **RAW_INSERT** — Bypasses Eloquent model validation
  - ❌ **NO_PRODUCTTYPE_CHECK** — No application-level validation
  - ❌ **DEFAULT_ZERO** — Likely inserts with MakeId=0, SeriesId=0
- **Evidence:** Live DB audit report (2025-12-19)
- **Action Required:** Convert to Eloquent model or centralized write gateway
- **Severity:** HIGH — Raw inserts bypass all application validation

---

## D. Apply/Reuse Flow Write Paths

### D1. applyProposalBom() — Apply/Reuse Proposal BOM
- **File:** `app/Http/Controllers/QuotationV2Controller.php` (or related controller)
- **Method:** `applyProposalBom()`
- **Context:** Apply/reuse Proposal BOM from another quotation
- **Risk Tags:**
  - ⚠️ **DUPLICATE_STACK** — Copies items into target BOM without clearing existing items (unless explicitly cleared)
  - ❌ **NO_PRODUCTTYPE_CHECK** — Copies items without enforcing ProductType=2 (though source items should already be L2)
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Gap Reference:** PB-GAP-004
- **Findings:**
  - Items are copied into new rows (no linking observed)
  - Risk remains for repeated apply causing duplicate items unless target BOM is cleared or guarded
  - DB triggers/cascades remain DB-PENDING (not verified)

---

## E. Manual Add Item Write Paths

### E1. addItem() — Manual Item Addition
- **File:** `app/Http/Controllers/QuotationV2Controller.php` (or related controller)
- **Method:** `addItem()`
- **Context:** Manual item addition to Proposal BOM
- **Risk Tags:**
  - ❌ **NO_PRODUCTTYPE_CHECK** — Validates product exists but does not enforce ProductType=2
  - ❌ **DEFAULT_ZERO** — MakeId/SeriesId default to 0
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-02`
- **Gap Reference:** PB-GAP-002
- **Findings:**
  - Validates product exists but does not enforce ProductType=2 (Specific products only)
  - MakeId and SeriesId are allowed to default to 0
  - Generic products can be added and persist with MakeId/SeriesId = 0, violating L2 requirement

---

## F. Make/Series Update Write Paths

### F1. updateMakeSeries() / changemakeseries() / MakeSeriesChange()
- **File:** `app/Http/Controllers/QuotationController.php` (and related controllers)
- **Methods:** `changemakeseries()`, `MakeSeriesChange()`, `getItemDescription()` (resolution logic)
- **Context:** Update Make/Series selection (L1→L2 resolution completion)
- **Risk Tags:**
  - ⚠️ **PARTIAL_RESOLUTION** — Resolution logic exists but is ad-hoc and not centralized
  - ⚠️ **NO_MANDATORY_RULE** — Not enforced as mandatory write-path rule
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-03`
- **Gap Reference:** PB-GAP-001, PB-GAP-002
- **Findings:**
  - No dedicated ProductResolutionService exists
  - Generic → Specific conversion is implemented ad-hoc inside controller methods
  - Resolution pattern: `Product::where('GenericId', $ProductId)->where('MakeId', $MakeId)->where('SeriesId', $SeriesId)->where('ProductType', 2)->first()`
  - Enforcement is partial and UI-driven (ProductType=2 check exists in API methods but NOT enforced as mandatory write-path rule)
  - No centralized validation enforces "generic → specific conversion" as required step before persistence

---

## G. Update Operations (Not Fully Inventoried)

**Note:** Update operations (`QuotationSaleBomItem::update()`, `updateOrCreate()`) were not fully inventoried in the audit report. These should be audited separately to ensure:
- ProductType cannot be changed to 1 (Generic) on existing items
- MakeId/SeriesId cannot be set to 0 on active items (Status=0)
- Validation rules are enforced on updates, not just creates

**Action Required:** Phase-4 must audit update operations separately.

---

## Risk Pattern Summary

### 🚨 RAW_INSERT (CRITICAL)
- **Count:** 2 locations
- **Files:** ImportProposalBoms.php, ImportLegacyOffers.php
- **Impact:** Bypasses ALL application validation, creates data integrity risks
- **Fix:** Convert to Eloquent model or centralized write gateway

### ❌ DEFAULT_ZERO (HIGH)
- **Count:** 13+ locations (all create paths)
- **Pattern:** `MakeId => 0 ?? 0`, `SeriesId => 0 ?? 0`
- **Impact:** Allows invalid L2 state (MakeId=0, SeriesId=0) to persist
- **Fix:** Enforce MakeId>0, SeriesId>0 for ProductType=2 items

### ❌ NO_PRODUCTTYPE_CHECK (HIGH)
- **Count:** 13+ locations (all create paths)
- **Impact:** Generic products (ProductType=1) can persist in Proposal BOM
- **Fix:** Enforce ProductType=2 validation on all write paths

### ⚠️ DUPLICATE_STACK (MEDIUM)
- **Count:** 3+ locations (apply/copy flows, imports)
- **Impact:** Repeated apply operations create duplicate items
- **Fix:** Clear existing items before apply, or implement explicit merge mode

---

## Phase-4 Action Items

1. **Centralize Write Gateway**
   - Create `ProposalBomItemWriter` service
   - All write paths must use gateway
   - Gateway enforces all L2 requirements

2. **Fix Raw Inserts**
   - Convert ImportProposalBoms.php to use Eloquent or gateway
   - Convert ImportLegacyOffers.php to use Eloquent or gateway

3. **Remove Default-Zero Patterns**
   - Replace all `MakeId => 0 ?? 0` with validation
   - Replace all `SeriesId => 0 ?? 0` with validation
   - Enforce MakeId>0, SeriesId>0 for ProductType=2

4. **Add ProductType Validation**
   - All write paths must validate ProductType=2
   - Exception: Transitional state (must resolve before finalization)

5. **Fix Duplicate Stacking**
   - All apply/copy flows must clear existing items OR use explicit merge mode
   - Document merge behavior explicitly

6. **Centralize Resolution Logic**
   - Create ProductResolutionService
   - Replace ad-hoc resolution logic in controllers
   - Enforce resolution as mandatory before persistence

---

## References

- `RESOLUTION_B_RULES.md` — L2 write enforcement rules
- `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md` — Code evidence findings
- `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` — Gap register with PB-GAP-001 through PB-GAP-004
- Live DB audit report (2025-12-19) — Write path locations and line numbers

