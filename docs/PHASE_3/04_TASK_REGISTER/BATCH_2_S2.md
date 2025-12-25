# Batch-2 — S2 Isolation (Module Boundaries + Decoupling Plan)

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Batch:** B2  
**Coverage:** S2 (Isolation)  
**Status:** ACTIVE (Planning Only)  
**Last Updated:** 2025-12-18 (IST)

**Authority:**
- Risk/ownership: `trace/phase_2/FILE_OWNERSHIP.md`
- Sequencing: `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- Gates: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Governance: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`

---

## 1. Batch Purpose

Batch-2 defines **Isolation tasks** that create safe boundaries before any alignment or propagation work begins.

S2 focuses on:
- module boundary enforcement (who can call whom)
- elimination of hidden coupling points
- creation of wrapper/adaptor seams for PROTECTED zones
- removal of duplicate resolution paths (planning only; execution in Phase 4)

**Rule:** No execution in Phase 3. These are task cards for Phase 4.

---

## 2. Pre-Conditions (Must be true)

Batch-2 is valid only after Batch-1 exit criteria are satisfied:
- S0 verification tasks have evidence
- S1 ownership placeholders are ready to expand
- ownership exceptions list exists (even if empty)

If S1 is incomplete, only the GOV S2 tasks can proceed.

---

## 3. Batch Task List (Authoritative)

| Task ID | S-Stage | Module | Sub-Area | Type | Risk | Gate | Objective (1 line) | In Scope (explicit) | Forbidden | Cross-Module Touchpoints | Evidence Required | Approvals Required | Rollback Required | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NSW-P4-S2-GOV-001 | S2 | GOV | Ownership Exceptions | Refactor Planning | HIGH | G3 | Convert S1 ownership exceptions into split/adapter task stubs | Exceptions list from `BATCH_1_S0_S1.md` | Any code edits | All modules | Exception→Task mapping table | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-GOV-002 | S2 | GOV | Boundary Blocks | Governance | HIGH | G3 | Create canonical “Boundary Block” per module (allowed callers / forbidden callers) | CIM/MBOM/FEED/PBOM/QUO boundary blocks | Changing business logic | All modules | Boundary blocks added to docs | Arch: Yes / Exec: No / Release: No | No | Planned |
| NSW-P4-S2-SHARED-001 | S2 | SHARED | Shared Utilities Contract | Refactor Planning | HIGH | G3 | Declare shared utility contracts (inputs/outputs) to prevent bleed-through | Shared endpoints list + shared utils | Any functional change | Reuse + dropdown APIs | Contract doc + mapping | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-SHARED-002 | S2 | SHARED | Shared Controller Split Plan | Refactor Planning | HIGH | G3 | Plan split for mixed-responsibility controllers (no moves yet) | Identified shared controllers | Any file move now | Multiple modules | Split plan: owner per method group | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-MASTER-001 | S2 | MASTER | Master Reference Isolation | Refactor Planning | MEDIUM | G2 | Ensure Master (Org/Vendor/PDF) exposes clean reference interfaces only | Master module docs + route grouping plan | UI changes | Quotation/Project | Interface notes + forbidden access list | Arch: Yes / Exec: No / Release: No | No | Planned |
| NSW-P4-S2-EMP-001 | S2 | EMP | Role/Security Touchpoints | Refactor Planning | MEDIUM | G2 | Document and isolate Employee/Role touchpoints as cross-cutting | Roles, permissions docs | Security redesign | All modules | Touchpoint map | Arch: Yes / Exec: No / Release: No | No | Planned |
| NSW-P4-S2-CIM-001 | S2 | CIM | Import Split Isolation | Refactor Planning | HIGH | G3 | Define hard boundary for ImportController split (CIM vs Master/PDF) + adaptor seam | Import split map from Batch-1 | Any controller edits | Master/PDFContain | Isolation plan + adaptor seam spec | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-CIM-002 | S2 | CIM | Catalog Resolution Single Path | Refactor Planning | HIGH | G3 | Identify and plan removal of duplicate catalog resolution paths | Category/item/product lookup endpoints | Any pricing changes | Quotation Legacy + V2 | “Single-path” resolution plan | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-MBOM-001 | S2 | MBOM | MBOM Interface Isolation | Refactor Planning | HIGH | G3 | Define MBOM read/apply interface contract (no apply changes) | MBOM endpoints + apply touchpoints | Apply behavior change | Quotation V2 | Contract spec + forbidden callers | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-FEED-001 | S2 | FEED | Feeder Interface Isolation | Refactor Planning | HIGH | G3 | Define Feeder template interface contract for V2 apply | Feeder endpoints + apply touchpoints | Apply behavior change | Quotation V2 | Contract spec + forbidden callers | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-PBOM-001 | S2 | PBOM | Proposal BOM Interface Isolation | Refactor Planning | HIGH | G3 | Define Proposal BOM interface contract for V2 apply | Proposal BOM endpoints + apply touchpoints | Apply behavior change | Quotation V2 | Contract spec + forbidden callers | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-QUO-001 | S2 | QUO | Legacy Quotation Isolation | Refactor Planning | HIGH | G3 | Define legacy quotation boundaries; ensure it consumes masters via contracts | Legacy routes + dependencies | Pricing logic changes | Shared endpoints | Boundary + consumption map | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S2-QUO-002 | S2 | QUO | V2 Wrapper Seams (Protected) | Refactor Planning | PROTECTED | G4 | Define wrapper/adaptor seams around V2 protected core | V2 protected list + apply bundles | Any direct core edits | MBOM/FEED/PBOM apply | Wrapper seam spec + “no-go” list | Arch: Yes / Exec: Yes / Release: Yes | Yes (validated) | Planned |
| NSW-P4-S2-QUO-003 | S2 | QUO | Costing/Quantity Protection Contract | Refactor Planning | PROTECTED | G4 | Specify strict contract for CostingService + QuantityService (wrapper-only) | Protected services list | Any direct edits | All modules | Contract spec + allowed wrappers | Arch: Yes / Exec: Yes / Release: Yes | Yes (validated) | Planned |

