# Phase-3 Release Runbook

**Phase:** BOM Node History & Restore  
**Status:** 📋 PLANNING (Day-2 in progress)  
**Date Created:** 2025-01-XX

---

## Overview

Phase-3 implements append-only event logging for BOM node operations, enabling point-in-time restore capabilities.

---

## Release Pack Contents

- `00_README_RUNBOOK.md` - This file (execution guide)
- `STATUS.md` - Current status and gate tracking
- `01_ARCH_DECISIONS.md` - Architecture decisions and rationale
- `02_EVENT_MODEL.md` - Event model (Day-1 snapshot, canonical)
- `03_SCHEMA_NODE_HISTORY.md` - Node history table schema design
- `04_BOMENGINE_NODE_OPS_CONTRACT.md` - BomEngine method contracts
- `05_VERIFICATION/` - Verification SQL queries
  - `NODE_HISTORY_VERIFICATION.sql` - Event insert verification
  - `RESTORE_VERIFICATION.sql` - Restore replay correctness
- `06_RISKS_AND_ROLLBACK.md` - Risk assessment and rollback procedures

---

## Execution Gates

### Gate-1: Planning Completeness
- [ ] Schema design complete
- [ ] BomEngine contracts defined
- [ ] Verification SQL drafted
- [ ] Runbook and status tracking complete

### Gate-2: Implementation Window
- [ ] Migration created
- [ ] BomEngine methods implemented
- [ ] Controller wiring complete

### Gate-3: Verification
- [ ] Event insert verification passes
- [ ] Restore replay verification passes
- [ ] Integration tests pass

---

## Execution Sequence

1. **Planning** (Day-1 + Day-2) - ✅ Day-1 Complete, 🔄 Day-2 In Progress
2. **Implementation Window** (after planning READY)
3. **Verification** (after implementation)
4. **Release** (after verification passes)

---

## Related Documents

- Master Plan: `PLANNING/RELEASE_PACKS/PHASES_3_4_5_MASTER_PLAN.md`
- Tracker: `PLANNING/RELEASE_PACKS/PHASES_3_4_5_TODO_TRACKER.md`
- Phase-2: `PLANNING/RELEASE_PACKS/PHASE2/`

---

**END OF RUNBOOK**

