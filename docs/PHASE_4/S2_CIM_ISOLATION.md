# S2.3 — CIM Isolation Pack (Import Split + Catalog Single-Path Plan)
#
# Task coverage:
# - NSW-P4-S2-CIM-001 (G3) Import split isolation (CIM vs MASTER/PDF) + adapter seam spec
# - NSW-P4-S2-CIM-002 (G3) Catalog resolution single-path plan (no execution)
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- Planning-only isolation for Phase-4 execution.
- **No QUO-V2 work** is authorized here (fenced by `NSW-P4-S2-QUO-REVERIFY-001`, G4).
- **No behavior change** in S2: only seams, boundaries, contracts, and split plans.
- **No pricing formula changes** (explicitly forbidden in S2; pricing is PROTECTED/controlled elsewhere).
- **Routes canonical note:** In this snapshot, `/api/*` endpoints live in `routes/web.php` with `/api` prefix. Treat this as canonical until S4 propagation.

---

## 1) Import Split Isolation (CIM vs MASTER/PDF) — NSW-P4-S2-CIM-001

### 1.1 Current reality (trace + code anchors)

**Primary mixed-responsibility controller:**
- `source_snapshot/app/Http/Controllers/ImportController.php`

**Authority: FILE_OWNERSHIP.md (ImportController row):**

| source_snapshot/app/Http/Controllers/ImportController.php | Controller | Component/Item Master + Master | Import/Export + PDF Formats | HIGH | Split ownership: Import routes (Component/Item Master) + pdfcontain (Master/PDF); touches settings table (pdfcontain) | Review required | import.* (Component/Item Master), pdfcontain.* (Master) |

**Authority: FILE_OWNERSHIP.md (split ownership note):**

- ImportController: Split between Component/Item Master (import routes) and Master (pdfcontain routes). Changes require coordination.

### 1.2 Route inventory (ROUTE_MAP.md) — same controller, different owners

**CIM-owned Import/Export/Temp staging routes (ImportController):**

| GET | /import | import.view | auth | ImportController@importview | Component/Item Master | Import/Export | - | import/index.blade.php | Import view |
| GET | /importview/{uuid} | product.tempview | auth | ImportController@importtempview | Component/Item Master | Import/Export | - | import/tempview.blade.php | Temp view |
| POST | /importview | product.importtemadd | auth | ImportController@importtemadd | Component/Item Master | Import/Export | - | - | Add temp |
| GET | /importview/{id}/delete | product.importtemdestroy | auth | ImportController@importtemdestroy | Component/Item Master | Import/Export | - | - | Delete temp |
| POST | /import | import.add | auth | ImportController@importadd | Component/Item Master | Import/Export | - | - | Import add |
| POST | /export | export.exportsample | auth | ImportController@exportsample | Component/Item Master | Import/Export | - | - | Export sample |

**MASTER-owned PDF container routes (same controller, different owner):**

| GET | /pdfcontain | pdfcontain.index | auth | ImportController@pdfcontain | Master | PDF Formats | - | pdfcontain/index.blade.php | PDF container - Controller name is misleading (ImportController). Feature is Master/PDF container. |
| PUT | /pdfcontain | pdfcontain.save | auth | ImportController@pdfcontainsave | Master | PDF Formats | - | - | Save PDF container - Controller name is misleading (ImportController). Feature is Master/PDF container. |

### 1.3 Boundary statement (hard fence for Phase-4)

- CIM import flow must not "reach into" MASTER/PDF behavior or settings.
- MASTER/PDF container must not depend on CIM import internals.
- Any shared utilities required between them must be accessed via **explicit seam / contract** (below).

### 1.4 Adapter seam specification (planning-only)

**Contract name:** `PdfContainSettingsContract`  
**Owner:** MASTER  
**Consumers:** MASTER/PDF UI; (optional later) quotation PDF generation; CIM only if explicitly required  
**Forbidden:** direct `Setting` reads/writes inside CIM-owned import code once the contract exists.

