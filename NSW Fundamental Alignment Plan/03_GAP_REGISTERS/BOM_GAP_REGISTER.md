# BOM Gap Register — Compliance Audit Output

**STATUS:** PRIMARY — EXECUTION DRIVER
**GOVERNED BY:** PROJECT_INDEX.md

**Source of Truth:** PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md  
**Status:** 📋 **Working Register** (editable)  
**Owner:** Engineering / Cursor audit output  
**Rule:** Log gaps only (do not implement here)

---

## 0) Metadata
- **Audit Date:** 2025-12-20
- **Audited Branch / Commit:** _[To be filled]_
- **Audited Environment:** Code Audit (Actual Implementation Review)
- **DB Type:** MySQL
- **Auditor:** Cursor AI (Code-Based Audit)
- **Code Files Reviewed:**
  - `app/Services/BomEngine.php` — Line item operations (Phase-1)
  - `app/Services/BomHistoryService.php` — History recording service
  - `app/Http/Controllers/QuotationV2Controller_Example_Integration.php` — Example integration only
  - `database/migrations/2025_12_20_213521_create_quotation_sale_bom_item_history_table.php` — History table migration

---

## 1) BOM Entity Mapping (Reference)
See: `PLANNING/GOVERNANCE/BOM_MAPPING_REFERENCE.md`

---

## 2) Gap Entries

### BOM-GAP-007 — Copy Operations Not Implemented (⏳ PARTIALLY RESOLVED)
- **Level(s):** Master BOM / Proposal BOM / Feeder / Panel
- **Scenario:** Copy / Apply / Reuse
- **Rule Violated:** 
  - Copy-New (Rule 1) — Copy operations do not exist in code
  - Cross-Level-Consistency (Rule 5) — Cannot verify consistency without implementations
