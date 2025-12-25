# Phase 5 Master Alignment Document

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
This document provides the complete alignment between:
1. Existing Phase 5 files and work
2. New Master Plan structure (7 phases)
3. Senate folder organization
4. Traceability and verification processes

## Source of Truth
- **Canonical:** This is the authoritative alignment document

---

## Executive Summary

### What We Have
- 20 existing Phase 5 documents covering scope, execution, freeze gates, and policies
- Clear Phase 5 scope: Step 1 (Data Dictionary) + Step 2 (Schema Design)
- Integration guide mapping pending upgrades to Phase 5 steps
- Freeze gate checklist for verification

### What We Need
- Organized senate structure for canonical truth
- Complete traceability from requirements to deliverables
- Legacy review framework (read-only reference)
- Freeze evidence documentation

### How They Align
- **Master Plan P1 + P2** = **Phase 5 Step 1 + Step 2**
- **Master Plan P5** = Post-implementation QA (different from our Phase 5)
- **Senate Structure** = Organized canonical workspace
- **Traceability** = Ensures nothing is missed

---

## Master Plan Alignment

### Phase Mapping

| Master Plan Phase | Purpose | Duration | Our Phase 5 Equivalent |
|------------------|---------|----------|----------------------|
| **P0** | Readiness & Governance | 1 week | ✅ Already complete (scope fence, readiness) |
| **P1** | Canonical Data Dictionary | 2-3 weeks | ✅ **Phase 5 Step 1** |
| **P2** | Canonical Schema Design | 2-3 weeks | ✅ **Phase 5 Step 2** |
| P3 | Backend Core Build | 5-6 weeks | ❌ Post-Phase 5 |
| P4 | Frontend UI Build | 4-5 weeks | ❌ Post-Phase 5 |
| **P5** | System Integration & QA | 3-4 weeks | ❌ Post-Phase 5 (different from our Phase 5) |
| P6 | Production Rollout | 2-3 weeks | ❌ Post-Phase 5 |

**Key Insight:** Our Phase 5 aligns with Master Plan P1 + P2. Master Plan P5 is implementation QA, not our analysis phase.

---

## Senate Structure Alignment

### Folder Purpose Mapping

| Senate Folder | Purpose | Contains | Status |
|---------------|---------|----------|--------|
| `00_GOVERNANCE/` | Phase 5 governance, scope, decisions | Charter, scope fence, decisions, risks | ✅ Created |
| `01_REFERENCE/` | Legacy review & TfNSW context | Read-only reference materials | ⏳ Placeholders needed |
| `02_FREEZE_GATE/` | Freeze verification & evidence | Checklist, pending upgrades, evidence | ✅ Partially created |
| `03_DATA_DICTIONARY/` | Step 1 outputs (FROZEN) | Data dictionary, guardrails, rules | ⏳ Step 1 outputs |
| `04_SCHEMA_CANON/` | Step 2 outputs (FROZEN) | Schema canon, ERD, table inventory | ⏳ Step 2 outputs |
| `05_TRACEABILITY/` | Requirement traceability | Requirement trace, file mapping | ✅ Created |
| `06_IMPLEMENTATION_REFERENCE/` | Post-Phase 5 planning | API design, UI wireframes, CI/CD | ⏳ Placeholders needed |
| `99_ARCHIVE/` | Superseded documents | Old README, drafts | ⏳ Placeholders needed |

---

## Existing File Alignment

### Governance Files → `00_GOVERNANCE/`

| Existing File | Senate Location | Purpose | Action |
|--------------|----------------|---------|--------|
| `PHASE_5_SCOPE_FENCE.md` | `00_GOVERNANCE/PHASE_5_SCOPE_FENCE.md` | Scope definition | ✅ Move |
| `PHASE_5_EXECUTION_SUMMARY.md` | `00_GOVERNANCE/PHASE_5_EXECUTION_SUMMARY.md` | Execution plan | ✅ Move |
| `PHASE_5_READINESS_PACKAGE.md` | `00_GOVERNANCE/PHASE_5_READINESS_PACKAGE.md` | Readiness review | ✅ Move |
| `LEGACY_VS_NSW_COEXISTENCE_POLICY.md` | `00_GOVERNANCE/LEGACY_VS_NSW_COEXISTENCE_POLICY.md` | Coexistence policy | ✅ Move |
| `NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md` | `00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md` | Master data governance | ✅ Move |
| `ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` | `00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` | ADR | ✅ Move |

### Freeze Gate Files → `02_FREEZE_GATE/`

| Existing File | Senate Location | Purpose | Action |
|--------------|----------------|---------|--------|
| `SPEC_5_FREEZE_GATE_CHECKLIST.md` | `02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` | Freeze verification | ✅ Move |
| `SPEC_5_FREEZE_RECOMMENDATIONS.md` | `02_FREEZE_GATE/SPEC_5_FREEZE_RECOMMENDATIONS.md` | Freeze recommendations | ✅ Move |
| `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` | `02_FREEZE_GATE/PHASE_5_PENDING_UPGRADES_INTEGRATION.md` | Integration guide | ✅ Move |