---

## 4. Batch-2 Outputs (What must exist after this batch)

1. Module Boundary Blocks for core modules (CIM/MBOM/FEED/PBOM/QUO)
2. Shared utilities contract notes + split plan for mixed controllers
3. Wrapper seam specifications for PROTECTED zones (Quotation V2 + Costing/Quantity)
4. “Single-path resolution plan” for catalog lookups (no execution)
5. Updated Task Register links to this Batch-2 file

---

## 5. Batch-2 Exit Criteria

Batch-2 is complete when:
- All tasks remain **Planned** but have required evidence documents prepared
- Each contract/boundary/seam is written clearly enough to be executed later
- No unresolved ownership ambiguity remains for S2 scope

Next batch:
- **Batch-3 — S3 Alignment task cards**

---

## 6. Evidence Pack (S2 Planning Artefacts; No Code)

This section is the **evidence set** required by the Batch-2 tasks above.  
It is written to be execution-ready for Phase 4, while remaining planning-only in Phase 3.

### 6.1 Ownership Exceptions → Task Stub Mapping (NSW-P4-S2-GOV-001)

**Input authority:** `docs/PHASE_3/04_TASK_REGISTER/BATCH_1_S0_S1.md` (S1 placeholder: ownership exceptions list)

Ownership exceptions to be tracked at minimum (known from Phase-2 trace/ownership):
- `source_snapshot/app/Http/Controllers/ImportController.php` (CIM Import + MASTER PDF container split ownership)
- `source_snapshot/routes/api.php` (Quotation-owned file hosting “shared APIs”; needs SHARED contract boundary)
- `source_snapshot/app/Http/Controllers/QuotationController.php` (mixed: legacy quotation + shared dropdown APIs)
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php` (PROTECTED V2 core + cross-module apply)

**Exception → Task mapping table (to be filled/expanded during S1 close):**

| Exception (File/Area) | Why it is an exception | Split Target (future) | Adapter/Wrappers Needed | Proposed Task ID(s) |
|---|---|---|---|---|
| `ImportController.php` | Controller hosts CIM import and Master/PDF (`pdfcontain.*`) | `CIM/Import*` + `MASTER/PdfContain*` | Adapter for shared `Setting` access | NSW-P4-S2-CIM-001, NSW-P4-S2-SHARED-002 |
| `QuotationController` shared API methods | Quotation owns dropdown APIs used by legacy+V2 | `SHARED/CatalogLookup*` | Contract + adapter to CIM | NSW-P4-S2-SHARED-001, NSW-P4-S2-SHARED-002, NSW-P4-S2-CIM-002 |
| `routes/api.php` | Shared endpoints live in Quotation module | Extract route groups to SHARED boundary | Route-group adaptor (Phase-4) | NSW-P4-S2-SHARED-002 |
| `QuotationV2Controller` apply + core | PROTECTED; cross-module apply bundles | Wrapper-only seams | Wrappers around apply + costing/qty | NSW-P4-S2-QUO-002, NSW-P4-S2-QUO-003 |

**Evidence required:** This table completed and signed off (Arch + Exec) before Phase 4 execution planning begins.

---

### 6.2 Canonical Boundary Blocks (NSW-P4-S2-GOV-002)

Boundary Blocks are the **canonical “who can call whom” declarations**. They define:
- **Allowed Callers** (modules)
- **Allowed Entry Points** (routes/controllers/services)
- **Forbidden Callers** (modules)
- **Forbidden Access Patterns** (e.g., “direct model reads across module boundary”)
- **Adapter/Wrappers** (the only permitted bypass mechanism)

**Authority anchors:**
- Route-to-module map: `trace/phase_2/ROUTE_MAP.md`
- Code-to-feature map: `trace/phase_2/FEATURE_CODE_MAP.md`
- Risk/ownership: `trace/phase_2/FILE_OWNERSHIP.md`

#### Boundary Block — SHARED (Cross-Module Utilities + APIs)

- **Owner**: SHARED
- **Purpose**: Host contracts for cross-module endpoints/utilities, not business logic.
- **Allowed callers**: ALL modules (by definition), but **only via declared contracts**.
- **Allowed entry points (current reality)**:
  - Shared dropdown APIs (currently owned by QUO): `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.makes` (see `trace/phase_2/ROUTE_MAP.md`)
  - Reuse search APIs: `api.reuse.*` (see `trace/phase_2/ROUTE_MAP.md`)
- **Forbidden**:
  - Adding new “shared” endpoints inside unrelated modules without SHARED contract + ownership.
  - Cross-module code reading other module models directly (outside contracts).
- **Adapter seams**:
  - `CatalogLookupContract` (defined in Section 6.3)
  - `ReuseSearchContract` (defined in Section 6.3)

#### Boundary Block — MASTER (Org/Vendor/PDF)

- **Owner**: MASTER
- **Allowed callers**: Project, Quotation, CIM (reference-only).
- **Allowed entry points (routes)**:
  - `organization.*`, `vendor.*`, `pdfcontain.*` (controller ownership anchored in `trace/phase_2/ROUTE_MAP.md` and `trace/phase_2/FEATURE_CODE_MAP.md`)
- **Forbidden**:
  - Any module directly mutating Master tables outside Master-owned controllers/services.
  - Reusing Master/PDF settings logic via CIM import flows (must be adapter-only).
- **Adapter seams**:
  - `PdfContainSettingsContract` for PDF container access (read/write scoping) (Section 6.6)

#### Boundary Block — EMP (Employee/Role)

- **Owner**: EMP
- **Allowed callers**: ALL modules (authentication/authorization is cross-cutting)
- **Allowed entry points (routes)**:
  - `role.*`, `user.*`
- **Forbidden**:
  - Any module implementing local authorization rules that diverge from EMP policy/middleware.
  - Any “role cache” duplication without an EMP-owned contract.
- **Adapter seams**:
  - `AuthorizationTouchpointMap` (Section 6.7) — documentation boundary, not code.

#### Boundary Block — CIM (Component/Item Master)

- **Owner**: CIM
- **Allowed callers**:
  - Quotation (read-only catalog lookup) via **SHARED CatalogLookupContract**
  - Master BOM / Feeder / Proposal BOM (read-only catalog lookup) via contract
- **Allowed entry points (routes/controllers)**:
  - CRUD routes: `category.*`, `subcategory.*`, `item.*`, `make.*`, `series.*`, `attribute.*`, `product.*`, `price.*`
  - Import routes: `import.*` (see `trace/phase_2/ROUTE_MAP.md`)
- **Forbidden**:
  - Quotation directly “knowing” CIM model structure (direct model reads across boundary) once contracts exist.
  - Any pricing logic changes as part of S2 (explicitly forbidden by NSW-P4-S2-CIM-002).
- **Adapter seams**:
  - `CatalogLookupContract` (Section 6.3)
  - Import split adapter seam (Section 6.8)

#### Boundary Block — MBOM (Master BOM)

- **Owner**: MBOM
- **Allowed callers**:
  - Quotation V2 (apply template) via explicit apply interface contract.
  - SHARED/Reuse search (read-only) via contract.
- **Allowed entry points (routes/controllers)**:
  - `masterbom.*`
  - Apply touchpoint: `quotation.v2.applyMasterBom` (consumer)
- **Forbidden**:
  - Any module directly mutating MBOM internals (tables/structure) outside MBOM controllers/services.
  - Any behavior change to apply as part of S2 (planning-only).
- **Adapter seams**:
  - `MbomApplyContract` (Section 6.10)

#### Boundary Block — FEED (Feeder Library)

- **Owner**: FEED
- **Allowed callers**:
  - Quotation V2 (apply feeder template) via explicit apply interface contract.
  - SHARED/Reuse search (read-only) via contract.
- **Allowed entry points (routes/controllers)**:
  - `feeder-library.*`
  - Apply touchpoint: `quotation.v2.applyFeederTemplate` (consumer)
- **Forbidden**:
  - Any apply behavior change as part of S2 (planning-only).
- **Adapter seams**:
  - `FeederApplyContract` (Section 6.11)

#### Boundary Block — PBOM (Proposal BOM)

- **Owner**: PBOM
- **Allowed callers**:
  - Quotation V2 (apply proposal BOM) via explicit apply interface contract.
  - MBOM (promote flow) under explicit PBOM-to-MBOM promotion contract (future S3/S4).
- **Allowed entry points (routes/controllers)**:
  - `proposal-bom.*`
  - Apply touchpoint: `quotation.v2.applyProposalBom` (consumer)
  - Search touchpoint: `api.proposalBom.search` (currently owned by QUO; must follow contract)
- **Forbidden**:
  - Any apply behavior change as part of S2 (planning-only).
- **Adapter seams**:
  - `ProposalBomApplyContract` (Section 6.12)

#### Boundary Block — QUO (Quotation Legacy + V2)

- **Owner**: QUO
- **Allowed callers**:
  - UI layer / routes only (no other module should “call” Quotation internals)
- **Allowed entry points**:
  - Legacy routes: `quotation.*`
  - V2 routes: `quotation.v2.*`, `reuse.*`, `api.reuse.*`
- **Forbidden**:
  - Upstream modules calling Quotation internals as “services”.
  - Direct edits to PROTECTED V2 core and protected services outside wrapper seams (see Rulebook).
- **Adapter seams**:
  - V2 wrapper seams (Section 6.13)
  - Costing/Quantity wrapper-only contract (Section 6.14)

---

### 6.3 Shared Utilities Contract Notes (NSW-P4-S2-SHARED-001)

**Goal:** Declare shared utility contracts (inputs/outputs) so callers don’t depend on implementation details.

#### Contract: CatalogLookupContract (Dropdown APIs)

**Authority anchor:** `trace/phase_2/ROUTE_MAP.md` (shared endpoints currently in QUO: `QuotationController@...`)

- **In-scope endpoints** (existing route names):
  - `api.category.subcategories`
  - `api.category.items`
  - `api.category.products`
  - `api.item.products`
  - `api.product.makes`
  - `api.make.series`
  - `api.product.descriptions`
  - `api.category.makes`
  - `api.makes`

- **Contract inputs (canonical request parameters)**:
  - categoryId / itemId / productId / makeId (as applicable)
  - optional: searchTerm (if present in current UI; verify during execution)

- **Contract outputs (canonical response shape)**:
  - list of `{ id, label }`
  - optional metadata: `{ sourceVersion, cacheHints }` (planning placeholder)

- **Forbidden coupling**:
  - returning ORM-specific fields without contract definition
  - callers relying on “extra fields” not declared in contract

#### Contract: ReuseSearchContract

**Authority anchor:** `trace/phase_2/ROUTE_MAP.md` (ReuseController search endpoints)

- **In-scope endpoints**:
  - `api.reuse.panels`
  - `api.reuse.feeders`
  - `api.reuse.masterBoms`
  - `api.reuse.proposalBoms`

- **Contract inputs**:
  - searchTerm
  - scope filters (quotationId/panelId where applicable; verify during execution)

- **Contract outputs**:
  - list of reuse candidates with stable identifiers and display labels

**Evidence required:** Contract notes + mapping to current endpoints (this section) approved before Phase 4 extraction/moves.

---

### 6.4 Shared Controller Split Plan (NSW-P4-S2-SHARED-002)

**Goal:** Plan split for mixed-responsibility controllers (no moves yet).

#### Candidate: `ImportController` (Split ownership: CIM vs MASTER/PDF)

- **CIM-owned method group (Import/Export)**:
  - routes: `import.*`, `export.*` (see ROUTE_MAP lines for `/import`, `/export`)
  - models referenced (from FEATURE_CODE_MAP): Category/Item/Product/Price/Attribute temp models, etc.

- **MASTER-owned method group (PDF container)**:
  - routes: `pdfcontain.*` (see ROUTE_MAP: `/pdfcontain`)
  - models referenced (from FEATURE_CODE_MAP): `Setting`

- **Planned split**:
  - Phase 4: create two controllers (or controller + service split):
    - `CimImportController` (CIM owner)
    - `MasterPdfContainController` (MASTER owner)
  - Temporary adapter seam to keep routes stable until propagation (S4).

#### Candidate: `QuotationController` (Legacy + Shared dropdown APIs)

- **QUO Legacy method group**:
  - routes: `quotation.*` legacy CRUD, step flows, exports, etc.
- **SHARED dropdown API group** (currently inside QuotationController):
  - methods backing `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.makes`

- **Planned split**:
  - Phase 4: extract dropdown APIs into SHARED-owned controller (e.g., `CatalogLookupController`)
  - QuotationController becomes a consumer (if it needs internal reuse).

**Evidence required:** “Owner per method group” mapping and target controller list (this section expanded with method names during S0/S1 evidence collection).

---

### 6.5 Master Reference Isolation Notes (NSW-P4-S2-MASTER-001)

**Goal:** Ensure MASTER exposes clean reference interfaces only (Org/Vendor/PDF).

- **Reference-only consumption rule**:
  - Quotation and Project can read Organization/Vendor reference data via stable interfaces (routes/services).
  - No module other than MASTER should own write access patterns to these entities.

- **Forbidden access list (Phase 4 enforcement target)**:
  - Quotation logic should not embed PDF container “settings” knowledge.
  - CIM import should not mutate PDF container settings except through MASTER-owned adapter/contract.

**Evidence required:** Interface notes + forbidden access list (this section), with route grouping plan.

---

### 6.6 Employee/Role Touchpoint Map (NSW-P4-S2-EMP-001)

**Goal:** Document and isolate Employee/Role touchpoints as cross-cutting.

**System-wide touchpoints to enumerate in Phase 4 execution planning:**
- route middleware usage: `auth`, `throttle:*` (see ROUTE_MAP)
- role/permission checks in controllers/services (to be extracted from code during execution)

**S2 boundary statement:**
- Modules may depend on authentication/authorization outcomes, but must not re-implement or fork role policy logic locally.

**Evidence required:** Touchpoint map expanded with concrete call sites (Phase 4).

---

### 6.7 Catalog Single-Path Resolution Plan (NSW-P4-S2-CIM-002)

**Goal:** Identify and plan removal of duplicate catalog resolution paths (planning-only).

**Authority anchors:**
- Shared dropdown API endpoints currently backing both legacy+V2: `trace/phase_2/ROUTE_MAP.md` (`api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`)
- Additional “AJAX lookup” endpoints exist inside CIM controllers (e.g., ProductController/MasterBomController lookups in ROUTE_MAP).

#### Observed duplication patterns (from trace)

- **Path A (Shared dropdown API path; QUO-owned today)**:
  - Category → (Subcategories, Items, Products, Makes)
  - Item → Products
  - Product → (Makes, Descriptions)
  - Make → Series
  - Fallback “All makes”

- **Path B (Module-local AJAX lookups)**:
  - ProductController: `product.getsubcategory`, `product.getproducttype`, `product.getgeneric`, `product.getseries`
  - MasterBomController: `masterbom.getsubcategory`, `masterbom.getproducttype`, `masterbom.getdescription`

#### Single-path target (planning statement)

- **Canonical owner for catalog resolution logic**: CIM (data) + SHARED (contract surface)
- **Canonical access surface**:
  - SHARED `CatalogLookupContract` endpoints only
  - All modules consume via contract and must not re-implement resolution rules

#### Phase 4 execution plan (no execution now)

- Inventory all resolution endpoints/methods and group into:
  - canonical (kept)
  - compatibility (temporary)
  - duplicate (planned removal)
- Define deprecation plan:
  - maintain backward compatibility until S4 propagation completes
  - remove duplicates only after S5 Bundle C (Catalog Validity) passes

**Evidence required:** “Single-path” resolution plan finalized with endpoint list and deprecation order.

---

### 6.8 Import Split Isolation + Adapter Seam (NSW-P4-S2-CIM-001)

**Goal:** Define hard boundary for ImportController split (CIM vs Master/PDF) + adaptor seam.

**Current reality (trace anchor):**
- `/import` + `/export` routes are CIM-owned (Import/Export)
- `/pdfcontain` routes are MASTER-owned (PDF Formats) but implemented inside `ImportController`

**Isolation plan:**
- Phase 4: introduce adapter seam so that:
  - CIM import flow cannot directly access PDF container settings logic
  - MASTER PDF container flow cannot pull in CIM import internals

**Adapter seam spec (planning-only):**
- **Name:** `PdfContainSettingsContract`
- **Owned by:** MASTER
- **Consumed by:** CIM Import (if needed), Quotation PDF generation (if needed)
- **Forbidden:** direct reads/writes to `Setting` from CIM-owned import logic once contract exists

**Evidence required:** Isolation plan + adapter seam spec approved (Arch + Exec).

---

### 6.9 Quotation Legacy Isolation (NSW-P4-S2-QUO-001)

**Goal:** Define legacy quotation boundaries and ensure it consumes masters via contracts.

**Known dependencies (trace anchor):**
- Legacy Quotation relies on shared dropdown APIs: `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`
- Legacy Quotation uses Master BOM “get” routes (`quotation.getMasterBom*`) and exports (PDF/Excel)

**Boundary statement:**
- Legacy Quotation may consume:
  - Catalog lookup via SHARED `CatalogLookupContract`
  - MBOM read/apply via `MbomApplyContract` (or read-only contract)
  - MASTER reference data via MASTER interfaces
- Legacy Quotation must not:
  - embed catalog resolution rules directly
  - bypass SHARED contracts by reading CIM models directly (target state)

**Evidence required:** Boundary + consumption map (this section expanded with call paths during Phase 4).

---

### 6.10 MBOM Interface Contract (NSW-P4-S2-MBOM-001)

**Goal:** Define MBOM read/apply interface contract (no apply changes).

**Consumer:** Quotation V2 apply flow (`quotation.v2.applyMasterBom`)

**Contract: MbomApplyContract**
- **Inputs**:
  - masterBomId
  - quotationId
  - panelId (if required by apply flow; verify)
- **Outputs**:
  - stable response: `{ appliedCount, warnings[], errors[] }` (shape to be verified against current behavior)
- **Forbidden**:
  - changing apply behavior in S2
  - introducing Quotation-owned business rules into MBOM apply logic

**Evidence required:** Contract spec + forbidden callers list.

---

### 6.11 Feeder Interface Contract (NSW-P4-S2-FEED-001)

**Goal:** Define Feeder template interface contract for V2 apply.

**Consumer:** Quotation V2 apply flow (`quotation.v2.applyFeederTemplate`)

**Contract: FeederApplyContract**
- **Inputs**:
  - feederTemplateId
  - quotationId
  - panelId
- **Outputs**:
  - stable response: `{ appliedCount, warnings[], errors[] }`
- **Forbidden**:
  - changing apply behavior in S2

**Evidence required:** Contract spec + forbidden callers list.

---

### 6.12 Proposal BOM Interface Contract (NSW-P4-S2-PBOM-001)

**Goal:** Define Proposal BOM interface contract for V2 apply.

**Consumer:** Quotation V2 apply flow (`quotation.v2.applyProposalBom`)

**Contract: ProposalBomApplyContract**
- **Inputs**:
  - proposalBomId
  - quotationId
- **Outputs**:
  - stable response: `{ appliedCount, warnings[], errors[] }`
- **Forbidden**:
  - changing apply behavior in S2

**Evidence required:** Contract spec + forbidden callers list.

---

### 6.13 Quotation V2 Wrapper Seams (PROTECTED) (NSW-P4-S2-QUO-002)

**Goal:** Define wrapper/adaptor seams around V2 protected core.

**Protected scope anchors (ownership authority):**
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php` (PROTECTED)
- `source_snapshot/app/Services/CostingService.php` (PROTECTED)
- `source_snapshot/app/Services/QuotationQuantityService.php` (PROTECTED)