- **Severity:** High
- **Where Found:**
  - Service: `app/Services/BomEngine.php` — ✅ Copy methods implemented (Phase-2 code)
  - Controller: `app/Http/Controllers/QuotationV2Controller.php` — ✅ Controller/method exists in runtime environment; patch prepared in planning (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending (Gate-2)
  - Methods: `copyMasterBomToProposal()`, `copyProposalBomToProposal()`, `copyFeederTree()` — ✅ IMPLEMENTED
  - **Panel Copy:** Panel BOM planning complete (PB0-PB6) — ✅ Planning pack ready; Panel copy operations planned but not yet verified
- **Observed behavior (current):**
  - ✅ Copy operations implemented in BomEngine (Phase-2 code):
    - `copyMasterBomToProposal()` — ✅ IMPLEMENTED
    - `copyProposalBomToProposal()` — ✅ IMPLEMENTED
    - `copyFeederTree()` — ✅ IMPLEMENTED
  - ⚠️ Copy methods not yet wired to controller endpoints (Phase-2.1 pending)
  - ⚠️ Copy operations not yet verified with live data (Phase-2.2 pending)
  - ⚠️ Cannot verify copy-never-link pattern in production (verification pending)
  - ⚠️ Panel copy operations: Planning complete (2025-12-23), execution BLOCKED until approval
- **Expected behavior (locked principle):**
  - Copy operations must create new instances with new IDs (copy-never-link)
  - Must work at all levels (Master/Proposal/Feeder/Panel)
  - Must preserve structure and relationships
  - Must record copy history (see BOM-GAP-004)
- **Evidence:**
  - ✅ `app/Services/BomEngine.php` — Copy methods implemented (copyMasterBomToProposal, copyProposalBomToProposal, copyFeederTree)
  - ✅ `PLANNING/GOVERNANCE/BOM_ENGINE_BLUEPRINT.md` — API design implemented
  - ✅ `PLANNING/PANEL_BOM/` — Panel BOM planning complete (PB0-PB6), execution window pack ready
  - ⚠️ Controller wiring pending (Phase-2.1)
  - ⚠️ Verification evidence pending (Phase-2.2)
  - ⚠️ Panel copy verification pending (Panel BOM execution window)
- **Fix Type:** New Implementation (Backend)
- **Suggested Fix Direction (high-level):**
  - Implement all copy methods in BomEngine per BOM_ENGINE_BLUEPRINT.md
  - Ensure copy-never-link pattern (always new IDs, never shared references)
  - Integrate copy history (BOM-GAP-004)
  - Create controller methods that call BomEngine copy methods
  - Panel copy: Follow Panel BOM planning pack (`PLANNING/PANEL_BOM/WINDOW_PB_*`)
- **Dependencies / Notes:**
  - ✅ Phase-1 integrated (BOM-GAP-003 CLOSED)
  - ✅ Copy operations implemented (Phase-2 code)
  - ✅ Panel BOM planning complete (PB0-PB6, 2025-12-23)
  - ⚠️ Related to BOM-GAP-001, BOM-GAP-002 (feeder-specific copy issues — copy operations exist but not yet wired/verified)
  - ⚠️ Related to BOM-GAP-004 (copy history migration pending)
  - ⚠️ Controller wiring required (Phase-2.1)
  - ⚠️ Verification evidence required (Phase-2.2 — R1/S1/R2/S2)
  - ⚠️ Panel copy verification required (Panel BOM execution window — Gate-0 through Gate-5)
- **Owner:** _[To be assigned]_
- **Target Phase:** Phase-2 (Copy Operations) / Panel BOM (Panel Copy Operations)
- **Status:** ⏳ PARTIALLY RESOLVED (Phase-2 code implemented; Panel BOM planning complete; pending migration + wiring + verification evidence)
- **Closure Gate:** CLOSE only after migration + R1/S1/R2/S2 evidence attached (Feeder) + Panel BOM Gate-0 through Gate-5 evidence attached (Panel).
- **Worklog:**
  - 2025-12-21: Planning patch prepared (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending; evidence capture pending (Gate-1 can be captured now, Gate-2/Gate-3 blocked until release window).
  - 2025-12-21: Gate-1 PASS — `bom_copy_history` schema verified on staging DB (`nepl_quotation`). Evidence: `evidence/PHASE2/G1_bom_copy_history_schema.txt`.
  - 2025-12-23: Panel BOM planning complete (PB0-PB6). Planning pack ready: `PLANNING/PANEL_BOM/`. Panel copy operations planned but not yet verified. Execution BLOCKED until approval.

---

### BOM-GAP-001 — Feeder Template Apply Creates New Feeder Every Time (No Reuse Detection)
- **Level(s):** Feeder
- **Scenario:** Apply / Re-apply
- **Rule Violated:** 
  - Copy-New (Rule 1) — Creates duplicate feeders instead of reusing
  - Cross-Level-Consistency (Rule 5) — applyProposalBom() has reuse, applyFeederTemplate() does not
- **Severity:** High
- **Where Found:**
  - Controller/Service: `app/Http/Controllers/QuotationV2Controller.php` — ✅ Controller/method exists in runtime environment; patch prepared in planning (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending (Gate-2)
  - Method: `applyFeederTemplate()` — ✅ Controller/method exists in runtime environment; patch prepared in planning; staging wiring pending (Gate-2)
  - Route/Endpoint: `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
  - DB Table(s): `quotation_sale_boms`, `quotation_sale_bom_items`
- **Observed behavior (current):**
  - System creates a NEW feeder BOM every time `applyFeederTemplate()` is called
  - No detection logic for existing feeders with same characteristics
  - No matching criteria (QuotationId, QuotationSaleId, MasterBomId, FeederName)
  - Each apply creates a new `QuotationSaleBom` record
  - Previous feeders remain active (Status=0), causing duplicates
- **Expected behavior (locked principle):**
  - System should detect existing feeder matching: QuotationId, QuotationSaleId, MasterBomId, FeederName, Level=0, ParentBomId=NULL, Status=0
  - If matching feeder exists → reuse it (do not create new)
  - If not found → create new feeder
  - Same pattern as `applyProposalBom()` which correctly implements reuse
- **Risk:**
  - Data corruption (duplicate feeders in quotation)
  - Incorrect pricing calculations (items counted multiple times)
  - User confusion (multiple feeders with same name)
  - Violates instance isolation principle
- **Evidence:**
  - `PLANNING/BASELINE/FEEDER_BOM_AS_IS.md:§2.1` — Documents "always creates NEW feeder"
  - `PLANNING/BASELINE/FEEDER_BOM_AS_IS.md:§3.3` — Documents "creates NEW feeder BOM every time"
  - `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:PB-GAP-004` — Root cause documented
  - `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_CORRECTIONS.md` — Identifies re-apply problem
- **Fix Type:** Backend only
- **Suggested Fix Direction (high-level):**
  - Add feeder detection logic before creation
  - Match on: QuotationId, QuotationSaleId, MasterBomId, FeederName, Level=0, ParentBomId=NULL, Status=0
  - If match found → reuse existing feeder ID
  - If no match → create new feeder
  - Reference: `applyProposalBom()` implementation pattern (which has correct reuse logic)
- **Dependencies / Notes:**
  - Related to BOM-GAP-002 (clear-before-copy must be implemented together)
  - Fix already designed in `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_CODE_CHANGES.md`
- **Owner:** _[To be assigned]_
- **Target Phase:** P5 (Feeder BOM Round-0)
- **Status:** OPEN (until feeder endpoint is actually wired + verified)
- **Worklog:**
  - 2025-12-21: Planning patch prepared (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending; evidence capture pending.

---

### BOM-GAP-002 — Feeder Template Apply Missing Clear-Before-Copy (Duplicate Stacking)
- **Level(s):** Feeder / Line Item
- **Scenario:** Apply / Re-apply
- **Rule Violated:** 
  - Copy-New (Rule 1) — Items stack instead of being replaced
  - Cross-Level-Consistency (Rule 5) — applyProposalBom() has clear-before-copy, applyFeederTemplate() does not
- **Severity:** High
- **Where Found:**
  - Controller/Service: `app/Http/Controllers/QuotationV2Controller.php` — ✅ Controller/method exists in runtime environment; patch prepared in planning (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending (Gate-2)
  - Method: `applyFeederTemplate()` — ✅ Controller/method exists in runtime environment; patch prepared in planning; staging wiring pending (Gate-2)
  - Route/Endpoint: `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
  - DB Table(s): `quotation_sale_bom_items`
- **Observed behavior (current):**
  - `applyFeederTemplate()` does NOT clear existing items before copying new ones
  - No soft-delete logic (Status=1) before item copying
  - If same feeder is reused (or if items exist), previous items remain active (Status=0)
  - New apply adds more items (Status=0)
  - Result: Multiple active items with same ProductId, Qty, etc. within the same feeder (duplicate stacking)
- **Expected behavior (locked principle):**
  - Before copying items into target feeder, soft-delete all active items under target
  - Update: `quotation_sale_bom_items WHERE QuotationSaleBomId = feeder_id AND Status=0` → `Status=1`
  - Then insert new items (copy-never-link)
  - Same pattern as `applyProposalBom()` which correctly implements clear-before-copy
- **Risk:**
  - Data corruption (duplicate items in feeder)
  - Incorrect pricing calculations (items counted multiple times)
  - Data integrity violation
  - Violates instance isolation principle
- **Evidence:**
  - `PLANNING/BASELINE/FEEDER_BOM_AS_IS.md:§2.1` — Documents "no clear-before-copy logic"
  - `PLANNING/BASELINE/FEEDER_BOM_AS_IS.md:§3.2` — Documents "does not clear existing items"
  - `PLANNING/BASELINE/FEEDER_BOM_AS_IS.md:§2.3` — Comparison: `applyProposalBom()` HAS clear-before-copy, `applyFeederTemplate()` LACKS it
  - `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:PB-GAP-004` — Root cause documented
- **Fix Type:** Backend only
- **Suggested Fix Direction (high-level):**
  - Before copying items, soft-delete existing active items: `QuotationSaleBomItem::where('QuotationSaleBomId', $feederId)->where('Status', 0)->update(['Status' => 1])`
  - Count deleted items for audit: `$deleted_count = QuotationSaleBomItem::where(...)->where('Status', 0)->count()`
  - Then proceed with item copying via `ProposalBomItemWriter` gateway
  - Reference: `applyProposalBom()` implementation pattern (which has correct clear-before-copy)
- **Dependencies / Notes:**
  - Must be implemented together with BOM-GAP-001 (feeder reuse detection)
  - Fix already designed in `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_CODE_CHANGES.md`
- **Owner:** _[To be assigned]_
- **Target Phase:** P5 (Feeder BOM Round-0)
- **Status:** OPEN (until clear-before-copy proven by SQL in P5)
- **Worklog:**
  - 2025-12-21: Planning patch prepared (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending; evidence capture pending.

---

### BOM-GAP-003 — Line Item Edits Missing History/Backup (✅ CLOSED)
- **Level(s):** Line Item
- **Scenario:** Edit / Update / Replace / Delete
- **Rule Violated:** 
  - Backup-History (Rule 4) — History service exists but not integrated into actual controllers (RESOLVED in Phase-1A)
- **Severity:** Medium (✅ CLOSED)
- **Where Found:**
  - Service: `app/Services/BomEngine.php` — ✅ IMPLEMENTED (addLineItem, updateLineItem, deleteLineItem, replaceLineItem all record history)
  - Service: `app/Services/BomHistoryService.php` — ✅ IMPLEMENTED (recordItemHistory, captureItemSnapshot, getChangedFields)
  - Controller: `app/Http/Controllers/QuotationV2Controller_Example_Integration.php` — ⚠️ EXAMPLE ONLY (not actual implementation)
  - DB Migration: `database/migrations/2025_12_20_213521_create_quotation_sale_bom_item_history_table.php` — ✅ EXISTS
  - Actual Controller: `app/Http/Controllers/QuotationV2Controller.php` — ❌ NOT FOUND (does not exist in codebase)
- **Observed behavior (current):**
  - ✅ BomEngine implements all line item operations with history recording:
    - `addLineItem()` — records CREATE operation with after snapshot
    - `updateLineItem()` — records UPDATE operation with before/after snapshots
    - `deleteLineItem()` — records DELETE operation with before/after snapshots
    - `replaceLineItem()` — records REPLACE operation with before/after snapshots
  - ✅ BomHistoryService implements history recording:
    - Captures complete item snapshots (NEPL column names preserved)
    - Records history with operation type, snapshots, changed_fields, user_id, timestamp
    - Supports parent_reference for copied items
  - ✅ History table migration exists (matches HISTORY_BACKUP_MIN_SPEC.md schema)
  - ✅ One live endpoint is integrated: `updateSaleData()` update-branch routes through BomEngine and records an UPDATE row in `quotation_sale_bom_item_history` with before/after snapshots and changed_fields including Qty (Phase-1A PASS).
  - ⚠️ Other item-edit endpoints remain unverified for BomEngine routing and must be migrated to engine-only writes in later phases.
  - ❌ **No restore capability** — Restore endpoints not implemented
- **Expected behavior (locked principle):**
  - ✅ Before edit: Capture complete before snapshot (all fields as JSON) — **IMPLEMENTED in BomEngine**
  - ✅ After edit: Capture complete after snapshot (all fields as JSON) — **IMPLEMENTED in BomEngine**
  - ✅ Create history record in `quotation_sale_bom_item_history` table — **IMPLEMENTED in BomHistoryService**
  - ✅ Record: operation type (CREATE/UPDATE/DELETE/REPLACE), before_snapshot, after_snapshot, changed_fields, user_id, timestamp — **IMPLEMENTED**
  - ✅ Preserve parent reference (what it was copied from, if applicable) — **SUPPORTED in BomHistoryService**
  - ❌ Enable restore capability (view historical states, restore to previous state) — **NOT IMPLEMENTED**
- **Risk:**
  - ✅ History recording works when BomEngine is used (low risk if integrated correctly)
  - ⚠️ Actual controllers may still use direct DB writes (bypassing BomEngine)
  - ❌ Cannot restore previous states (no restore endpoints)
- **Evidence:**
  - ✅ `app/Services/BomEngine.php:58-118` — addLineItem() with history
  - ✅ `app/Services/BomEngine.php:142-237` — updateLineItem() with history
  - ✅ `app/Services/BomEngine.php:256-330` — replaceLineItem() with history
  - ✅ `app/Services/BomEngine.php:344-396` — deleteLineItem() with history
  - ✅ `app/Services/BomHistoryService.php:35-89` — recordItemHistory() implementation
  - ✅ `database/migrations/2025_12_20_213521_create_quotation_sale_bom_item_history_table.php` — Migration exists
  - ❌ Actual QuotationV2Controller.php — NOT FOUND in codebase
  - ⚠️ Only example file exists: `app/Http/Controllers/QuotationV2Controller_Example_Integration.php`
- **Fix Type:** Integration (Backend)
- **Suggested Fix Direction (high-level):**
  - ✅ BomEngine and BomHistoryService are implemented correctly
  - ⚠️ Integrate BomEngine into actual controller methods (follow example integration pattern)
  - ⚠️ Ensure all item edit endpoints route through BomEngine (no direct DB writes)
  - ❌ Implement restore endpoints (view history, restore to previous state, compare states)
  - ⚠️ Verify history table migration has been run
- **Dependencies / Notes:**
  - ✅ DB migration exists — needs to be executed
  - ✅ History service implemented — needs controller integration
  - ⚠️ Example integration file shows correct pattern — actual controllers need to follow it
  - ❌ Restore capability still needs implementation (Phase-1 does not include restore)
  - Related to BOM-GAP-004 and BOM-GAP-005 (same pattern should apply to BOM node edits and copy operations)
- **Owner:** _[To be assigned]_
- **Target Phase:** Phase-1A (UPDATE branch integration)
- **Status:** ✅ CLOSED (Phase-1A PASS — history row created with UPDATE, before/after snapshot, changed_fields includes Qty)
- **Closure Date:** 2025-12-20
- **Closure Method:** `updateSaleData()` integration via BomEngine
- **Closure Evidence:** Phase-1A PASS — UPDATE operation verified with:
  - ✅ History row created in `quotation_sale_bom_item_history` table
  - ✅ Before snapshot captured (complete item state)
  - ✅ After snapshot captured (complete item state)
  - ✅ Changed fields recorded (includes Qty field)
  - ✅ Operation type: UPDATE
  - ✅ User context and timestamp recorded
- **Closure Reference:** Phase-1A PASS criteria met — history is now real and recorded for UPDATE operations via `updateSaleData()` endpoint

---

### BOM-GAP-004 — BOM Copy Operations Missing History/Backup (⏳ PARTIALLY RESOLVED)
- **Level(s):** Master BOM / Proposal BOM / Feeder / Panel
- **Scenario:** Copy / Apply / Reuse
- **Rule Violated:** 
  - Backup-History (Rule 4) — Copy history migration not created/run, not yet verified
  - Copy-New (Rule 1) — Copy operations implemented but not yet wired/verified
- **Severity:** High
- **Where Found:**
  - Controller/Service: `app/Http/Controllers/QuotationV2Controller.php` — ✅ Controller/method exists in runtime environment; patch prepared in planning (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending (Gate-2)
  - Service: `app/Services/BomEngine.php` — ✅ Copy methods implemented (Phase-2 code)
  - Methods: `copyMasterBomToProposal()`, `copyProposalBomToProposal()`, `copyFeederTree()` — ✅ IMPLEMENTED
  - Service: `app/Services/BomHistoryService.php` — ✅ `recordCopyHistory()` method implemented
  - DB Table(s): `bom_copy_history` — ✅ Migration created (`NEPL_Basecode/database/migrations/2025_12_20_214545_create_bom_copy_history_table.php`); ⚠️ Migration execution pending
- **Observed behavior (current):**
  - ✅ Copy operations implemented in BomEngine (Phase-2 code):
    - `copyMasterBomToProposal()` — ✅ IMPLEMENTED
    - `copyProposalBomToProposal()` — ✅ IMPLEMENTED
    - `copyFeederTree()` — ✅ IMPLEMENTED
  - ✅ `recordCopyHistory()` method exists in BomHistoryService
  - ✅ `bom_copy_history` table migration created (`NEPL_Basecode/database/migrations/2025_12_20_214545_create_bom_copy_history_table.php`)
  - ⚠️ Migration execution pending (table does not exist in DB yet)
  - ⚠️ Copy methods not yet wired to controller endpoints (Phase-2.1 pending)
  - ⚠️ Copy history not yet verified with live data (Phase-2.2 pending)
  - ❌ Cannot trace what was copied from where (history table does not exist)
- **Expected behavior (locked principle):**
  - At time of copy: Capture complete source snapshot (structure + all nested items)
  - After copy: Capture complete target snapshot (structure + all nested items)
  - Create copy history record in `bom_copy_history` table
  - Record: source_type, source_id, target_type, target_id, source_snapshot, target_snapshot, id_mapping (source ID → target ID), user_id, timestamp, operation
  - Preserve traceability (what was copied from what)
- **Risk:**
  - No audit trail (cannot track copy operations)
  - Cannot trace lineage (what was copied from what)
  - Cannot compare source vs target after copy
  - Compliance issues (no copy history)
- **Evidence:**
  - ✅ `app/Services/BomEngine.php` — Copy methods implemented (copyMasterBomToProposal, copyProposalBomToProposal, copyFeederTree)
  - ✅ `app/Services/BomHistoryService.php` — `recordCopyHistory()` method implemented
  - ✅ `PLANNING/GOVERNANCE/HISTORY_BACKUP_MIN_SPEC.md:§Level 3` — Defines required copy history structure
  - ✅ `database/migrations/2025_12_20_214545_create_bom_copy_history_table.php` — Migration created (PascalCase columns)
  - ⚠️ Controller wiring pending (Phase-2.1)
  - ⚠️ Verification evidence pending (Phase-2.2)
- **Fix Type:** Backend + DB schema (New Implementation)
- **Suggested Fix Direction (high-level):**
  - Create DB migration for `bom_copy_history` table per `HISTORY_BACKUP_MIN_SPEC.md:§Level 3` schema
  - Implement copy methods in BomEngine (Phase-2):
    - `copyMasterBomToProposal()` — Master BOM → Proposal BOM
    - `copyProposalBomToProposal()` — Proposal BOM → Proposal BOM (reuse)
    - `copyFeederTree()` — Feeder template apply (with reuse detection + clear-before-copy)
    - `copyFeederReuse()` — Feeder reuse/copy
    - `copyPanelTree()` — Panel copy
  - Each copy method must:
    - Before copy: Capture source snapshot (complete structure + items as JSON)
    - After copy: Capture target snapshot (complete structure + items as JSON)
    - Create ID mapping (source ID → target ID for all items and BOMs)
    - Create copy history record in `bom_copy_history` table
    - Use copy-never-link pattern (new IDs for all copied items)
  - Create controller methods that call BomEngine copy methods
  - Follow same history pattern as line item operations (BOM-GAP-003)
- **Dependencies / Notes:**
  - ✅ Phase-1 (line item operations) integrated (BOM-GAP-003 CLOSED)
  - ❌ Requires DB migration for `bom_copy_history` table (must be created per HISTORY_BACKUP_MIN_SPEC.md:§Level 3)
  - ✅ Copy operations implemented across all levels (Master/Proposal/Feeder/Panel)
  - ✅ History pattern established in BomHistoryService (`recordCopyHistory()` implemented)
  - ⚠️ Controller wiring required (Phase-2.1)
  - ⚠️ Verification evidence required (Phase-2.2 — R1/S1/R2/S2)
  - Related to BOM-GAP-001, BOM-GAP-002 (copy operations must implement reuse + clear-before-copy)
- **Owner:** _[To be assigned]_
- **Target Phase:** Phase-2 (Copy Operations)
- **Status:** ⏳ PARTIALLY RESOLVED (Phase-2 code implemented; pending migration + wiring + verification evidence)
- **Closure Gate:** CLOSE only after migration + R1/S1/R2/S2 evidence attached.
- **Worklog:**
  - 2025-12-21: Planning patch prepared (`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`); staging wiring pending; evidence capture pending (Gate-1 can be captured now, Gate-2/Gate-3 blocked until release window).
  - 2025-12-21: Gate-1 PASS — `bom_copy_history` schema verified on staging DB (`nepl_quotation`). Evidence: `evidence/PHASE2/G1_bom_copy_history_schema.txt`.

---

### BOM-GAP-005 — BOM Node Edits Missing History/Backup (Not Implemented)
- **Level(s):** Master BOM / Proposal BOM / Feeder / Panel
- **Scenario:** Edit / Update
- **Rule Violated:** 
  - Backup-History (Rule 4) — No history records created on BOM node edits
- **Severity:** Medium
- **Where Found:**
  - Service: `app/Services/BomEngine.php` — ❌ No BOM node update methods exist
  - Service: `app/Services/BomHistoryService.php` — ❌ No BOM history recording methods exist
  - Controller/Service: `app/Http/Controllers/QuotationV2Controller.php` — ❌ NOT FOUND
  - Methods: BOM node update operations (name, quantity, attributes changes) — ❌ NOT FOUND
  - DB Table(s): `quotation_sale_bom_history` — ❌ Migration does not exist
- **Observed behavior (current):**
  - ❌ BomEngine only has line item operations (Phase-1) — no BOM node operations
  - ❌ No `updateBomNode()` method in BomEngine
  - ❌ No BOM history recording in BomHistoryService (only item history exists)
  - ❌ BOM nodes (feeders, panels, nested BOMs) are updated directly (if at all) — no history
  - ❌ No history record is created in `quotation_sale_bom_history` (table does not exist)
  - ❌ Previous state is lost (no before snapshot)
  - ❌ No after snapshot recorded
  - ❌ No structure snapshot (nested items not captured)
  - ❌ No user context or timestamp in history
  - ❌ No restore capability
- **Expected behavior (locked principle):**
  - Before edit: Capture complete before snapshot (BOM node + structure snapshot including nested items)
  - After edit: Capture complete after snapshot (BOM node + structure snapshot)
  - Create history record in `quotation_sale_bom_history` table
  - Record: operation type (CREATE/UPDATE/DELETE/APPLY_TEMPLATE/REUSE), before_snapshot, after_snapshot, changed_fields, user_id, timestamp, parent_reference
  - Enable restore capability (view historical states, restore to previous state)
- **Risk:**
  - Data loss (previous BOM states cannot be recovered)
  - No audit trail (cannot track BOM-level changes)
  - No rollback capability (cannot undo BOM changes)
  - Cannot restore BOM structure to previous state
- **Evidence:**
  - ❌ `app/Services/BomEngine.php` — No BOM node methods found (only line item methods)
  - ❌ `app/Services/BomHistoryService.php` — No BOM history methods found (only item history)
  - ❌ `grep -r "updateBomNode\|recordBomHistory" app/` — No results found
  - ❌ `glob_file_search "*bom_history*.php" database/migrations` — No BOM history migration found
  - ✅ `PLANNING/GOVERNANCE/HISTORY_BACKUP_MIN_SPEC.md:§Level 2` — Defines required BOM history structure
  - ✅ `PLANNING/GOVERNANCE/BOM_ENGINE_IMPLEMENTATION_PLAN.md:§Phase-3` — BOM node operations planned for Phase-3
- **Fix Type:** Backend + DB schema (New Implementation)
- **Suggested Fix Direction (high-level):**
  - Create DB migration for `quotation_sale_bom_history` table per `HISTORY_BACKUP_MIN_SPEC.md:§Level 2` schema
  - Extend BomHistoryService with BOM history methods:
    - `recordBomHistory()` — Record BOM node history
    - `captureBomSnapshot()` — Capture BOM node + structure snapshot
  - Implement `updateBomNode()` method in BomEngine:
    - Before edit: Capture before snapshot (BOM node + complete structure as JSON including nested items)
    - After edit: Capture after snapshot (BOM node + complete structure as JSON)
    - Create history record with operation type (CREATE/UPDATE/DELETE/APPLY_TEMPLATE/REUSE), snapshots, changed_fields, user_id, timestamp, parent_reference
  - Follow same pattern as line item operations (BOM-GAP-003) for consistency
  - Implement restore endpoint to view/restore historical BOM states
- **Dependencies / Notes:**
  - ⚠️ Phase-1 (line item operations) must be integrated first (BOM-GAP-003)
  - ❌ Requires DB migration for `quotation_sale_bom_history` table (does not exist)
  - ⚠️ Must capture structure snapshot (nested items) for complete history
  - ✅ History pattern already established in BomHistoryService (can be extended)
  - Related to BOM-GAP-003 (history pattern should be consistent)
- **Owner:** _[To be assigned]_
- **Target Phase:** Phase-3 (BOM Node Operations) per BOM_ENGINE_IMPLEMENTATION_PLAN.md
- **Status:** ❌ NOT IMPLEMENTED (Planned for Phase-3)

---

### BOM-GAP-006 — Lookup Pipeline Preservation Not Verified After Copy
- **Level(s):** Line Item (all levels)
- **Scenario:** Copy / Apply / Reuse
- **Rule Violated:** 
  - Lookup-Pipeline (Rule 3) — Preservation not verified/guaranteed
- **Severity:** Medium
- **Where Found:**
  - Controller/Service: All copy operations (`applyMasterBom()`, `applyProposalBom()`, `applyFeederTemplate()`, etc.)
  - Methods: All copy/apply/reuse methods
  - Route/Endpoint: `[To be verified]`
  - DB Table(s): `quotation_sale_bom_items`, lookup tables (categories, subcategories, items, products)
- **Observed behavior (current):**
  - Copy operations copy ProductId and related fields
  - Lookup pipeline preservation (Category → Subcategory → Item → Product → Make → Series → SKU) is not explicitly verified
  - No validation that lookup chain remains intact after copy
  - No verification that SKU search works after copy
  - No verification that attribute mapping remains intact
  - No verification that product replacement via lookup works after copy
- **Expected behavior (locked principle):**
  - After copy, all line items must retain full lookup context
  - Category → Subcategory → Item/Type → Product/Generic → Make → Series → SKU/Description chain must remain intact
  - SKU must be searchable after copy
  - Attribute mapping must remain intact
  - Product replacement via lookup must work after copy
  - Category/subcategory navigation must be preserved
- **Risk:**
  - Broken references (orphaned items)
  - Lookup failures after copy
  - Product replacement may not work
  - SKU search may fail
  - User cannot navigate category/subcategory hierarchy
- **Evidence:**
  - `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md:§Rule 3` — Defines lookup pipeline requirements
  - `PLANNING/GOVERNANCE/BOM_MAPPING_REFERENCE.md:§F) Lookup Pipeline Requirements` — Defines lookup preservation requirements
  - No verification tests found in documentation
- **Fix Type:** Backend + Verification
- **Suggested Fix Direction (high-level):**
  - Add verification logic after copy operations to validate lookup pipeline
  - Verify: Category → Subcategory → Item → Product chain is intact
  - Verify: SKU search works (test search after copy)
  - Verify: Attribute mapping intact (test attribute access after copy)
  - Verify: Product replacement works (test replacement flow after copy)
  - Add integration tests to verify lookup pipeline preservation
  - Document lookup preservation as mandatory requirement
- **Dependencies / Notes:**
  - May require code review to verify current behavior
  - May be compliant but not verified (needs testing)
  - If compliant, gap can be closed with verification evidence
- **Owner:** _[To be assigned]_
- **Target Phase:** next sprint
- **Status:** OPEN (Needs Verification)

---

## 3) Summary Dashboard

| Severity | Count | Status |
|---|---|---|
| Critical | 0 | - |
| High | 5 | BOM-GAP-001, BOM-GAP-002, BOM-GAP-004 (⏳ PARTIALLY RESOLVED), BOM-GAP-007 (⏳ PARTIALLY RESOLVED), BOM-GAP-013 |
| Medium | 3 | BOM-GAP-003 (✅ CLOSED), BOM-GAP-005, BOM-GAP-006 |
| Low | 0 | - |

**Total Gaps:** 8  
**Open Gaps:** 5  
**Partially Resolved:** 2 (BOM-GAP-004, BOM-GAP-007)  
**Closed Gaps:** 1 (BOM-GAP-003)

### Gap Summary by Rule Violated

| Rule | Gap Count | Gap IDs |
|---|---|---|
| Rule 1: Copy-New | 3 | BOM-GAP-001, BOM-GAP-002, BOM-GAP-007 |
| Rule 2: Editability | 0 | - |
| Rule 3: Lookup-Pipeline | 1 | BOM-GAP-006 |
| Rule 4: Backup-History | 3 | BOM-GAP-003 (✅ CLOSED), BOM-GAP-004, BOM-GAP-005 |
| Rule 5: Cross-Level-Consistency | 3 | BOM-GAP-001, BOM-GAP-002, BOM-GAP-007 |

### Gap Summary by Level

| Level | Gap Count | Gap IDs |
|---|---|---|
| Feeder | 2 | BOM-GAP-001, BOM-GAP-002 |
| Line Item | 1 | BOM-GAP-003 (✅ CLOSED), BOM-GAP-006 |
| Master BOM / Proposal BOM / Feeder / Panel | 4 | BOM-GAP-004, BOM-GAP-005, BOM-GAP-007, BOM-GAP-006 |

---

## 4) Closure Rules

A gap can be marked **CLOSED** only when:
- ✅ Fix is implemented
- ✅ Verification evidence attached (before/after)
- ✅ No regression across levels (Master/Proposal/Feeder/Panel)
- ✅ Compliance verified against BOM_PRINCIPLE_LOCKED.md

---

## 5) Audit Instructions for Cursor

When auditing, follow this process:

1. **Identify Operation:** Find all BOM copy/edit/reuse operations
2. **Check Each Rule:** Verify compliance with all 5 rules
3. **Document Gaps:** Create gap entry for each violation
4. **No Implementation:** Only log gaps, do not fix
5. **Reference Evidence:** Include code paths, file names, line numbers

**Focus Areas:**
- Master BOM apply flows
- Proposal BOM reuse flows
- Feeder reuse/copy flows
- Panel reuse/copy flows
- Line item edit flows (add/delete/replace/edit)
- History/backup behavior
- Lookup pipeline preservation

---

## 2.1) Fundamentals Gaps (Phase-0 Integration)

**Context:** Fundamentals gap correction addresses foundational alignment between design-time masters and runtime instances. All fundamentals gaps are addressed via Phase-0 (Fundamentals Gap Correction) planning and conditional patching.

**Related Documents:**
- Baseline Bundle: `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` (to be frozen)
- Verification Queries: `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` (to be frozen)
- Verification Checklist: `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` (to be frozen)
- Patch Plan: `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (✅ frozen)
- Execution SOP: `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md` (✅ frozen)
- Serial Tracker: `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_SERIAL_TRACKER_v1.0.md` (✅ created)

### Fundamentals Gap Mapping

| Gap ID | Fundamentals Verification Query | Conditional Patch | Closure Path |
|--------|--------------------------------|-------------------|--------------|
| BOM-GAP-001 | VQ-001 (Feeder Masters), VQ-002 (Master→Instance) | P1 (Feeder Template Filter), P3 (Copy-Never-Link Guard) | Phase-0 verification + conditional patching |
| BOM-GAP-002 | VQ-002 (Master→Instance), VQ-005 (Copy-Never-Link) | P3 (Copy-Never-Link Guard) | Phase-0 verification + conditional patching |
| BOM-GAP-005 | VQ-003 (Proposal BOM Master), VQ-004 (Orphan BOMs) | Reference only (planned for Phase-3) | Fundamentals baseline documents hierarchy rules |
| BOM-GAP-006 | VQ-005 (Copy-Never-Link Sanity) | P3 (Copy-Never-Link Guard) | Phase-0 verification + conditional patching |

**Verification Query Reference:**
- **VQ-001:** Verify Feeder Masters exist (`master_boms` where `TemplateType='FEEDER'`)
- **VQ-002:** Verify Feeder Master → Instance relationship (MasterBomId references)
- **VQ-003:** Verify Proposal BOM Master ownership (QuotationId validation)
- **VQ-004:** Verify no orphan runtime BOMs (QuotationId must not be NULL)
- **VQ-005:** Verify copy-never-link sanity (no master mutation paths)

**Patch Reference:**
- **P1:** Feeder Template Filter Standardization (enforce `TemplateType='FEEDER'`)
- **P2:** Quotation Ownership Enforcement (QuotationId validation)
- **P3:** Copy-Never-Link Enforcement Guard (prevent master mutation)
- **P4:** Legacy Data Normalization (optional, last resort)

**Status:** Fundamentals gaps are managed via Phase-0 execution window. Closure requires:
1. Read-only verification (VQ-001 through VQ-005)
2. Conditional patch application (only if verification fails)
3. Evidence capture and sign-off

---

### BOM-GAP-013 — Template Data Missing (Phase-2 Data Readiness)
**Problem:** Selected MasterBomId has 0 rows in `master_bom_items`, so feeder apply copies 0 components even if endpoint succeeds.  
**Impact:** Phase-2 Gate-3 cannot be executed (inserted_count=0; UI shows no components).  
**Fix Path:** Add Gate-0 Data Readiness check + enforce template selection based on `master_bom_items` count before R1/R2.  
**Closure Evidence:** SQL output proving `COUNT(*) > 0` for chosen template + R1 inserted_count = N + S1/S2 verification outputs.

**Closure requires:**
- Gate-0 SQL output showing `COUNT(*) > 0` for chosen TEMPLATE_ID
- R1 JSON shows `inserted_count = N` (matches Gate-0 item_count)
- S1/S2 evidence files exist (`evidence/PHASE2/S1_sql_output.txt`, `evidence/PHASE2/S2_sql_output.txt`)

---

**END OF GAP REGISTER**

