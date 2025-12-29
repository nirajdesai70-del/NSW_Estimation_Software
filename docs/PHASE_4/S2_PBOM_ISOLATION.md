# S2.5 — PBOM Isolation Pack (Reuse/Promote Surface vs QUO Apply Boundary)
#
# Task coverage:
# - NSW-P4-S2-PBOM-001 (G3) PBOM CRUD/reuse/promote vs QUO apply boundary (planning-only)
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase‑4 execution.
- **No code moves**.
- **No logic fixes**.
- **No QUO‑V2 execution**: QUO‑V2 remains fenced behind `NSW-P4-S2-QUO-REVERIFY-001` (G4).
- PBOM isolation here is limited to: **contracts, boundaries, forbidden couplings, and adapter seam notes**.

---

## 1) Confirmed Apply Entry Point (authoritative route; implementation fenced)

### Route surface (code anchor)

- **Route**: `quotation.v2.applyProposalBom`
- **HTTP**: `POST /quotation/v2/apply-proposal-bom`
- **Controller target (snapshot)**: `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyProposalBom`
- **Middleware**: `auth`, `throttle:critical-write`

### Apply request contract (observed from V2 panel UI + controller validation)

The apply endpoint validates/consumes:

- `QuotationId` (required)
- `QuotationSaleBomId` (required) — target feeder/BOM node to receive copied items
- `SourceQuotationSaleBomId` (required) — “proposal BOM” source id
- `Qty` (required numeric) — multiplier for copied quantities

### Apply response contract (observed)

- Success: `{ success: true, message: string }`
- Validation failure: `{ success: false, message: string }` (422)
- Execution failure: `{ success: false, message: string, error_details?: string|null }` (500)

---

## 2) PBOM Surface (authoritative; current implementation reality)

### PBOM “CRUD” / browsing routes (PBOM-owned intent; implemented over QUO tables)

PBOM is exposed as an authenticated route group:

- Prefix: `/proposal-bom`
- Controller: `source_snapshot/app/Http/Controllers/ProposalBomController.php`

**Routes:**

- `proposal-bom.index` → `GET /proposal-bom` — list reusable BOMs
- `proposal-bom.show` → `GET /proposal-bom/{id}` — show a reusable BOM and its items
- `proposal-bom.reuse` → `GET /proposal-bom/{id}/reuse` — mark a BOM for reuse (session-based)
- `proposal-bom.promote` → `POST /proposal-bom/{id}/promote` — promote a proposal BOM into a Master BOM template

### PBOM search endpoints (currently QUO-owned implementation)

PBOM selection in V2 uses existing search endpoints:

- `api.proposalBom.search` → `GET /api/proposal-bom/search?q=term` → `QuotationController@searchProposalBom`
- `api.reuse.proposalBoms` → `GET /api/reuse/proposal-boms` → `ReuseController@searchProposalBoms`

**Discipline:** These are recorded as PBOM selection surfaces, but they are implemented inside QUO/Reuse in the snapshot; refactoring is out of scope for S2.

### Storage reality (critical boundary note)

PBOMs are **not a separate table** in this snapshot:

- Proposal BOMs are stored as `quotation_sale_boms` rows (historical quotation BOMs) and their `quotation_sale_bom_items`.
- `ProposalBomController` queries `QuotationSaleBom` and treats BOMs with `BomName` and/or `MasterBomName` as reusable “proposal BOMs”.

---

## 3) PBOM Reuse/Promote vs QUO Apply Boundary (hard boundary statements)

### Ownership split (effective for Phase‑4 planning)

- **PBOM owns (selection + reuse intent + promotion intent)**:
  - Listing/browsing reusable BOMs
  - “Select for reuse” UX state (e.g. session marker)
  - Promotion request: “turn this historical BOM into an MBOM template”
- **QUO owns (apply/mutation into active quotations)**:
  - Copying items into a live quotation’s tree (`applyProposalBom`)
  - Any pricing/discount propagation behavior during apply

### Boundary statement (apply discipline)

