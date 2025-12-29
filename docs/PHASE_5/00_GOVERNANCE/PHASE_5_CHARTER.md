---
Status: CANONICAL
Version: v1.0
Owner: Phase 5 Governance
Updated: 2025-12-27
Scope: Phase-5
---

# Phase 5 Charter - NSW Estimation Software Master Plan

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
This document establishes Phase 5 as the canonical definition phase for NSW Estimation Software, following the master execution plan structure.

## Source of Truth
- **Canonical:** This is the authoritative Phase 5 charter
- **Master Plan Reference:** Aligned with NSW Estimation Software Master Execution Plan
- **Fundamentals baseline:** see `FUNDAMENTALS_SOURCE_OF_TRUTH.md`
- **Fundamentals Alignment Plan register:** `01_REFERENCE/NSW_FUNDAMENTALS_ALIGNMENT_PLAN_REGISTER.md`

## Phase 5 Position in Master Plan

**Repo "Phase 5" (Canonical Design)** aligns to **Master Plan P1 + P2**.

**Master Plan P5 (System Integration & QA)** is a post-implementation phase and is tracked separately as "Post-Phase-5 QA".

### Master Plan Structure (Reference)

| Phase | Name | Purpose | Duration |
|-------|------|---------|----------|
| P0 | Readiness & Governance | Entry gate, scope lock | 1 week |
| **P1** | **Canonical Data Dictionary** | **Single source of truth** | **2-3 weeks** |
| **P2** | **Canonical Schema Design** | **DB + rules freeze** | **2-3 weeks** |
| P3 | Backend Core Build | Engine & APIs | 5-6 weeks |
| P4 | Frontend UI Build | Operator-facing system | 4-5 weeks |
| P5 | System Integration & QA | Stability + trust | 3-4 weeks |
| P6 | Production Rollout & Hardening | Go-live + scale | 2-3 weeks |

**Mapping:**
- **Repo Phase 5 (Step 1)** = Master Plan **P1** (Canonical Data Dictionary)
- **Repo Phase 5 (Step 2)** = Master Plan **P2** (Canonical Schema Design)
- **Master Plan P5** = Post-Phase-5 QA & Hardening (separate, post-implementation)

## Naming Policy

To prevent confusion:

- **Repo "PHASE_5"** = Canonical Design phase (Data Dictionary + Schema Design)
  - This is analysis/design only
  - Maps to Master Plan P1 + P2
  - Located in: `docs/PHASE_5/`

- **Master Plan "P5"** = System Integration & QA phase
  - This is post-implementation QA
  - Happens after backend/frontend are built
  - Tracked separately as "Post-Phase-5 QA"
  - Not the same as repo Phase 5

## Phase 5 Scope (Canonical)

### Step 1: Freeze NSW Canonical Data Dictionary
- Define entity semantics (Category/Subcategory/Type/Attribute, L0/L1/L2, etc.)
- Document business rules and constraints
- Establish naming conventions
- Output: `NSW_DATA_DICTIONARY_v1.0.md` (FROZEN)

### Step 2: Define NSW Canonical Schema (Design Only)
- Translate dictionary to table structure
- Define relationships and constraints
- Create ER diagram and table inventory
- Output: `NSW_SCHEMA_CANON_v1.0.md` + ERD

## Current Operating Mode

**Mode:** 🔓 OPEN_GATE_EXPLORATION (as of 2025-01-27)

Phase 5 currently operates in Exploration Mode with controlled decision capture. See `PHASE_5_MODE_POLICY.md` for details.

**Key Operating Rules:**
- Schema and rule changes require Decision Register entry FIRST
- All changes must be logged (Decision Register or Feature Discovery Log)
- Prerequisites are reference inputs, not blockers
- See `EXPLORATION_MODE_SETUP_SUMMARY.md` for complete setup details

## Critical Rules

1. **Three-Truth Model:**
   - Truth-A (Canonical): `docs/PHASE_5/` - Write only here
   - Truth-B (Legacy Reference): `project/nish/` - READ-ONLY
   - Truth-C (Implementation): Post-Phase 5 only

2. **Freeze Discipline:**
   - No UI before Schema Freeze
   - No schema change after Phase 2 without governance approval
   - No analytics/BI scope in Phase 5

3. **Primary Objective:**
   - Change / Variation Estimation (TfNSW-grade canonical system)

4. **UI Classification:**
   - Any UI built in existing NEPL app = **REFERENCE HARNESS ONLY** (validation/testing)
   - Phase-5 UI design = clean slate after Schema Freeze (future)
   - See `UI_CONTEXT_CLASSIFICATION.md` for complete policy

## Change Log
- v1.0: Created as part of Phase 5 Senate setup
- v1.1: Added UI classification reference (2025-01-27)

