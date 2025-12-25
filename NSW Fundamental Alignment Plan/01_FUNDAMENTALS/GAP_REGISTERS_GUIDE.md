# Gap Registers Guide — How to Use Gap Registers

**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** 📋 PLANNING MODE ONLY  
**Purpose:** Explain gap registers, their purpose, status fields, update procedures, and layer mapping

---

## What Are Gap Registers?

Gap registers are working documents that track identified gaps, violations, or missing implementations in the NSW Estimation Software. They serve as:

- **Audit output:** Gaps identified during code audits or design reviews
- **Execution drivers:** Gaps that drive implementation work
- **Status tracking:** Track gap status from OPEN → PARTIALLY RESOLVED → CLOSED
- **Evidence requirements:** Define what evidence is needed to close gaps

**Rule:** Gap registers log gaps only (do not implement here). Implementation happens in separate execution windows.

---

## Gap Register Files

### 1. BOM Gap Register (Primary)

**File:** `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`

**Status:** PRIMARY — EXECUTION DRIVER

**Purpose:** Tracks BOM-related gaps across all levels (Master BOM, Proposal BOM, Feeder, Panel, Line Item)

**Scope:**
- Copy operations (BOM-GAP-001, BOM-GAP-002, BOM-GAP-004, BOM-GAP-007)
- History/backup (BOM-GAP-003, BOM-GAP-004, BOM-GAP-005)
- Lookup pipeline (BOM-GAP-006)
- Template data (BOM-GAP-013)
- Fundamentals gaps (BOM-GAP-001, BOM-GAP-002, BOM-GAP-005, BOM-GAP-006)

**Gap IDs:**
- BOM-GAP-001: Feeder Template Apply Creates New Feeder Every Time (No Reuse Detection) — OPEN
- BOM-GAP-002: Feeder Template Apply Missing Clear-Before-Copy (Duplicate Stacking) — OPEN
- BOM-GAP-003: Line Item Edits Missing History/Backup — ✅ CLOSED
- BOM-GAP-004: BOM Copy Operations Missing History/Backup — ⏳ PARTIALLY RESOLVED
- BOM-GAP-005: BOM Node Edits Missing History/Backup — ❌ NOT IMPLEMENTED
- BOM-GAP-006: Lookup Pipeline Preservation Not Verified After Copy — OPEN
- BOM-GAP-007: Copy Operations Not Implemented — ⏳ PARTIALLY RESOLVED
- BOM-GAP-013: Template Data Missing (Phase-2 Data Readiness) — OPEN

**Layer Mapping:**
- **Feeder:** BOM-GAP-001, BOM-GAP-002
- **Line Item:** BOM-GAP-003 (✅ CLOSED), BOM-GAP-006
- **Master BOM / Proposal BOM / Feeder / Panel:** BOM-GAP-004, BOM-GAP-005, BOM-GAP-007, BOM-GAP-006

---

### 2. Proposal BOM Gap Register

**File:** `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md`

**Status:** FROZEN — REFERENCE ONLY

**Purpose:** Tracks Proposal BOM-specific gaps (L2 layer, ProductType=2 enforcement)

**Scope:**
- ProductType=2 enforcement
- MakeId/SeriesId requirements
- Write gateway compliance
- Transitional state handling

**Gap IDs:**
- PB-GAP-001 through PB-GAP-004 (see gap register for details)

**Layer Mapping:**
- **Proposal BOM (L2):** All gaps in this register

---

### 3. Master BOM Gap Register

**File:** `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md`

**Status:** FROZEN — REFERENCE ONLY

**Purpose:** Tracks Master BOM-specific gaps (L1 layer, ProductType=1 enforcement)

**Scope:**
- L1-only enforcement (ProductType=1)
- Master BOM structure
- Master BOM → Proposal BOM copy operations

**Gap IDs:**
- MB-GAP-001 through MB-GAP-XXX (see gap register for details)

**Layer Mapping:**
- **Master BOM (L1):** All gaps in this register

---

### 4. Fundamentals Gap Correction TODO

**File:** `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_GAP_CORRECTION_TODO.md`

**Status:** ✅ COMPLETE (Phase-0 Execution Complete)

**Purpose:** Tracks fundamentals gap correction work (GAP-001, GAP-002, GAP-005, GAP-006)