- PBOM **must not** directly mutate active quotation structures/items.
- PBOM triggers apply only via the **documented QUO apply endpoint** (`quotation.v2.applyProposalBom`).
- QUO apply treats PBOM as an **external source identifier** (`SourceQuotationSaleBomId`) and enforces validation and copying.

### Boundary statement (promotion discipline)

- PBOM promotion is conceptually a **request** to create an MBOM template.
- In Phase‑4 execution, MBOM creation should be isolated behind an MBOM-owned seam (see Adapter Seams).
- S2 records current behavior only; no changes are allowed.

---

## 4) Forbidden Coupling (explicit)

### Forbidden: any QUO‑V2 core edits / apply behavior changes

**Rule:** No edits to QUO‑V2 controllers/services/models in S2.

- Do not touch `QuotationV2Controller` (PROTECTED) or downstream QUO services/models.
- Do not change apply semantics for `quotation.v2.applyProposalBom`.

### Forbidden: PBOM introducing new QUO protected callers

**Rule:** PBOM must not introduce new direct dependencies on QUO protected services/models/controllers beyond the currently observed surfaces.

- New cross-module integration must be via documented HTTP endpoints or approved adapters/contracts (post‑G4).

---

## 5) Adapter Seam Notes (planning-only; no execution leakage)

### 5.1 Proposed seam: PBOM read/search adapter (PBOM-owned)

**Contract name:** `ProposalBomReadContract`  
**Owner:** PBOM  
**Consumers:** PBOM UI; V2 selection UI (via search); reuse flows  
**Purpose:** stable read-only listing/search of reusable BOM roots

**DTO skeleton (minimum):**

- `ProposalBomSummary`:
  - `ProposalBomId` (maps to `QuotationSaleBomId`)
  - `BomName`
  - `SourceQuotationNo?`, `ProjectName?`, `ClientName?` (display-only)
  - `Level?`
  - `ComponentCount?`

### 5.2 Proposed seam: PBOM apply command wrapper (QUO-owned; PBOM/V2 UI calls via route)

**Contract name:** `ApplyProposalBomCommand`  
**Owner:** QUO  
**Consumer:** V2 apply UI  
**Purpose:** stable command interface for “copy items from source BOM to target BOM”

**Input skeleton (matches observed UI payload):**

- `quotationId`
- `targetQuotationSaleBomId`
- `sourceQuotationSaleBomId`
- `qtyMultiplier`

### 5.3 Proposed seam: Promote-to-MBOM adapter (MBOM-owned; PBOM calls)

**Contract name:** `PromoteProposalBomToMasterBomContract`  
**Owner:** MBOM  
**Consumer:** PBOM promote action  
**Purpose:** create a new MBOM template from a proposal BOM snapshot without PBOM writing MBOM internals directly

---

## 6) Known Risks / Couplings (record only; do not fix in S2)

### PBOM is implemented over QUO tables/models (coupling)

- PBOM “data model” is `QuotationSaleBom` + `QuotationSaleBomItem`, with joins to quotation/project/client for display/search.
- This means PBOM currently depends on QUO-owned persistence structures.

**Discipline:** Record only; any separation requires Phase‑4 execution approvals and should be done via seams/contracts.

### “Reuse” is session-based and redirects into QUO legacy UI flow

- `ProposalBomController@reuse()` writes session keys:
  - `reuse_proposal_bom_id`
  - `reuse_proposal_bom_name`
- Then redirects to `quotation.index` with instructions to apply later.

**Discipline:** Record only; no flow changes in S2.

### PBOM selection in V2 depends on a legacy search API

- V2 panel uses `api.proposalBom.search` (`QuotationController@searchProposalBom`) for Select2 AJAX search.

**Discipline:** Record only; do not move/rename routes/controllers in S2.

### Promote-to-master writes MBOM rows directly (cross-module coupling)

- `proposal-bom.promote` creates `MasterBom` and `MasterBomItem` records directly.

**Coupling risk notes (record only):**

