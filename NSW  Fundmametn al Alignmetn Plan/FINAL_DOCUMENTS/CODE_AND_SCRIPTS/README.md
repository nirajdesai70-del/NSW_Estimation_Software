# Code and Scripts

**Purpose:** This folder contains all code files, scripts, and SQL files that implement or support the NSW Software upgrade.

---

## Folder Structure

```
CODE_AND_SCRIPTS/
├── PHP_SERVICES/ - Core BOM services
├── PHP_CONTROLLERS/ - Controller examples
├── PHP_MIGRATIONS/ - Database migrations
├── SQL_SCRIPTS/ - Verification and execution SQL
├── SHELL_SCRIPTS/ - Shell automation scripts
└── PYTHON_SCRIPTS/ - Python governance scripts
```

---

## PHP_SERVICES/ (2 files)

### Core BOM Implementation Services

1. **BomEngine.php**
   - **Purpose:** Centralized service for all BOM operations
   - **Enforces:** BOM principles (Copy→New Instance, Full Editability, Lookup Pipeline, Backup & History, Cross-Level Consistency)
   - **Phase:** Phase-1 (P0) - Line Item Edit + History Foundation
   - **Reference:** BOM_ENGINE_BLUEPRINT.md, BOM_ENGINE_IMPLEMENTATION_PLAN.md
   - **Uses:** NEPL column names (PascalCase)
   - **Status:** ✅ Core implementation

2. **BomHistoryService.php**
   - **Purpose:** History recording service for BOM operations
   - **Functionality:** Immutable history recording, copy-never-link pattern
   - **Phase:** Phase-1 foundation
   - **Status:** ✅ Core implementation

---

## PHP_CONTROLLERS/ (1 file)

1. **QuotationV2Controller_Example_Integration.php**
   - **Purpose:** Example controller showing BomEngine integration
   - **Use:** Reference for integrating BomEngine into controllers
   - **Status:** Example/Reference

---

## PHP_MIGRATIONS/ (2 files)

### Database Schema Migrations

1. **2025_01_XX_XXXXXX_create_quotation_sale_bom_item_history_table.php**
   - **Purpose:** Creates BOM item history table
   - **Phase:** Phase-1 foundation
   - **Status:** ✅ Migration ready

2. **2025_12_20_214545_create_bom_copy_history_table.php**
   - **Purpose:** Creates BOM copy history table
   - **Phase:** Phase-1 foundation
   - **Status:** ✅ Migration ready

---

## SQL_SCRIPTS/ (5 files)

### Verification and Execution SQL

1. **verify_phase1_bom_history_queries.sql**
   - **Purpose:** Phase 1 BOM history verification queries
   - **Use:** Verify history recording functionality

2. **S1_S2_VERIFICATION.sql**
   - **Purpose:** Phase 2 S1/S2 verification queries
   - **Use:** Verify feeder template apply functionality

3. **NODE_HISTORY_VERIFICATION.sql**
   - **Purpose:** Phase 3 node history verification
   - **Use:** Verify BOM node history recording

4. **RESTORE_VERIFICATION.sql**
   - **Purpose:** Phase 3 restore verification
   - **Use:** Verify restore functionality

5. **LOOKUP_INTEGRITY_VERIFICATION.sql**
   - **Purpose:** Phase 4 lookup integrity verification
   - **Use:** Verify lookup pipeline preservation

---

## SHELL_SCRIPTS/ (7 files)

### Automation and Verification Scripts

1. **verify_phase1_bom_history.sh**
   - **Purpose:** Verify Phase 1 BOM history implementation
   - **Use:** Run Phase 1 verification

2. **verify_feeder_apply_a3_a4.sh**
   - **Purpose:** Verify feeder apply operations (A3/A4)
   - **Use:** Run Phase 2 verification

3. **validate_phase4_gates.sh**
   - **Purpose:** Validate Phase 4 gates
   - **Use:** Run Phase 4 verification

4. **audit_live_nish_changes.sh**
   - **Purpose:** Audit live changes in nish workspace
   - **Use:** Monitor runtime changes

5. **generate_live_audit_report.sh**
   - **Purpose:** Generate live audit reports
   - **Use:** Create audit documentation

6. **resolution_b_audit.sh**
   - **Purpose:** Resolution B audit script
   - **Use:** Audit Resolution B compliance

7. **phase3_audit.sh**
   - **Purpose:** Phase 3 audit script
   - **Use:** Run Phase 3 audit

---

## PYTHON_SCRIPTS/ (8 files)

### Governance Automation Scripts

1. **kickoff_specific_r1.py**
   - **Purpose:** Kickoff Specific Item Master Round 1
   - **Use:** Automate R1 kickoff process

2. **validate_specific_r1_kickoff.py**
   - **Purpose:** Validate Specific Item Master R1 kickoff
   - **Use:** Validate kickoff requirements

3. **validate_final_freeze.py**
   - **Purpose:** Validate final freeze conditions
   - **Use:** Check freeze readiness

4. **trigger_freeze_if_r2_complete.py**
   - **Purpose:** Trigger freeze if R2 is complete
   - **Use:** Automate freeze process

5. **generate_signoff_sheet.py**
   - **Purpose:** Generate signoff sheets
   - **Use:** Create signoff documentation

6. **archive_artifacts.py**
   - **Purpose:** Archive governance artifacts
   - **Use:** Archive compliance records

7. **export_dashboard_to_csv.py**
   - **Purpose:** Export dashboard to CSV
   - **Use:** Export governance data

8. **trace_laravel_fields.py**
   - **Purpose:** Trace Laravel field mappings
   - **Use:** Verify field mappings in code

---

## Integration Notes

### For NSW Software Upgrade

1. **Start with Services:**
   - Review `PHP_SERVICES/BomEngine.php` for core BOM logic
   - Review `PHP_SERVICES/BomHistoryService.php` for history patterns

2. **Use Migrations:**
   - Apply migrations in order
   - Verify schema matches design documents

3. **Run Verification:**
   - Use SQL scripts to verify functionality
   - Use shell scripts for automated verification
   - Use Python scripts for governance automation

4. **Reference Examples:**
   - Use controller example for integration patterns
   - Follow NEPL column naming (PascalCase)

---

## File Count Summary

- **PHP Services:** 2 files
- **PHP Controllers:** 1 file
- **PHP Migrations:** 2 files
- **SQL Scripts:** 5 files
- **Shell Scripts:** 7 files
- **Python Scripts:** 8 files

**Total: 25 code/script files**

---

**Last Updated:** 2025-01-XX  
**Purpose:** Complete code and script collection for NSW Software upgrade