**Scope:**
- Feeder Master definition
- Proposal BOM Master definition
- Canonical hierarchy
- Master→Instance mapping

**Gap IDs:**
- GAP-001: Feeder Template Apply Creates New Feeder Every Time — ✅ **DOC-CLOSED** (documentation frozen, runtime implementation pending)
- GAP-002: Feeder Template Apply Missing Clear-Before-Copy — ✅ **DOC-CLOSED** (documentation frozen, runtime implementation pending)
- GAP-005: BOM Node Edits Missing History/Backup — ✅ **DOC-CLOSED** (documentation frozen, runtime implementation pending)
- GAP-006: Lookup Pipeline Preservation Not Verified After Copy — ✅ **DOC-CLOSED** (documentation frozen, runtime verification pending)

**Layer Mapping:**
- **Feeder:** GAP-001, GAP-002
- **BOM Node:** GAP-005
- **Lookup Pipeline:** GAP-006

**Note:** Fundamentals gaps are managed via Phase-0 execution window. Closure requires verification + conditional patching.

---

### 5. Panel BOM Gap Documents

**Files:**
- `PLANNING/PANEL_BOM/GAP_CLOSURE_TEMPLATE.md` — Gap closure template
- `PLANNING/VERIFICATION/PB_GAP_004_*` — PB-GAP-004 verification documents

**Status:** PLANNING ONLY (Execution deferred)

**Purpose:** Tracks Panel BOM-specific gaps

**Scope:**
- Panel copy operations
- Panel instance isolation
- Panel BOM structure