### Reference Files → `01_REFERENCE/`

| Existing File | Senate Location | Purpose | Action |
|--------------|----------------|---------|--------|
| `NEPL_TO_NSW_EXTRACTION.md` | `01_REFERENCE/LEGACY_REVIEW/NEPL_TO_NSW_EXTRACTION.md` | Legacy extraction | ✅ Move |
| `NISH_PENDING_WORK_EXTRACTED.md` | `01_REFERENCE/LEGACY_REVIEW/NISH_PENDING_WORK_EXTRACTED.md` | Legacy work notes | ✅ Move |

### Implementation Reference → `06_IMPLEMENTATION_REFERENCE/`

| Existing File | Senate Location | Purpose | Action |
|--------------|----------------|---------|--------|
| `SPEC_5_REVIEW_AND_WORKING_DRAFT.md` | `06_IMPLEMENTATION_REFERENCE/SPEC_5_REVIEW_AND_WORKING_DRAFT.md` | SPEC-5 review | ✅ Move |
| `POST_PHASE_5_IMPLEMENTATION_ROADMAP.md` | `06_IMPLEMENTATION_REFERENCE/POST_PHASE_5_IMPLEMENTATION_ROADMAP.md` | Post-Phase 5 roadmap | ✅ Move |

### Archive → `99_ARCHIVE/`

| Existing File | Senate Location | Purpose | Action |
|--------------|----------------|---------|--------|
| `README.md` | `99_ARCHIVE/DRAFTS/README.md` | Old README (superseded) | ✅ Archive |
| `QUICK_REFERENCE.md` | `99_ARCHIVE/DRAFTS/QUICK_REFERENCE.md` | Quick reference (draft) | ✅ Archive |

---

## Process Alignment

### Phase 5 Execution Process

```
1. Governance (P0 equivalent) ✅ COMPLETE
   └─> Scope fence, readiness, decisions

2. Step 1: Data Dictionary (P1 equivalent) ⏳ PENDING
   └─> Use: Pending Upgrades Integration Guide
   └─> Output: 03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md (FROZEN)
   └─> Verify: Freeze Gate Checklist

3. Step 2: Schema Design (P2 equivalent) ⏳ PENDING
   └─> Use: Data Dictionary + Pending Upgrades Integration Guide
   └─> Output: 04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md (FROZEN)
   └─> Verify: Freeze Gate Checklist + Evidence

4. Freeze Gate ⏳ PENDING
   └─> Complete: Freeze Gate Checklist
   └─> Document: Freeze Evidence
   └─> Approve: Governance sign-off

5. Post-Phase 5 (P3-P6 equivalent) ❌ NOT IN PHASE 5
   └─> Use: Implementation Reference documents
```

### Traceability Process

```
Requirement → Source Document → Data Dictionary Section → Schema Table → Evidence
     ↓              ↓                    ↓                    ↓            ↓
   R-001    Pending Upgrades    QuotationSaleBom      quote_boms    Schema DDL
```

### Verification Process

```
1. Complete Requirement Trace Matrix
2. Map Files to Requirements (CSV)
3. Verify Freeze Gate Checklist
4. Document Freeze Evidence
5. Get Governance Approval
```

---

## Key Alignments

### 1. Scope Alignment ✅
- Phase 5 = Analysis only (Data Dictionary + Schema)
- No implementation, no legacy migration
- Aligned with Master Plan P1 + P2

### 2. Freeze Discipline Alignment ✅
- Freeze Gate Checklist ensures nothing missed
- Pending Upgrades Integration Guide maps requirements
- Freeze Evidence documents verification

### 3. Legacy Policy Alignment ✅
- `project/nish/` is read-only reference
- Legacy review documents "what not to do"
- Legacy-to-Canonical mapping tracks decisions

### 4. Traceability Alignment ✅
- Requirement Trace Matrix maps all requirements
- File-to-Requirement Map ensures coverage
- Evidence links requirements to deliverables

---

## Next Actions

### Immediate (Senate Setup)
1. ✅ Create senate folder structure
2. ✅ Create governance documents (charter, glossary, decisions, risks)
3. ✅ Create traceability documents
4. ⏳ Create placeholder files for missing documents
5. ⏳ Move existing files to senate locations

### Phase 5 Execution
1. ⏳ Complete Step 1: Data Dictionary (use Pending Upgrades Integration Guide)
2. ⏳ Complete Step 2: Schema Design (use Data Dictionary + Integration Guide)
3. ⏳ Complete Freeze Gate verification
4. ⏳ Document Freeze Evidence
5. ⏳ Get governance approval

---

## Change Log
- v1.0: Created master alignment document

