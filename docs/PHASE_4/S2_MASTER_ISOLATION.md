# S2.4 — MASTER Isolation Pack (Reference Interface Declaration)
#
# Task coverage:
# - NSW-P4-S2-MASTER-001 (G2) Master reference interface declaration
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase-4 execution.
- **No QUO‑V2 work** is authorized here (fenced by `NSW-P4-S2-QUO-REVERIFY-001`, G4).
- **No behavior change** in S2: only reference interfaces, boundaries, and forbidden access rules.
- **No pricing formula changes** (explicitly forbidden in S2; pricing is PROTECTED/controlled elsewhere).
- **Routes canonical note:** In this snapshot, `/api/*` endpoints live in `routes/web.php` with `/api` prefix. Treat this as canonical until S4 propagation.

---

## 1) MASTER Reference Interface Declaration

### 1.1 What MASTER Exposes (Read-Only Reference Surfaces)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`, `trace/phase_2/ROUTE_MAP.md`

MASTER exposes reference data to other modules as read-only consumption, but CRUD routes are MASTER-only UI flows. Other modules may only read via future contracts.

#### Organization Master (OrganizationController)
- **Routes:** `organization.*` (index, create, store, edit, update, destroy)
- **Purpose:** Company/organization definitions, addresses, GST information, letterhead data
- **Current consumers:** Project, Quotation (legacy + V2)
- **Reference surface:** Organization entity data (read-only for consumers)
- **Route ownership:** CRUD routes are owned and used only by MASTER UI. Other modules may only read via future contracts.

#### Vendor Master (VendorController)
- **Routes:** `vendor.*` (index, create, store, edit, update, destroy)
- **Purpose:** Vendor/manufacturer master data
- **Current consumers:** Component/Item Master (Make/Brand concept), Quotation (pricing references)
- **Reference surface:** Vendor entity data (read-only for consumers)
- **Route ownership:** CRUD routes are owned and used only by MASTER UI. Other modules may only read via future contracts.
- **Route naming note:** Route group uses `vendor.*` naming though URI prefix is `/vendors`.

#### PDF Container Settings (ImportController@pdfcontain — split ownership)
- **Routes:** `pdfcontain.*` (index, save)
- **Purpose:** PDF format/layout configuration (settings table)
- **Owner:** MASTER (PDF Formats)
- **Split note:** Implemented in `ImportController` (shared with CIM import routes)
- **Reference surface:** PDF container configuration (read-only for consumers; write via declared contract only)
- **Adapter seam:** See `docs/PHASE_4/S2_CIM_ISOLATION.md` (PdfContainSettingsContract)

### 1.2 What MASTER Must Never Expose (Forbidden Write Paths)

**Hard boundaries (enforced by isolation):**

1. **No direct table access by consumers**
   - Consumers must not query `organizations`, `vendors`, or `settings` tables directly
   - All access must route through declared reference interfaces

2. **No pricing/BOM mutation paths**
   - MASTER does not expose pricing calculation logic
   - MASTER does not expose BOM structure mutation (MBOM owns that)
   - MASTER does not expose quotation costing logic

3. **No cross-module writes**
   - MASTER reference surfaces are **read-only** for external consumers
   - Write operations (create/update/delete) are MASTER-owned UI flows only
   - No module may trigger MASTER entity mutations via API calls

4. **No settings reads except via declared contracts**
   - PDF container settings must be accessed via `PdfContainSettingsContract` (see CIM isolation)
   - No direct `Setting` model queries by consumers
   - Future settings contracts must be declared before use

---

## 2) Inbound Consumers (Inventory Only)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md` (cross-module references)

### 2.1 CIM (Component/Item Master)
- **Consumption:** Vendor/Make references (vendor master data)
- **Current state:** Direct model access (to be migrated to contract in S4)
- **Future contract:** `MasterReferenceContract` (vendor lookup surface)

### 2.2 MBOM (Master BOM)
- **Consumption:** Organization references (if BOM templates reference org data)
- **Current state:** Direct model access (to be verified in execution)
- **Future contract:** `MasterReferenceContract` (organization lookup surface)

### 2.3 FEED (Feeder Library)
- **Consumption:** Organization/Vendor references (if feeder templates reference master data)
- **Current state:** Direct model access (to be verified in execution)
- **Future contract:** `MasterReferenceContract` (organization/vendor lookup surface)

### 2.4 PBOM (Proposal BOM)
- **Consumption:** Organization references (proposal BOMs may reference org data)
- **Current state:** Direct model access (to be verified in execution)
- **Future contract:** `MasterReferenceContract` (organization lookup surface)