- Promotion currently copies `ProductId` and integer `Quantity` into `MasterBomItem`.
- MBOM has additional integrity rules (e.g. B4 resolution semantics) that may not align with this direct copy path.

**Discipline:** Record only; any reconciliation is post‑G4 and requires approvals.

---

## 7) PBOM Routes Inventory (authoritative; current implementation reality)

### 7.1 PBOM-owned CRUD routes (ProposalBomController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `proposal-bom.index` | GET | `/proposal-bom` | `ProposalBomController@index` | List reusable BOMs | PBOM-owned |
| `proposal-bom.show` | GET | `/proposal-bom/{id}` | `ProposalBomController@show` | Show reusable BOM and items | PBOM-owned |
| `proposal-bom.reuse` | GET | `/proposal-bom/{id}/reuse` | `ProposalBomController@reuse` | Mark BOM for reuse (session-based) | PBOM-owned |
| `proposal-bom.promote` | POST | `/proposal-bom/{id}/promote` | `ProposalBomController@promoteToMaster` | Promote proposal BOM to Master BOM | PBOM-owned |

### 7.2 QUO-owned apply routes (QuotationV2Controller)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.v2.applyProposalBom` | POST | `/quotation/v2/apply-proposal-bom` | `QuotationV2Controller@applyProposalBom` | Apply proposal BOM to quotation | QUO-owned (PROTECTED) |

### 7.3 QUO-owned search routes (QuotationController — compat)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `api.proposalBom.search` | GET | `/api/proposal-bom/search` | `QuotationController@searchProposalBom` | Search proposal BOMs (Select2 AJAX) | COMPAT (legacy) |
| `quotation.getProposalBomVal` | GET | `/quotation/getProposalBomVal` | `QuotationController@getProposalBomVal` | Get proposal BOM value (legacy) | COMPAT (legacy) |

### 7.4 SHARED-owned reuse routes (ReuseController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `api.reuse.proposalBoms` | GET | `/api/reuse/proposal-boms` | `ReuseController@searchProposalBoms` | Search proposal BOMs for reuse | SHARED-owned (future) |

**Note:** Legacy routes are inventory-only in S2; removal happens only after S4 propagation + S5 Bundle-C pass.

---

## 8) Forbidden Callers (hard fence for Phase-4)

### 8.1 Modules forbidden from calling PBOM directly

**Rule:** The following modules **must not** call PBOM ORM models or internal services directly:

- **QUO (Legacy + V2):** Must use `quotation.v2.applyProposalBom` wrapper endpoint only
- **MBOM:** Must not access PBOM-specific logic (PBOMs are stored as `QuotationSaleBom` rows)
- **FEED:** Must use QUO apply wrapper (feeder templates are separate from proposal BOMs)
- **SHARED:** Must use `ProposalBomReadContract` (when implemented) or reuse search endpoints

### 8.2 Forbidden direct access patterns

**Forbidden:**
- Direct `QuotationSaleBom` queries from QUO code to find "proposal BOMs" (must use contract/route)
- Direct `ProposalBomController` method calls from other controllers
- Bypassing `quotation.v2.applyProposalBom` to copy items directly
- Direct `MasterBom` / `MasterBomItem` writes from PBOM promote action (must use contract)

**Allowed:**
- HTTP calls to `quotation.v2.applyProposalBom` endpoint
- HTTP calls to `api.reuse.proposalBoms` endpoint (SHARED contract)
- Future: `ProposalBomReadContract` interface calls (S4+)
- Future: `PromoteProposalBomToMasterBomContract` interface calls (S4+)

### 8.3 PBOM forbidden from calling

**Rule:** PBOM **must not** call:

- QUO models/services (except via `ApplyProposalBomCommand` wrapper)
- MBOM models/services (except via `PromoteProposalBomToMasterBomContract`)
- FEED models/services
- QUO costing/quantity services
- QUO controllers (except via HTTP wrapper endpoints)

**Current exception (to be fixed in S4):**
- `ProposalBomController@promoteToMaster` directly creates `MasterBom` / `MasterBomItem` rows (forbidden coupling)
- **Fix:** Replace with `PromoteProposalBomToMasterBomContract` call in S4

