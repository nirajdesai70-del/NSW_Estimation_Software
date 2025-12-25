# Master BOM — Gap Register (Round-1)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md  
**Version:** v1.1_20251219  
**Date (IST):** 2025-12-18  
**Status:** ⏳ **EVIDENCE-BASED (DB-PENDING)**

## ✅ Standard Remark: Evidence-Based Review (DB Pending)

**Remark (Scope & Evidence Tier):**  
This Master BOM review is executed using the authoritative Master BOM design pack (Index/Plan + Parts 1–11) and code references where available. The design pack is now **imported/registered into this repo workspace for evidence-path referencing** under `docs/MASTER_BOM/DESIGN/`, therefore Design Evidence is marked **VERIFIED**. Live database verification is not available as of **2025-12-18**, therefore all data-integrity outcomes that require runtime/DB proof are marked **DB-PENDING** and must be validated before any “final freeze” is treated as production-confirmed.

**Reminder (Mandatory DB Verification Later):**  
Before final acceptance / production freeze, execute the DB Verification Pack below and update this document’s DB axis from **DB-PENDING → VERIFIED**.

### ✅ DB-PENDING verification items (not counted as FAIL)
These items require DB/runtime access and must be verified later. Until then, track them here as **DB-PENDING** (not failures unless design/code evidence is wrong):

#### A) Schema & Keys
- Verify `master_boms`, `master_bom_items` schema and constraints match design

#### B) Resolution enforcement (CRITICAL)
- Verify `ResolutionStatus` in Master BOM items is only `L0`/`L1` (no `L2`)
- Verify `ProductId` remains `NULL` for Master BOM items where `ResolutionStatus` is `L0`/`L1` (B4 invariant)
- If any violation exists → raise **CRITICAL**, quarantine/fix data, and add a hard guard

#### C) Copy-Never-Link Independence (CRITICAL)
- Verify quotation/proposal BOM rows are copies (Master BOM edits do not mutate copied BOM rows)

#### D) Soft Delete (Archival)
- Verify deletes set `Status=1` and do not cascade into quotation/proposal BOM (note: code evidence suggests hard delete; see MB-GAP-004)

#### E) Pricing/SKU Non-Leakage at Master BOM stage
- Verify Master BOM stage does not join/resolve pricing/SKU tables (pricing allowed only after copy + Make/Series selection)

### Status wording (when DB is the only missing evidence)
If DB evidence is not available, but design/code evidence is complete, use:
**Status: ⏳ EVIDENCE-BASED (DB-PENDING)**

---

## Evidence Format (Mandatory)
Use one of:
- `Evidence: <file>:<section>`
- `Evidence: <file>:Lx–Ly` (if line references are available)

---

## 1) Executive Summary

This Gap Register records gaps discovered in Round‑0 readiness and Round‑1 execution, with DB/runtime-dependent verification items tracked as **DB-PENDING** until verified.

- Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§1`
- Evidence: `MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md:§0`

| Axis | Status | Meaning |
|---|---|---|
| Design Evidence | VERIFIED | Design pack registered under `docs/MASTER_BOM/DESIGN/` |
| Code Evidence | PARTIAL (EXTERNAL) | Code evidence captured from external Laravel path; not yet imported/registered into this workspace |
| DB Evidence | DB-PENDING | No DB access available today; runtime data integrity proof pending |

---

## 2) Gap Counts by Severity (current)

| Severity | Count |
|---|---:|
| CRITICAL | 0 |
| HIGH | 2 |
| MEDIUM | 0 |
| LOW | 0 |

---

## 3) Gaps (Readiness Blockers)

### MB-GAP-003 — Master BOM items force `ProductId = NULL` (descriptor/spec model) [L1 Layer]
- **Category**: Governance / Logic
- **Severity**: HIGH
- **Layer Label**: L1 (Master BOM operates at L1 layer)
- **Evidence**:
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L25–L49` (B4 rule: L0/L1 ⇒ ProductId must be NULL)
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L155–L166` (store path sets `ProductId => null`)
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L219–L247` (update path deletes existing items and re-inserts with `ProductId => null`)
- **Impact**:
  - Audit correctness — confirms Master BOM is currently an L1 template (descriptor/spec), not a "generic product list".
  - Prevents future drift where engineers attempt to enforce `ProductType=1` against a field that is intentionally `NULL`.
  - **L1 Layer Context:** Master BOM operates at L1 (Technical Variant, Make-agnostic). ProductId=NULL is by design for L1 spec templates. Generic products (ProductType=1) represent L0 or L1, but Master BOM items are L1 spec templates that reference these generics conceptually, not via direct ProductId linkage.
- **Fix Type**: Planned (not data-corrupting)
- **Recommendation**:
  - Update governed Master BOM docs to explicitly state: Master BOM items are L1 spec templates; `ProductId` is `NULL` by design (B4). Master BOM operates at L1 layer.
  - Align Round‑1 checks: L1→L2 resolution rule applies at quotation resolution stage (Proposal BOM), not at `MasterBomItem` storage stage.