### 2.5 QUO (Quotation — Legacy + V2)
- **Consumption:**
  - **Legacy:** Organization references (quotation headers, letterheads)
  - **V2:** Organization references (quotation headers, letterheads)
  - **Both:** Vendor references (pricing context)
- **Current state:** Direct model access (to be migrated to contract in S4)
- **Future contract:** `MasterReferenceContract` (organization/vendor lookup surface)

---

## 3) Forbidden Access Rules

### 3.1 No Direct Table Access
- **S2 rule:** No new direct table access introduced. Existing legacy direct access is tolerated but must be tracked.
- **S4 rule:** All known call sites migrate to contracts; remaining direct accesses are tracked as COMPAT with retirement plan.
- **Enforcement:** Code review + static analysis (S4+)
- **COMPAT exception format:** Any direct access that must temporarily remain must be logged as `DEC-MASTER-DIRECT-ACCESS-<module>-001` in `PROJECT_DECISION_LOG.md` with retirement plan (S5 Bundle-C).

### 3.2 No Settings Reads Except Via Declared Contracts
- **Rule:** PDF container settings must be accessed via `PdfContainSettingsContract` only
- **Enforcement:** Adapter seam contract (see `docs/PHASE_4/S2_CIM_ISOLATION.md`)
- **Future settings:** Any new settings surface must declare a contract before use

### 3.3 No Cross-Module Writes
- **Rule:** MASTER reference surfaces are read-only for external consumers
- **Enforcement:** Route-level authorization (MASTER-owned routes only allow MASTER UI flows)
- **Exception:** None (write operations are MASTER-owned UI flows only)

### 3.4 No Pricing/BOM Mutation Paths
- **Rule:** MASTER does not expose pricing calculation or BOM structure mutation
- **Enforcement:** Interface declaration (MASTER only exposes reference data, not business logic)
- **Boundary:** Pricing logic is PROTECTED (QUO-V2); BOM mutation is MBOM-owned

---

## 4) Future Contract Candidates (Names Only, No Implementation)

**Planning statement:** These contracts will be designed and implemented in S3/S4. S2 only declares their names and intended scope.

### 4.1 MasterReferenceContract
- **Purpose:** Unified read-only reference surface for Organization and Vendor master data
- **Scope:** Organization lookup, Vendor lookup (by ID, by name search)
- **Consumers:** CIM, MBOM, FEED, PBOM, QUO (legacy + V2)
- **Implementation:** S3 alignment, S4 propagation
- **Important:** `MasterReferenceContract` is **not** `organization.*` or `vendor.*` CRUD routes. It is a new shared read-only surface (S3 freeze, S4 propagation).

### 4.2 MasterSettingsContract (If Needed Later)
- **Purpose:** General settings lookup surface (beyond PDF container)
- **Scope:** TBD (only if additional settings surfaces are required)
- **Consumers:** TBD
- **Implementation:** TBD (may not be needed if PdfContainSettingsContract is sufficient)

**Note:** PDF container settings are already covered by `PdfContainSettingsContract` (see `docs/PHASE_4/S2_CIM_ISOLATION.md`). This contract is a placeholder for future settings surfaces only.

---

## 5) Explicit "No Moves in S2" Statement

**Hard fence:** No structural changes are authorized in S2.

### 5.1 No Controller Split
- **Current state:** `ImportController` contains both CIM import routes and MASTER PDF container routes
- **S2 action:** Only declare the split boundary (see `docs/PHASE_4/S2_CIM_ISOLATION.md`)
- **S2 forbidden:** No controller file moves, no route reassignments
- **Future:** Controller split will happen in S4+ after contract propagation

### 5.2 No Route Move
- **Current state:** MASTER routes (`organization.*`, `vendor.*`, `pdfcontain.*`) are stable
- **S2 action:** Only document route ownership and reference surface boundaries
- **S2 forbidden:** No route name changes, no route file migrations
- **Future:** Route stability maintained until S4 propagation is complete

### 5.3 No Behavior Change
- **Current state:** MASTER reference surfaces work as-is (direct model access by consumers)
- **S2 action:** Only declare what should become contracts (planning-only)
- **S2 forbidden:** No migration of consumers to contracts, no interface implementation
- **Future:** Contract implementation and consumer migration happen in S3/S4

---

## 6) Trace Anchors

### 6.1 FILE_OWNERSHIP.md Rows (MASTER-Owned Files)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`

| File | Owner | Feature | Risk | Notes |
|------|-------|---------|------|-------|
| `source_snapshot/app/Http/Controllers/OrganizationController.php` | Master | Organization | MEDIUM | Organization CRUD operations; master data |
| `source_snapshot/app/Http/Controllers/VendorController.php` | Master | Vendor | MEDIUM | Vendor CRUD operations; master data |
| `source_snapshot/app/Http/Controllers/ImportController.php` | Component/Item Master + Master | Import/Export + PDF Formats | HIGH | Split ownership: Import routes (CIM) + pdfcontain (Master/PDF); touches settings table |