---

## 9) Apply Semantics (qty, reuse, origin tracking, instance isolation, no side effects)

### 9.1 Quantity multiplier semantics

**Contract rule:** The `Qty` parameter in `quotation.v2.applyProposalBom` is a **multiplier**, not an absolute quantity.

**Behavior (frozen in S2):**
- Each source `QuotationSaleBomItem.Qty` is multiplied by `Qty` when creating target items
- UI must supply multiplier; apply endpoint owns quantity math
- No pre-multiplication in UI callers (explicitly forbidden)

**Example:**
- Source item: `Qty = 2.0`
- Apply request: `Qty = 3.0`
- Result: Target item `Qty = 6.0`

### 9.2 Origin tracking semantics

**Contract rule:** Apply endpoint must set origin tracking fields to enable reuse detection and audit trails.

**Fields set by apply (observed pattern):**
- `QuotationSaleBom.MasterBomId` = source `MasterBomId` (if source has one)
- `QuotationSaleBom.MasterBomName` = source `MasterBomName` (if source has one)
- `QuotationSaleBomItem` origin fields (if applicable)

**Note:** PBOM apply copies from one `QuotationSaleBom` to another, so origin tracking may reference the source quotation BOM rather than a template.

### 9.3 Instance isolation semantics (PB-GAP-004 closure requirement)

**Contract rule (frozen for S5 verification):** Apply operation **must create new instances** with new IDs; no shared IDs between source and target.

**Required behavior (to be verified in S5):**
- Each copied `QuotationSaleBomItem` must have a new `QuotationSaleBomItemId` (auto-generated)
- Target `QuotationSaleBom` must have a different `QuotationSaleBomId` than source
- Re-applying the same source to the same target must not duplicate or link items (must clear-before-copy or detect duplicates)

**Evidence requirement (PB-GAP-004):**
- S5 verification must provide evidence in `docs/PHASE_4/evidence/GAP/PB-GAP-004/`
- Evidence must include: R1 request/response, S1/S2 snapshots showing instance isolation (new IDs, no shared references)

### 9.4 Quantity chain correctness (PB-GAP-003 closure requirement)

**Contract rule (frozen for S5 verification):** Apply operation **must preserve quantity chain integrity** and handle feeder discovery edge cases correctly.

**Required behavior (to be verified in S5):**
- Quantity multipliers must propagate correctly through the BOM tree
- Feeder discovery (finding parent feeders) must work correctly for copied items
- Edge cases: nested BOMs, multiple feeders, quantity = 0, quantity = NULL

**Evidence requirement (PB-GAP-003):**
- S5 verification must provide evidence in `docs/PHASE_4/evidence/GAP/PB-GAP-003/`
- Evidence must include: R1 request/response, S1/S2 snapshots showing quantity chain correctness, feeder discovery edge case tests

### 9.5 No side effects rule

**Contract rule:** Apply operation must not mutate source proposal BOM data.

**Guarantees:**
- Source `QuotationSaleBom` / `QuotationSaleBomItem` rows are **never modified** by apply
- Apply creates new `QuotationSaleBomItem` rows in target BOM only
- Source proposal BOM remains immutable and reusable

**Exception (record only, not to fix in S2):**
- If source has `MasterBomId`, apply copies that reference to target (this is reference copying, not mutation)

---

## 10) S4 Propagation Hooks (declared, not executed)

### 10.1 Contract propagation targets

**Target 1: ProposalBomReadContract implementation**
- **Owner:** PBOM
- **Consumers:** QUO apply, PBOM UI, reuse search
- **S4 Task:** `NSW-P4-S4-PBOM-001` — Propagate Proposal BOM apply contract

**Target 2: ApplyProposalBomCommand wrapper**
- **Owner:** QUO
- **Consumer:** PBOM/V2 apply UI
- **S4 Task:** Adopt wrapper entry points for V2 apply flows (when `NSW-P4-S2-QUO-002` completes)