**Non-negotiable doctrine (Rulebook):**
- No direct edits to PROTECTED logic without G4 evidence + approvals.
- Allowed patterns: wrappers/adapters/decorators + controlled delegation.

#### Wrapper seam approach (planning-only)

- Introduce **outer wrapper classes** that own:
  - request validation standardization
  - dependency injection boundaries
  - cross-module orchestration (e.g., applying MBOM/FEED/PBOM)
- The PROTECTED core remains the delegated computation engine.

#### “No-Go” list (explicit)

- No direct modifications to:
  - `CostingService` logic (including SUM(AmountTotal) invariants)
  - `QuotationQuantityService` calculation logic
  - core V2 entity models listed as PROTECTED in `trace/phase_2/FILE_OWNERSHIP.md`

#### Allowed wrappers (to be implemented in Phase 4; names illustrative)

- `QuotationV2ApplyFacade` (handles apply flows, delegates into existing controller/service)
- `QuotationCostingFacade` (wrapper-only access to costing recalculation)
- `QuotationQuantityFacade` (wrapper-only access to qty recalculation)

**Evidence required:** Wrapper seam spec + no-go list (this section) plus approvals (Arch/Exec/Release) before any Phase 4 change that touches PROTECTED flows.

---

### 6.14 Costing/Quantity Protection Contract (PROTECTED) (NSW-P4-S2-QUO-003)

