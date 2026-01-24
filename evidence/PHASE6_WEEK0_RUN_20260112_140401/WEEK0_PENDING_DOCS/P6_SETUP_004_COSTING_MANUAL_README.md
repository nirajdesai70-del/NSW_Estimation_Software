# Phase-6 Costing Manual — Structure Definition (Week-0)

**Phase:** Phase-6  
**Week:** Week-0  
**Document ID:** P6-SETUP-004  
**Version:** v1.0  
**Status:** ✅ COMPLETE (Structure Only)  
**Date:** 2026-01-12

---

## 1. Purpose

This directory defines the **documentation structure** for the Phase-6 Costing Manual.

**Week-0 Scope:**
- ✅ Directory structure definition
- ✅ Section intent descriptions
- ❌ No costing logic content
- ❌ No formulas, examples, or calculations
- ❌ No implementation guidance

Content will be authored during Phase-6 execution weeks, aligned to frozen contracts and Canon.

---

## 2. Governance & Authority

- **Schema Authority:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Contract Authority:**  
  `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
- **Gate Authority:**  
  `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`

This manual must not introduce schema meaning changes or contradict the QCD Contract.

---

## 3. Directory Structure & Intent

### `00_OVERVIEW/`
**Intent:** High-level explanation of the costing system.
- Audience: Business, QA, auditors
- No formulas; conceptual overview only

### `01_QCD_CONCEPTS/`
**Intent:** Explain QCD (Quotation Cost Detail) concepts.
- Inputs/outputs at a conceptual level
- Engine-first principle
- Determinism and auditability

### `02_COST_HEADS/`
**Intent:** Describe logical cost head/bucket concepts.
- Mapping to Canon concepts
- No table or column definitions

### `03_QUANTITY_LOGIC/`
**Intent:** Explain quantity derivation concepts.
- BOM → effective quantities (conceptual)
- No executable formulas in Week-0

### `04_ADDERS/`
**Intent:** Describe cost adders conceptually.
- Types, applicability, boundaries
- No rates or calculations in Week-0

### `05_EXAMPLES/`
**Intent:** Worked examples (added later).
- Placeholder only in Week-0

### `06_VALIDATION/`
**Intent:** Validation and reconciliation concepts.
- Engine vs spreadsheet reconciliation
- Audit checks and acceptance criteria

### `99_APPENDIX/`
**Intent:** Supporting references.
- Glossary
- Decision references
- Change logs

---

## 4. Authoring Rules (Mandatory)

- All content must:
  - Reference Schema Canon v1.0
  - Respect QCD Contract v1.0
  - Avoid duplicating Canon definitions
- No schema meaning changes allowed
- Any formula introduction requires governance approval

---

## 5. Week-0 Status

- Structure: ✅ DEFINED
- Content: ⏳ DEFERRED (Phase-6 execution weeks)

**P6-SETUP-004:** ✅ COMPLETE

---

## 6. Directory Creation

**Expected Structure:**
```
docs/PHASE_6/COSTING/MANUAL/
├── README.md (this file)
├── 00_OVERVIEW/
├── 01_QCD_CONCEPTS/
├── 02_COST_HEADS/
├── 03_QUANTITY_LOGIC/
├── 04_ADDERS/
├── 05_EXAMPLES/
├── 06_VALIDATION/
└── 99_APPENDIX/
```

**Note:** Directories will be created during Phase-6 execution weeks when content is authored.

---

## References

- **Schema Canon v1.0:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **QCD Contract v1.0:**  
  `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
- **D0 Gate Checklist:**  
  `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`
- **Phase-6 Task Register:**  
  `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`

---

**End of Document**