**Contract scope (minimal, v1):**
- `getPdfContainConfig(): array`
- `savePdfContainConfig(payload: array): void`

**Error rules:**
- Fail closed (return default config) if settings row missing.
- Do not leak DB schema; return canonical config keys only.

### 1.5 Planned split (no moves in S2)

**Plan (execution in later stages, not S2):**
- Create:
  - `CimImportController` (CIM owner; `import.*`, `product.temp*`, `export.*`)
  - `MasterPdfContainController` (MASTER owner; `pdfcontain.*`)
- Keep **route names stable** until S4 propagation is complete.
- In S2: only declare the seam, owner boundaries, and file move plan.

**Deliverable expectation:** After split, FILE_OWNERSHIP should list:
- `CimImportController` → CIM owner
- `MasterPdfContainController` → MASTER owner
- `PdfContainSettingsContract` → MASTER owner, SHARED-allowed as a consumer surface if needed later

---

## 2) Catalog Resolution Single-Path Plan — NSW-P4-S2-CIM-002

### 2.1 Goal

Eliminate duplicate catalog resolution paths by converging on **one canonical lookup surface**:

- **CIM owns data + resolution logic**
- **SHARED owns the contract surface** (see `docs/PHASE_4/S2_SHARED_ISOLATION.md`)
- Consumers (CIM/MBOM/FEED/PBOM/QUO) must use the SHARED contract after S4 propagation.

### 2.2 Current duplication (known paths)

**Path A — SHARED dropdown APIs (contract target)**
- Currently implemented inside QUO's controller surface (legacy structure).
- Contract target: **CatalogLookupContract** (SHARED).

**Path B — Module-local AJAX lookup endpoints (duplicate resolution)**

**CIM Product lookup routes (ROUTE_MAP.md):**

| GET | /product/getsubcategory/{id} | product.getsubcategory | auth | ProductController@getsubcategory | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /product/getproducttype/{id} | product.getproducttype | auth | ProductController@getproducttype | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /product/getgeneric | product.getgeneric | auth | ProductController@getgeneric | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /product/getseries | product.getseries | auth | ProductController@getseries | Component/Item Master | Specific Product | - | - | AJAX lookup |

**MBOM lookup helper routes (ROUTE_MAP.md) — still catalog resolution:**

| GET | /masterbom/getsubcategory/{id} | masterbom.getsubcategory | auth | MasterBomController@getsubcategory | Master BOM | Items | - | - | AJAX lookup |
| GET | /masterbom/getproducttype/{id} | masterbom.getproducttype | auth | MasterBomController@getproducttype | Master BOM | Items | - | - | AJAX lookup |
| GET | /masterbom/getdescription | masterbom.getdescription | auth | MasterBomController@getdescription | Master BOM | Items | - | - | AJAX lookup |

*Note: These MBOM lookup routes are inventory only in S2; consumers migrate to CatalogLookupContract only in S4; deletion happens only after Bundle C passes in S5.*

### 2.3 Single-path target (planning statement)

- All dropdown/search resolution for:
  - Category → Subcategory
  - Category → Items/Types
  - Category/Item → Products
  - Product → Makes
  - Make → Series
  - Product → Descriptions
…must route through SHARED **CatalogLookupContract**, implemented against CIM-owned master data.

### 2.4 Deprecation discipline (no execution in S2)

S2 delivers only the plan:

1) **Inventory** all catalog lookup endpoints and classify each as:
- **Canonical:** keep (CatalogLookupContract)
- **Compat:** temporary bridge (allowed only until S5 Bundle C is green)
- **Duplicate:** remove later

2) Removal happens only after:
- S4 propagation confirms zero consumers on deprecated routes
- S5 **Bundle C (Catalog Validity)** passes

### 2.4.1 Catalog Lookup Route Classification Table (S2 output)