**Gap IDs:**
- PB-GAP-004: Instance Isolation Verification (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PB_GAP_004_INSTANCE_ISOLATION_VERIFICATION_v1.0_2025-12-19.md`)

**Layer Mapping:**
- **Panel BOM:** All gaps in Panel BOM planning

---

## Status Fields

### Status Values

| Status | Meaning | Next Action |
|--------|---------|-------------|
| **OPEN** | Gap identified, not yet addressed | Plan implementation |
| **⏳ PARTIALLY RESOLVED** | Implementation started, verification pending | Complete implementation + verification evidence |
| **✅ DOC-CLOSED** | Documentation/spec frozen; planning complete; no runtime validation | No action needed (documentation only) |
| **✅ RUN-CLOSED** | Verified via SQL/API requests + evidence archive; runtime validated | No action needed (runtime verified) |
| **❌ NOT IMPLEMENTED** | Gap identified, implementation not started | Plan implementation |

**⚠️ CRITICAL:** Closure language must distinguish between documentation closure and runtime closure. See [PATCH_APPENDIX_v1.1.md](./PATCH_APPENDIX_v1.1.md) for details.

### Status Transitions

```
OPEN → ⏳ PARTIALLY RESOLVED → ✅ RUN-CLOSED
  ↓
❌ NOT IMPLEMENTED → OPEN → ⏳ PARTIALLY RESOLVED → ✅ RUN-CLOSED

Documentation Path:
OPEN → ✅ DOC-CLOSED (documentation frozen, no runtime validation)
```

**Rules:**
- Gap can be marked **DOC-CLOSED** when:
  - ✅ Documentation/spec frozen
  - ✅ Planning complete
  - ⚠️ No runtime validation required

- Gap can be marked **RUN-CLOSED** only when:
  - ✅ Fix is implemented
  - ✅ Verification evidence attached (before/after)
  - ✅ Runtime validation passed (SQL/API evidence)
  - ✅ No regression across levels (Master/Proposal/Feeder/Panel)
  - ✅ Compliance verified against locked principles

---

## How to Interpret Status Fields

### PENDING
- Gap identified, planning in progress
- No implementation started

### READY
- Planning complete, ready for implementation
- Implementation can begin

### PASS
- Verification passed
- Evidence captured
- Gap can be closed

### CLOSED
- Gap resolved
- Evidence attached
- No further action needed

### PARTIALLY RESOLVED
- Implementation started (code exists)
- Verification evidence pending
- Closure blocked until evidence attached

**Example:** BOM-GAP-004 (BOM Copy Operations Missing History/Backup)
- Status: ⏳ PARTIALLY RESOLVED
- Reason: Copy methods implemented in BomEngine, but migration + wiring + verification evidence pending
- Closure Gate: CLOSE only after migration + R1/S1/R2/S2 evidence attached

---

## How to Update Gap Registers

### During Execution Windows

1. **Before Execution:**
   - Review gap register
   - Identify gaps to address
   - Plan implementation approach

2. **During Execution:**
   - Update worklog with progress
   - Record evidence as it's captured
   - Update status when milestones reached

3. **After Execution:**
   - Attach verification evidence
   - Update status to CLOSED (if all criteria met)
   - Update closure date and method

### Update Format

**Worklog Entry:**
```
- YYYY-MM-DD: Description of work done. Evidence: `path/to/evidence/file.txt`
```

**Status Update:**
```
- **Status:** ⏳ PARTIALLY RESOLVED (Implementation complete; verification evidence pending)
- **Closure Gate:** CLOSE only after [specific evidence requirements]
```

**Closure Entry:**
```
- **Status:** ✅ CLOSED
- **Closure Date:** YYYY-MM-DD
- **Closure Method:** Description of how gap was closed
- **Closure Evidence:** `path/to/evidence/file.txt`
```

### Update Rules

1. **No Implementation in Gap Register:** Gap registers log gaps only, do not implement here
2. **Evidence Required:** All status updates must reference evidence files
3. **Closure Criteria:** Gap can be closed only when all closure criteria met
4. **Cross-Reference:** Update related gap registers if gap affects multiple layers

---

## Layer Mapping

### Which Gaps Belong to Which Layer?

| Layer | Gap Register | Gap IDs |
|-------|--------------|---------|
| **Category/Subcategory/Item** | NEPL Governance Checklist | Category/Subcategory/Item compliance gaps |
| **Generic Item Master (L0/L1)** | Generic Item Master Review | Generic Item Master gaps |
| **Specific Item Master (L2)** | Specific Item Master Review | Specific Item Master gaps |
| **Master BOM (L1)** | Master BOM Gap Register | MB-GAP-001, MB-GAP-002, etc. |
| **Proposal BOM (L2)** | Proposal BOM Gap Register | PB-GAP-001, PB-GAP-002, PB-GAP-003, PB-GAP-004 |
| **Feeder BOM** | BOM Gap Register | BOM-GAP-001, BOM-GAP-002 |
| **Panel BOM** | Panel BOM Planning | PB-GAP-004 (instance isolation) |
| **Line Item** | BOM Gap Register | BOM-GAP-003 (✅ CLOSED), BOM-GAP-006 |
| **Copy Operations** | BOM Gap Register | BOM-GAP-001, BOM-GAP-002, BOM-GAP-004, BOM-GAP-007 |
| **History/Backup** | BOM Gap Register | BOM-GAP-003 (✅ CLOSED), BOM-GAP-004, BOM-GAP-005 |

---

## Gap Register Cross-References

### Fundamentals Gaps → BOM Gaps

**Fundamentals gaps are tracked in:**
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_GAP_CORRECTION_TODO.md` (✅ COMPLETE)
- `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` (Section 2.1: Fundamentals Gaps)

**Mapping:**
- GAP-001 → BOM-GAP-001 (Feeder reuse detection)
- GAP-002 → BOM-GAP-002 (Clear-before-copy)
- GAP-005 → BOM-GAP-005 (BOM node history)
- GAP-006 → BOM-GAP-006 (Lookup pipeline)

### Proposal BOM Gaps → Resolution-B

**Proposal BOM gaps related to Resolution-B:**
- PB-GAP-001: ProductType=2 enforcement (Resolution-B rules)
- PB-GAP-002: MakeId/SeriesId requirements (Resolution-B rules)
- PB-GAP-003: Write gateway compliance (Resolution-B rules)

**Reference:** `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md`

---

## Gap Register Maintenance

### Regular Review

- Review gap registers during planning phases
- Update status as implementation progresses
- Close gaps when all criteria met

### Evidence Archive

- All gap closure evidence must be archived
- Evidence location: `evidence/` directory structure
- Evidence format: SQL output, JSON responses, verification checklists

### Cross-Reference Updates

- Update related gap registers when gap affects multiple layers
- Maintain consistency across gap registers
- Document dependencies between gaps

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial gap registers guide created from repository content |
| v1.1 | 2025-12-XX | Added DOC-CLOSED vs RUN-CLOSED distinction, date corrections |

---

**END OF GAP REGISTERS GUIDE**