**Split ownership note:**
- ImportController: Split between Component/Item Master (import routes) and Master (pdfcontain routes). Changes require coordination.

### 6.2 ROUTE_MAP.md Entries (MASTER-Owned Routes Only)

**Authority:** `trace/phase_2/ROUTE_MAP.md`

**Organization routes (OrganizationController):**
- `GET /organization` → `organization.index` → `OrganizationController@index`
- `GET /organization/create` → `organization.create` → `OrganizationController@create`
- `POST /organization/create` → `organization.store` → `OrganizationController@store`
- `GET /organization/{id}/edit` → `organization.edit` → `OrganizationController@edit`
- `PUT /organization/{id}/edit` → `organization.update` → `OrganizationController@update`
- `DELETE /organization/{id}/destroy` → `organization.destroy` → `OrganizationController@destroy`

**Vendor routes (VendorController):**
- `GET /vendors` → `vendor.index` → `VendorController@index`
- `GET /vendors/create` → `vendor.create` → `VendorController@create`
- `POST /vendors/create` → `vendor.store` → `VendorController@store`
- `GET /vendors/{id}/edit` → `vendor.edit` → `VendorController@edit`
- `PUT /vendors/{id}/edit` → `vendor.update` → `VendorController@update`
- `DELETE /vendors/{id}/destroy` → `vendor.destroy` → `VendorController@destroy`

**PDF container routes (ImportController — split ownership):**
- `GET /pdfcontain` → `pdfcontain.index` → `ImportController@pdfcontain`
- `PUT /pdfcontain` → `pdfcontain.save` → `ImportController@pdfcontainsave`

**Note:** PDF container routes are documented here for completeness, but the adapter seam specification is in `docs/PHASE_4/S2_CIM_ISOLATION.md` (CIM isolation step).

---

## Evidence / Approvals Checklist (G2)

- [ ] Architectural approval: MASTER reference interface declaration accepted
- [ ] Architectural approval: Forbidden access rules accepted
- [ ] Execution approval: No behavior change; no QUO-V2 scope crossed
- [ ] Execution approval: No controller split; no route moves; no consumer migration
- [ ] Trace anchors verified: FILE_OWNERSHIP.md and ROUTE_MAP.md entries confirmed

---

## References (Authority)

- `trace/phase_2/FILE_OWNERSHIP.md` (MASTER-owned controllers: OrganizationController, VendorController, ImportController split)
- `trace/phase_2/ROUTE_MAP.md` (MASTER-owned routes: organization.*, vendor.*, pdfcontain.*)
- `docs/PHASE_4/S2_CIM_ISOLATION.md` (PdfContainSettingsContract adapter seam)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (SHARED contract surface reference)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (S2 fences + order)
- `features/master/README.md` (MASTER module overview)

---

## Evidence

**Authority References:**
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md` (MASTER-owned controller rows)
- Route Map: `trace/phase_2/ROUTE_MAP.md` (MASTER-owned route entries: organization.*, vendor.*, pdfcontain.*)

**Evidence Pointers:**
- Controller/service file list: `OrganizationController.php`, `VendorController.php`, `ImportController.php` (split ownership)
- Route names touched: `organization.*`, `vendor.*`, `pdfcontain.*`
- Output doc: `docs/PHASE_4/S2_MASTER_ISOLATION.md`

**Gate Satisfied By:**
- Reference interface declaration complete (read-only surfaces, forbidden write paths)
- Inbound consumers inventoried (CIM, MBOM, FEED, PBOM, QUO)
- Forbidden access rules specified (S2 vs S4 enforcement)
- Future contract candidates declared (names only, no implementation)
- No moves statement explicit (no controller split, no route moves, no behavior change)
- Trace anchors verified (FILE_OWNERSHIP.md rows, ROUTE_MAP.md entries)

---

## Task Status

**NSW-P4-S2-MASTER-001:** ✅ Complete

**Exit Criteria Met:**
- ✅ Document exists (`docs/PHASE_4/S2_MASTER_ISOLATION.md`)
- ✅ Boundaries are explicit (read-only reference surfaces, forbidden write paths)
- ✅ No overlap with CIM/MBOM contracts (PDF container seam documented in CIM isolation)
- ✅ Evidence link added to Master Task List

**Next Tasks:** S2.4 EMP-001 (Employee/Role touchpoints), then S2.5 MBOM-001 (with cleaner MASTER reference surface)

---