| Route Name | URI | Current Owner (as-is) | Classification | Migration Plan | Notes |
|------------|-----|----------------------|----------------|----------------|-------|
| api.category.subcategories | /api/category/{categoryId}/subcategories | QUO (implementation) / SHARED (contract target) | CANONICAL | Keep route; move implementation to SHARED controller later | Canonical contract surface (CatalogLookupContract) |
| api.category.items | /api/category/{categoryId}/items | QUO / SHARED target | CANONICAL | Keep; migrate consumers to contract in S4 | |
| api.category.products | /api/category/{categoryId}/products | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| api.item.products | /api/item/{itemId}/products | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| api.product.makes | /api/product/{productId}/makes | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| api.make.series | /api/make/{makeId}/series | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| api.product.descriptions | /api/product/{productId}/descriptions | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| api.category.makes | /api/category/{categoryId}/makes | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| api.makes | /api/makes | QUO / SHARED target | CANONICAL | Keep; migrate consumers in S4 | |
| product.getsubcategory | /product/getsubcategory/{id} | CIM | COMPAT | S4: migrate CIM UI to CatalogLookupContract; then remove in S5 after Bundle-C | Keep temporarily to avoid breaking Product UI before propagation |
| product.getproducttype | /product/getproducttype/{id} | CIM | COMPAT | Same as above | Likely maps to CatalogLookupContract "items/types" surface |
| product.getgeneric | /product/getgeneric | CIM | COMPAT | Same as above | Generic selection must be reconciled to L0/L1 rules (no semantic drift) |
| product.getseries | /product/getseries | CIM | COMPAT | Same as above | Must align to Make→Series contract |
| masterbom.getsubcategory | /masterbom/getsubcategory/{id} | MBOM | COMPAT | S4: migrate MBOM UI to CatalogLookupContract; remove in S5 after Bundle-C | Inventory-only in S2; do not delete now |
| masterbom.getproducttype | /masterbom/getproducttype/{id} | MBOM | COMPAT | Same as above | |
| masterbom.getdescription | /masterbom/getdescription | MBOM | COMPAT | Same as above | Must align to Product→Descriptions contract |
| (future discovered) | (any other /{module}/get lookup)* | Any module | DUPLICATE (default) | Do not create new; convert to COMPAT only if required | Any new lookup endpoint requires decision log + justification |

**Classification rules:**
- **CANONICAL** = CatalogLookupContract `/api/*` routes only.
- **COMPAT** = temporary module-local endpoints that must be removed after S4 propagation + S5 Bundle-C pass.
- **DUPLICATE** = any new/non-essential lookup endpoints not required to keep UI running during migration.

### 2.5 Guardrails (to prevent silent drift)

- No module may rely on extra fields not declared in CatalogLookupContract.
- No caller may assume internal ORM field names from CIM tables.
- Any route still serving compat endpoints must be flagged in S5 regression matrix (Bundle C).
- **Governance rule:** Any new COMPAT endpoint creation is forbidden unless logged in `PROJECT_DECISION_LOG.md` as `DEC-COMPAT-<route>-001` with justification + retirement plan (S5 Bundle-C).

---

## Evidence / Approvals Checklist (G3)

- [ ] Architectural approval: split plan + `PdfContainSettingsContract` accepted
- [ ] Architectural approval: single-path catalog resolution target accepted
- [ ] Execution approval: no behavior change; no QUO-V2 scope crossed
- [ ] Rollback placeholder recorded for later controller moves (S4+)

---

## References (Authority)

- `trace/phase_2/FILE_OWNERSHIP.md` (ImportController split ownership)
- `trace/phase_2/ROUTE_MAP.md` (Import routes + pdfcontain routes + product lookup routes + masterbom lookup routes)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (CatalogLookupContract ownership + SHARED contract surface)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (S2 fences + order)

---

## Task Status

- NSW-P4-S2-CIM-001: ✅ Complete
- NSW-P4-S2-CIM-002: 🔄 In Progress
