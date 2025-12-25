# Phase-4 Release Runbook

**Phase:** Lookup Pipeline Verification  
**Status:** 📋 PLANNING (Day-1 in progress)  
**Date Created:** 2025-12-21

---

## Overview

Phase-4 ensures lookup pipeline integrity after any copy/reuse/edit so that BOM line items remain fully editable with full master-data lookup preserved.

---

## Release Pack Contents

- `00_README_RUNBOOK.md` - This file (execution guide)
- `STATUS.md` - Current status and gate tracking
- `01_SCOPE_LOCK.md` - Scope boundaries (what IS / IS NOT covered)
- `02_LOOKUP_INTEGRITY_RULES.md` - Lookup pipeline integrity rules and enforcement
- `03_SCHEMA_OPTIONAL_AUDIT_TABLE.md` - Optional audit table schema (planning only)
- `04_VERIFICATION/` - Verification SQL queries
  - `LOOKUP_INTEGRITY_VERIFICATION.sql` - Lookup pipeline integrity verification queries
- `05_FAILURE_MODES_AND_REPAIR.md` - Failure modes and repair procedures
- `06_RISKS_AND_ROLLBACK.md` - Risk assessment and rollback procedures

---

## Execution Gates

### Gate-1: Planning Completeness
- [ ] Scope lock complete
- [ ] Lookup integrity rules defined
- [ ] Verification SQL drafted
- [ ] Failure modes and repair procedures documented
- [ ] Runbook and status tracking complete

### Gate-2: Implementation Window
- [ ] Verification procedures implemented
- [ ] Repair scripts ready (if needed)
- [ ] Integration tests pass

### Gate-3: Verification
- [ ] Lookup integrity verification passes
- [ ] Failure mode testing complete
- [ ] System-wide verification complete

---

## Execution Sequence

(TBD - to be populated during Day-2 planning)

---

## Pipeline to Protect

**Category → SubCategory → Item/Type → Generic/Product → Make → Series → SKU/Description**

This pipeline must remain intact after any copy/reuse/edit operation to ensure line items remain fully editable with lookup preserved.

---

END