### MB-GAP-004 — Master BOM uses hard delete (`delete()`), not soft delete (`Status=1` / `SoftDeletes`) [L1 Layer]
- **Category**: Governance / Service
- **Severity**: HIGH
- **Layer Label**: L1 (Master BOM governance at L1 layer)
- **Evidence**:
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L287–L299` (`destroy()` executes `delete()` for `MasterBom` and `MasterBomItem`)
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L219–L247` (update flow hard-deletes `MasterBomItem` rows before re-insert)
- **Impact**:
  - Violates archival/trace expectations (template history can vanish), increasing audit and investigation risk.
  - Update flow destroys item history (delete + re-insert), even when the Master BOM remains active.
- **Fix Type**: Planned (Immediate only if audit policy treats hard delete as critical)
- **Recommendation**:
  - Convert Master BOM delete to soft delete (choose one: `Status` flag or Laravel `SoftDeletes`).
  - Add a governed rule: if referenced by any quotation, mark inactive; do not delete.
  - Add verification SQL (DB-PENDING) to confirm no unexpected cascades.

---

## 4) CRITICAL Gaps (Data‑Corrupting)

None identified because Round‑1 verification is not executed in this workspace.

---

## 5) Closed Gaps (Resolved)

### MB-GAP-001 — Design evidence IMPORT-PENDING (Master BOM design pack not yet registered in repo workspace) — ✅ RESOLVED
- **Resolved By:** Batch A import of design pack under `docs/MASTER_BOM/DESIGN/`
- **Resolution Evidence:** `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§3.2`
- **Notes:** Design Evidence axis now VERIFIED; repo-level trace paths are resolvable.

### MB-GAP-002 — Specific Item Master “plan recorded” evidence IMPORT-PENDING — ✅ RESOLVED
- **Resolved By:** Import of `docs/SPECIFIC_ITEM_MASTER/PLAN/SPECIFIC_ITEM_MASTER_DETAILED_DESIGN.md`
- **Resolution Evidence:** `docs/SPECIFIC_ITEM_MASTER/PLAN/SPECIFIC_ITEM_MASTER_DETAILED_DESIGN.md:L1–L6`
- **Notes:** Dependency satisfied; implementation may remain deferred.

---

## 6) Gap Revalidation (Phase-3)

**Purpose:** Re-classify all gaps with L0-L1-L2 layer context after Phase-3 Rule Compliance Review.

| Gap ID | Original Classification | Layer Label | Re-classification | Reason | Status |
|--------|------------------------|-------------|-------------------|--------|--------|
| MB-GAP-001 | HIGH (CLOSED) | Cross-Layer | ✅ Close | Design evidence imported; terminology clarified by L0-L1-L2 definitions | CLOSED |
| MB-GAP-002 | HIGH (CLOSED) | Cross-Layer | ✅ Close | Specific Item Master plan registered; terminology clarified by L0-L1-L2 definitions | CLOSED |
| MB-GAP-003 | HIGH | L1 | 🔁 Reword | Gap description needs L1 layer context (Master BOM operates at L1, ProductId NULL by design for L1 spec templates) | UPDATED |
| MB-GAP-004 | HIGH | L1 | ❌ Keep | True violation (hard delete vs soft delete); not terminology-related; requires code fix | OPEN |

**Re-classification Legend:**
- ✅ **Close:** Gap was terminology-caused, now resolved by L0-L1-L2 clarity
- 🔁 **Reword:** Gap needs layer context added to description
- ❌ **Keep:** True violation remains, not terminology-related

**Layer Label Legend:**
- **L0:** Generic Item Master (Functional Family)
- **L1:** Master BOM (Technical Variant, Make-agnostic)
- **L2:** Specific Item Master / Proposal BOM (Catalog Item with Make+Series+SKU)
- **Proposal-Resolution:** L1 → L2 resolution process
- **Cross-Layer:** Affects multiple layers

**Notes:**
- MB-GAP-003: Updated gap description to clarify that Master BOM operates at L1 layer, and ProductId=NULL is by design for L1 spec templates (not a bug, but a design decision that needs documentation).
- MB-GAP-004: Remains OPEN as it represents a true code violation (hard delete vs soft delete) that requires implementation fix.

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | Created as governed Gap Register; limited to Round-0 readiness blockers because Round-1 is not executed |
| v1.0_20251218 | 2025-12-18 | Amended DB-PENDING item B to Resolution enforcement; added MB-GAP-003/004 evidence |
| v1.0_20251218 | 2025-12-18 | Amended: moved MB-GAP-001 to Closed Gaps; counts updated (Design Evidence VERIFIED) |
| v1.0_20251218 | 2025-12-18 | Amended header/axes to reflect Design VERIFIED (DB remains DB-PENDING) |
| v1.0_20251218 | 2025-12-18 | Amended: moved MB-GAP-002 to Closed Gaps; counts updated (Specific Item Master plan registered) |
| v1.1_20251219 | 2025-12-19 | Phase-3: Added Gap Revalidation table; re-classified gaps with L0-L1-L2 layer labels |


