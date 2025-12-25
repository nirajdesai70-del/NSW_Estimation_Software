# Phase-3 Planning Pack (v1.0)

**Project:** NSW Estimation Software  
**Phase:** Phase-3  
**Name:** BOM Node History & Restore  
**Mode:** 📋 PLANNING ONLY  
**Execution:** Deferred (separate approval required)  
**Date:** 2025-12-22  

---

## 1️⃣ Phase-3 Objective (Why this phase exists)

Phase-3 introduces history + restore at BOM-node level, not line items.

This enables:
- Undo / restore of structural BOM changes
- Audit-safe recovery
- Confidence in complex edits (rename, qty change, hierarchy changes)

**Phase-1** handled line item history  
**Phase-3** handles BOM node history

---

## 2️⃣ What is a "BOM Node" (Canonical)

A BOM Node is any structural entity above line items:

| Node Type | Examples |
|-----------|----------|
| Feeder BOM | Feeder name, qty, parent |
| Panel BOM | Panel-level BOM |
| Proposal BOM | Structural grouping |
| Any Level-0 / Level-1 BOM | Tree nodes |

### NOT included in Phase-3:
- ❌ Line item add/edit/delete (already Phase-1)
- ❌ Pricing logic
- ❌ Copy/apply logic (Phase-2)

---

## 3️⃣ Operations Covered in Phase-3

Phase-3 captures history for structural changes only:

| Operation | Included |
|-----------|----------|
| Rename BOM node | ✅ |
| Update feeder quantity | ✅ |
| Change parent / hierarchy | ✅ |
| Soft-delete BOM node | ✅ |
| Restore BOM node | ✅ |
| Compare versions | ✅ |

---

## 4️⃣ Core Design Principle (LOCKED)

Every BOM node change must be:
- captured before change
- captured after change
- restorable
- auditable

**No direct updates without history.**

---

## 5️⃣ Phase-3 Architecture (High-Level)

### New Concepts (Planning)

1. **BOM Node History**
   - Independent of line item history
   - Snapshot-based (structure + metadata)

2. **Restore Engine**
   - Restore a BOM node to a previous version
   - Cascade restore if hierarchy changed

---

## 6️⃣ Planned Data Model (Conceptual)

**Table:** `quotation_sale_bom_node_history` (NEW – planned)

| Field | Description |
|-------|-------------|
| HistoryId | Primary key |
| QuotationSaleBomId | Node being changed |
| QuotationId | Parent quotation |
| OperationType | Event type (RENAME, QTY_CHANGE, REPARENT, etc.) |
| BeforeSnapshot | JSON structure before change |
| AfterSnapshot | JSON structure after change |
| ChangedFields | JSON array of changed field names |
| ParentReference | Hierarchy context |
| CreatedBy | User who made change |
| CreatedAt | Timestamp |

⚠️ **Planning only** — no migration created yet

**See:** `03_SCHEMA_NODE_HISTORY.md` for detailed schema design.

---

## 7️⃣ Snapshot Strategy

### Before Snapshot captures:
- BOM node fields (name, qty, parent, level)
- Children relationships (IDs only)
- Metadata

### After Snapshot captures:
- Same structure post-change

**Snapshots are structural, not line-item deep.**

---

## 8️⃣ Restore Semantics

Restore works as:
1. Select HistoryId (or timestamp)
2. Load BeforeSnapshot
3. Apply snapshot back to BOM node
4. Record restore action as new history entry

**Restore is not destructive** — it is another version.

---

## 9️⃣ Verification Strategy (Planning)

Phase-3 execution will validate:

| Check | Purpose |
|-------|---------|
| History row created | No blind updates |
| Before/After snapshots differ | Change captured |
| Restore recreates old state | Restore correctness |
| New history on restore | Audit continuity |

---

## 🔍 Phase-3 Verification Queries (Planned)

### Examples (planning):

```sql
-- Verify history creation
SELECT COUNT(*) 
FROM quotation_sale_bom_node_history
WHERE QuotationSaleBomId = <ID>;

-- Verify event sequence
SELECT OperationType, CreatedAt 
FROM quotation_sale_bom_node_history
WHERE QuotationSaleBomId = <ID>
ORDER BY CreatedAt DESC;

-- Verify restore correctness
SELECT BeforeSnapshot, AfterSnapshot
FROM quotation_sale_bom_node_history
WHERE BomNodeHistoryId = <RESTORE_TARGET_ID>;
```

**See:** `05_VERIFICATION/NODE_HISTORY_VERIFICATION.sql` and `RESTORE_VERIFICATION.sql` for complete verification queries.

---