**Target 3: PromoteProposalBomToMasterBomContract implementation**
- **Owner:** MBOM
- **Consumer:** PBOM promote action
- **S4 Task:** Replace direct `MasterBom` / `MasterBomItem` writes in `ProposalBomController@promoteToMaster`

### 10.2 Route migration targets

**Target 1: PBOM search routes → ReuseSearchContract**
- `api.reuse.proposalBoms` → Migrate to `ReuseSearchContract` (when `NSW-P4-S2-SHARED-001` completes)
- `api.proposalBom.search` → Remove after S4 migration (legacy Select2 endpoint)

**Target 2: Legacy QUO routes → Deprecation**
- `quotation.getProposalBomVal` → Remove after S5 Bundle-C pass

### 10.3 Gap closure targets (S5)

**Target 1: PB-GAP-003 closure (quantity chain correctness)**
- **S5 Task:** `NSW-P4-S5-PBOM-GAP-003` — Verify quantity chain correctness + feeder discovery edge cases
- **Evidence:** `docs/PHASE_4/evidence/GAP/PB-GAP-003/`
- **Gate:** S5/G3 (escalate to G4 if PROTECTED touched)

**Target 2: PB-GAP-004 closure (instance isolation)**
- **S5 Task:** `NSW-P4-S5-PBOM-GAP-004` — Verify instance isolation under proposal reuse/apply flows
- **Evidence:** `docs/PHASE_4/evidence/GAP/PB-GAP-004/`
- **Gate:** S5/G3 (escalate to G4 if PROTECTED touched)

---

## 11) References (Authority)

**Authority Documents:**
- `trace/phase_2/FILE_OWNERSHIP.md` (ProposalBomController ownership)
- `trace/phase_2/ROUTE_MAP.md` (PBOM routes inventory)
- `docs/PHASE_4/S2_GOV_BOUNDARY_BLOCKS.md` (PBOM boundary rules)
- `docs/PHASE_4/S2_GOV_EXCEPTION_TASK_MAPPING.md` (Exception mapping)
- `docs/PHASE_4/GAP_GATEBOARD.md` (PB-GAP-003, PB-GAP-004)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (S2 fences + order)
- `docs/PHASE_4/S2_MBOM_ISOLATION.md` (MBOM pattern reference)
- `docs/PHASE_4/S2_FEED_ISOLATION.md` (FEED pattern reference)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (CatalogLookupContract + ReuseSearchContract)

**Code Anchors:**
- `source_snapshot/app/Http/Controllers/ProposalBomController.php` (PBOM CRUD)
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyProposalBom` (QUO apply)
- `source_snapshot/app/Http/Controllers/ReuseController.php@searchProposalBoms` (Reuse search)
- `source_snapshot/app/Http/Controllers/QuotationController.php@searchProposalBom` (Legacy search)
- `source_snapshot/routes/web.php` (Route definitions)

---

## 12) Evidence / Approvals Checklist (G3)

- [x] Architectural approval: PBOM selection/reuse/promote vs QUO apply boundary accepted
- [x] Execution approval: planning-only; no behavior change; no QUO‑V2 scope crossed
- [x] Adapter seam acceptance: `ProposalBomReadContract`, `ApplyProposalBomCommand`, `PromoteProposalBomToMasterBomContract` recorded as the only approved future refactor seams
- [x] Gap closure requirements: PB-GAP-003 (quantity chain correctness) + PB-GAP-004 (instance isolation) semantics frozen in contract
- [x] Routes inventory: All PBOM routes classified (PBOM-owned, QUO-owned, SHARED-owned, COMPAT)
- [x] Forbidden callers: Hard fence documented for all modules
- [x] Apply semantics: Quantity multiplier, reuse tracking, origin tracking, instance isolation, no side effects documented
- [x] S4 propagation hooks: Contract migration targets declared

---

## Task Status

- **NSW-P4-S2-PBOM-001:** ✅ Complete
- **Next Stage:** S3 — Alignment (contract freeze)

---

**Last Updated:** 2025-12-18  
**Status:** ✅ Complete — Ready for S3 alignment