**Goal:** Specify strict contract for CostingService + QuantityService (wrapper-only).

**Authority anchors:**
- Protected services: `trace/phase_2/FILE_OWNERSHIP.md`
- Gate requirements: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md` (Bundle B)

#### Contract: CostingServiceWrapperContract

- **Allowed callers**: QUO wrappers only (no other modules)
- **Allowed call sites**:
  - V2 apply flows
  - V2 qty updates that require cost recalculation
- **Inputs**:
  - quotationId
  - scope identifiers (panelId/feederId/bomId) as needed
- **Outputs**:
  - totals snapshot (planning placeholder): `{ total, totalDiscounted, breakdown? }`
- **Invariants** (must remain true):
  - SUM(AmountTotal) roll-up preserved (as stated in FILE_OWNERSHIP notes)

#### Contract: QuantityServiceWrapperContract

- **Allowed callers**: QUO wrappers only
- **Inputs/Outputs**: qty changes and resulting normalized quantities, with stable error semantics
- **Invariants**:
  - quantity changes must remain consistent with costing recalculation expectations

**Evidence required:** Contract spec + allowed wrappers list + rollback validated (G4).

---

## 7. Task Card Stubs (Phase 4 Execution Entries; Planning Only)

These are structured per `docs/PHASE_3/04_TASK_REGISTER/TASK_CARD_TEMPLATE.md`.  
They remain **Planned** in Phase 3.

### NSW-P4-S2-GOV-001

- **Objective (1 sentence):** Convert S1 ownership exceptions into split/adapter task stubs ready for Phase 4 execution.
- **In Scope (explicit files):** `docs/PHASE_3/04_TASK_REGISTER/BATCH_1_S0_S1.md`, `trace/phase_2/FILE_OWNERSHIP.md`
- **Forbidden:** Any code edits
- **Entry Conditions:** S1 exceptions list exists (even if empty)
- **Exit Conditions:** Exception→Task mapping table completed (Section 6.1)
- **Cross-Module Touchpoints:** All modules
- **Test Bundle Required:** None (planning-only)
- **Rollback Plan:** Required in Phase 4 (task itself is governance planning)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.1 (completed table)
- **Status:** Planned

### NSW-P4-S2-GOV-002

- **Objective (1 sentence):** Publish canonical boundary blocks per module.
- **In Scope (explicit files):** This document Section 6.2
- **Forbidden:** Changing business logic
- **Entry Conditions:** ROUTE_MAP + FEATURE_CODE_MAP + FILE_OWNERSHIP available
- **Exit Conditions:** Boundary blocks approved and referenced by subsequent tasks
- **Cross-Module Touchpoints:** All modules
- **Test Bundle Required:** None (planning-only)
- **Rollback Plan:** Not required (planning-only)
- **Approvals Required:** Architectural
- **Evidence to Attach:** Section 6.2
- **Status:** Planned

### NSW-P4-S2-SHARED-001

- **Objective (1 sentence):** Declare stable shared contracts for dropdown APIs and reuse search.
- **In Scope (explicit):** Section 6.3 (contracts)
- **Forbidden:** Any functional change
- **Entry Conditions:** Shared endpoints list verified in ROUTE_MAP
- **Exit Conditions:** Contract doc approved and linked to split plan
- **Cross-Module Touchpoints:** Reuse + dropdown APIs (Legacy+V2)
- **Test Bundle Required:** Bundle C (Catalog Validity) and bundle impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.3
- **Status:** Planned

### NSW-P4-S2-SHARED-002

- **Objective (1 sentence):** Plan split for mixed-responsibility controllers with owner per method group.
- **In Scope (explicit):** Section 6.4
- **Forbidden:** Any file move now
- **Entry Conditions:** Ownership exceptions confirmed (S1)
- **Exit Conditions:** Split plan approved with method-group owners
- **Cross-Module Touchpoints:** Multiple modules (ImportController, QuotationController)
- **Test Bundle Required:** Bundle A/B/C impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.4
- **Status:** Planned

### NSW-P4-S2-MASTER-001

- **Objective (1 sentence):** Ensure MASTER exposes clean reference interfaces only.
- **In Scope (explicit):** Section 6.5
- **Forbidden:** UI changes
- **Entry Conditions:** MASTER routes confirmed in ROUTE_MAP
- **Exit Conditions:** Interface notes + forbidden access list approved
- **Cross-Module Touchpoints:** Quotation/Project
- **Test Bundle Required:** None (planning-only)
- **Rollback Plan:** Not required
- **Approvals Required:** Architectural
- **Evidence to Attach:** Section 6.5
- **Status:** Planned

### NSW-P4-S2-EMP-001

- **Objective (1 sentence):** Document and isolate Employee/Role security touchpoints as cross-cutting.
- **In Scope (explicit):** Section 6.6
- **Forbidden:** Security redesign
- **Entry Conditions:** ROUTE_MAP + FILE_OWNERSHIP available
- **Exit Conditions:** Touchpoint map approved
- **Cross-Module Touchpoints:** All modules
- **Test Bundle Required:** None (planning-only)
- **Rollback Plan:** Not required
- **Approvals Required:** Architectural
- **Evidence to Attach:** Section 6.6
- **Status:** Planned

### NSW-P4-S2-CIM-001

- **Objective (1 sentence):** Define hard boundary for ImportController split + adapter seam.
- **In Scope (explicit):** Section 6.8
- **Forbidden:** Any controller edits
- **Entry Conditions:** Import split verified (Batch-1 evidence)
- **Exit Conditions:** Isolation plan + adapter seam spec approved
- **Cross-Module Touchpoints:** MASTER/PDFContain
- **Test Bundle Required:** Bundle C impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.8
- **Status:** Planned

### NSW-P4-S2-CIM-002

- **Objective (1 sentence):** Plan removal of duplicate catalog resolution paths into a single canonical path.
- **In Scope (explicit):** Section 6.7
- **Forbidden:** Any pricing changes
- **Entry Conditions:** Shared endpoints list verified (ROUTE_MAP)
- **Exit Conditions:** Single-path resolution plan approved with deprecation order
- **Cross-Module Touchpoints:** Quotation Legacy + V2
- **Test Bundle Required:** Bundle C (Catalog Validity)
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.7
- **Status:** Planned

### NSW-P4-S2-MBOM-001

- **Objective (1 sentence):** Define MBOM read/apply interface contract (no apply changes).
- **In Scope (explicit):** Section 6.10
- **Forbidden:** Apply behavior change
- **Entry Conditions:** Apply touchpoints verified (Batch-1 evidence)
- **Exit Conditions:** Contract spec + forbidden callers approved
- **Cross-Module Touchpoints:** Quotation V2
- **Test Bundle Required:** Bundle A (Apply) impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.10
- **Status:** Planned

### NSW-P4-S2-FEED-001

- **Objective (1 sentence):** Define Feeder template interface contract for V2 apply.
- **In Scope (explicit):** Section 6.11
- **Forbidden:** Apply behavior change
- **Entry Conditions:** Apply touchpoints verified (Batch-1 evidence)
- **Exit Conditions:** Contract spec + forbidden callers approved
- **Cross-Module Touchpoints:** Quotation V2
- **Test Bundle Required:** Bundle A (Apply) impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.11
- **Status:** Planned

### NSW-P4-S2-PBOM-001

- **Objective (1 sentence):** Define Proposal BOM interface contract for V2 apply.
- **In Scope (explicit):** Section 6.12
- **Forbidden:** Apply behavior change
- **Entry Conditions:** Apply touchpoints verified (Batch-1 evidence)
- **Exit Conditions:** Contract spec + forbidden callers approved
- **Cross-Module Touchpoints:** Quotation V2
- **Test Bundle Required:** Bundle A (Apply) impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.12
- **Status:** Planned

### NSW-P4-S2-QUO-001

- **Objective (1 sentence):** Define legacy quotation boundaries; ensure it consumes masters via contracts.
- **In Scope (explicit):** Section 6.9
- **Forbidden:** Pricing logic changes
- **Entry Conditions:** Legacy routes/deps mapped (Batch-1 evidence)
- **Exit Conditions:** Boundary + consumption map approved
- **Cross-Module Touchpoints:** Shared endpoints (dropdown APIs)
- **Test Bundle Required:** Bundle C impacts evaluated in Phase 4
- **Rollback Plan:** Required (G3)
- **Approvals Required:** Architectural + Execution
- **Evidence to Attach:** Section 6.9
- **Status:** Planned

### NSW-P4-S2-QUO-002

- **Objective (1 sentence):** Define wrapper/adaptor seams around V2 protected core.
- **In Scope (explicit):** Section 6.13
- **Forbidden:** Any direct core edits
- **Entry Conditions:** Protected list + apply bundles verified (Batch-1 evidence)
- **Exit Conditions:** Wrapper seam spec + no-go list approved
- **Cross-Module Touchpoints:** MBOM/FEED/PBOM apply (Bundle A)
- **Test Bundle Required:** Bundle A + Bundle B (as applicable)
- **Rollback Plan:** Required and validated (G4)
- **Approvals Required:** Architectural + Execution + Release
- **Evidence to Attach:** Section 6.13
- **Status:** Planned

### NSW-P4-S2-QUO-003

- **Objective (1 sentence):** Specify strict wrapper-only contract for CostingService + QuantityService.
- **In Scope (explicit):** Section 6.14
- **Forbidden:** Any direct edits
- **Entry Conditions:** Protected services verified in FILE_OWNERSHIP
- **Exit Conditions:** Contract spec + allowed wrappers approved
- **Cross-Module Touchpoints:** All modules (because totals ripple)
- **Test Bundle Required:** Bundle B (Costing Integrity)
- **Rollback Plan:** Required and validated (G4)
- **Approvals Required:** Architectural + Execution + Release
- **Evidence to Attach:** Section 6.14
- **Status:** Planned