## 10️⃣ Evidence Structure (Future Execution)

```
evidence/PHASE3/phase3_window_YYYYMMDD/
├── preflight/
│   ├── gate0_itemcount.txt
│   └── initial_state.sql
├── execution/
│   ├── rename_node.json
│   ├── qty_update.json
│   ├── reparent_node.json
│   └── restore_operation.json
├── verification/
│   ├── history_created.txt
│   ├── restore_result.txt
│   └── audit_continuity_check.txt
└── summary/
    └── PHASE3_EXECUTION_SUMMARY.md
```

---

## 11️⃣ Entry / Exit Criteria (Planning)

### Entry Criteria
- ✅ Phase-0 COMPLETE
- ✅ Phase-1 COMPLETE
- ✅ Phase-2 planning COMPLETE
- ⏳ Phase-3 approval signed

### Exit Criteria
- ⏳ BOM node history captured
- ⏳ Restore proven
- ⏳ No regression to Phase-1 logic

---

## 12️⃣ Phase-3 Risks & Controls

| Risk | Control |
|------|---------|
| Large snapshot size | Structural snapshot only (not line-item deep) |
| Partial restore | Cascade logic clearly defined |
| History spam | Only structural ops logged (not every attribute change) |

---

## 13️⃣ Phase-3 Status

**Phase-3 planning is IN PROGRESS.**  
**No execution permitted until approval.**

### Planning Completion Checklist

- [x] ✅ Event model defined (`02_EVENT_MODEL.md`)
- [x] ✅ History table schema designed (`03_SCHEMA_NODE_HISTORY.md`)
- [x] ✅ Restore semantics documented (`04_BOMENGINE_NODE_OPS_CONTRACT.md`)
- [x] ✅ BomEngine methods designed (`04_BOMENGINE_NODE_OPS_CONTRACT.md`)
- [x] ✅ Verification SQL queries created (`05_VERIFICATION/`)
- [x] ✅ Release pack structure created (this pack)
- [x] ✅ Runbook and status tracking created (`00_README_RUNBOOK.md`, `STATUS.md`)
- [x] ✅ Architecture decisions documented (`01_ARCH_DECISIONS.md`)
- [x] ✅ Gap mapping completed (`00_SCOPE_LOCK.md`)
- [ ] ⏳ Phase-3 marked READY in master index (pending final review)

---

## 14️⃣ What is NOT done in Phase-3

- ❌ Line item history (already done in Phase-1)
- ❌ Feeder apply logic (Phase-2)
- ❌ Template copy logic (Phase-2)
- ❌ Pricing or calculations
- ❌ Hard deletes (only soft-delete via DEACTIVATED event)
- ❌ Bulk operations (one event per node)
- ❌ Periodic snapshots (delta-based only)

---

## ✅ Phase-3 Planning Summary

- ✅ Phase-3 is independent of Phase-2 execution
- ✅ Planning can proceed fully
- ✅ Execution will be clean, reversible, auditable
- ✅ No overlap or confusion with earlier phases

---

## 📋 Related Documents

### Canonical Release Pack
```
PLANNING/RELEASE_PACKS/PHASE3/
├─ 00_README_RUNBOOK.md - Execution guide
├─ 00_SCOPE_LOCK.md - Scope boundaries
├─ STATUS.md - Current status and gates
├─ 01_ARCH_DECISIONS.md - ADRs
├─ 02_EVENT_MODEL.md - Event types and semantics
├─ 03_SCHEMA_NODE_HISTORY.md - Table schema design
├─ 04_BOMENGINE_NODE_OPS_CONTRACT.md - Method contracts
├─ 05_VERIFICATION/ - Verification SQL
│  ├─ NODE_HISTORY_VERIFICATION.sql
│  └─ RESTORE_VERIFICATION.sql
├─ 06_RISKS_AND_ROLLBACK.md - Risk assessment
└─ PHASE3_PLANNING_PACK_V1.0.md - This document
```

### Cross-References
- **Master Plan:** `PLANNING/MASTER_PLANNING_INDEX.md`
- **Phase-1:** History foundation (line items)
- **Phase-2:** Feeder template apply (copy history)
- **Phase-4:** Lookup pipeline verification (future)
- **Phase-5:** System-wide audit (future)

---

## 🔜 Next Steps

1. **Complete Planning Review** - Final alignment check
2. **Register in Master Index** - Update `MASTER_PLANNING_INDEX.md` with Phase-3 READY status
3. **Generate Approval Pack** - Create execution approval documents (when ready)
4. **Execution Window** - Await approval for implementation

---

**END OF PHASE-3 PLANNING PACK V1.0**

