# S2 GOV-002: Canonical Boundary Blocks

**Task ID:** NSW-P4-S2-GOV-002  
**Status:** ✅ Complete  
**Gate:** G3  
**Risk:** HIGH  
**Date:** 2025-12-18

---

## Objective

Create canonical "who can call whom" declarations for each module to define allowed callers, forbidden access patterns, and adapter seams.

---

## Boundary Block Definition

Boundary Blocks define:
- **Allowed Callers** (modules)
- **Allowed Entry Points** (routes/controllers/services)
- **Forbidden Callers** (modules)
- **Forbidden Access Patterns** (e.g., "direct model reads across module boundary")
- **Adapter/Wrappers** (the only permitted bypass mechanism)

---

## Authority Anchors

- Route-to-module map: `trace/phase_2/ROUTE_MAP.md`
- Code-to-feature map: `trace/phase_2/FEATURE_CODE_MAP.md`
- Risk/ownership: `trace/phase_2/FILE_OWNERSHIP.md`

---

## Boundary Blocks by Module

### SHARED (Cross-Module Utilities + APIs)

**Module Owns:**
- Cross-module utility endpoints/contracts
- Catalog lookup APIs (to be extracted from QUO)
- Reuse search APIs (to be extracted from QUO)
- Shared deletion policies

**Module May Call:**
- CIM models (via contract, read-only for catalog data)
- Other module models (via contracts only, no direct access)

**Module Must Not Call:**
- Business logic in other modules
- Protected services (CostingService, QuotationQuantityService) directly

**Allowed Cross-Module Entrypoints:**
- `CatalogLookupContract` endpoints:
  - `api.category.subcategories`
  - `api.category.items`
  - `api.category.products`
  - `api.item.products`
  - `api.product.makes`
  - `api.make.series`
  - `api.product.descriptions`
  - `api.category.makes`
  - `api.makes`
- `ReuseSearchContract` endpoints:
  - `api.reuse.*`

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Adding new "shared" endpoints inside unrelated modules without SHARED contract + ownership
- Cross-module code reading other module models directly (outside contracts)
- Direct access to PROTECTED services

**Adapter Seams:**
- `CatalogLookupContract` (defined in S2_SHARED_ISOLATION.md)
- `ReuseSearchContract` (defined in S2_SHARED_ISOLATION.md)

---

### MASTER (Org/Vendor/PDF)

**Module Owns:**
- Organization CRUD
- Vendor CRUD
- PDF container formats (Settings table access)

**Module May Call:**
- No external module dependencies (reference data provider)

**Module Must Not Call:**
- CIM business logic
- Quotation business logic
- Other module internals

**Allowed Cross-Module Entrypoints:**
- `organization.*` routes (read-only for other modules)
- `vendor.*` routes (read-only for other modules)
- `pdfcontain.*` routes (CIM import may access via adapter)

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Any module directly mutating Master tables outside Master-owned controllers/services
- Reusing Master/PDF settings logic via CIM import flows (must be adapter-only)

**Adapter Seams:**
- `PdfContainSettingsContract` for PDF container access (read/write scoping)

---

### EMP (Employee/Role)

**Module Owns:**
- User management
- Role management
- Authentication/authorization policies

**Module May Call:**
- No external module dependencies (cross-cutting concern)

**Module Must Not Call:**
- Business logic modules
- Data modules directly

**Allowed Cross-Module Entrypoints:**
- `role.*` routes (authorization touchpoints)
- `user.*` routes (authentication touchpoints)
- Authorization middleware/policies

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Any module implementing local authorization rules that diverge from EMP policy/middleware
- Any "role cache" duplication without an EMP-owned contract

**Adapter Seams:**
- `AuthorizationTouchpointMap` (documentation boundary, not code)

---

### CIM (Component/Item Master)

**Module Owns:**
- Category, Subcategory, Item (ProductType), Attribute CRUD
- Product (Generic/Specific) CRUD
- Make, Series CRUD
- Price list management
- Import/export for products (CIM portion)
- Catalog data integrity

**Module May Call:**
- SHARED CatalogLookupContract (for exposing catalog data)
- MASTER PdfContainSettingsContract (via adapter, for import)

**Module Must Not Call:**
- Quotation business logic directly
- BOM logic directly
- Protected services

**Allowed Cross-Module Entrypoints:**
- CRUD routes: `category.*`, `subcategory.*`, `item.*`, `make.*`, `series.*`, `attribute.*`, `product.*`, `price.*`
- Import routes: `import.*` (CIM portion only)
- Catalog lookup via SHARED contract

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Quotation directly "knowing" CIM model structure (direct model reads across boundary) once contracts exist
- Any pricing logic changes as part of S2 (explicitly forbidden)
- Direct access to other module's protected services

**Adapter Seams:**
- `CatalogLookupContract` (consumer/provider via SHARED)
- Import split adapter seam (for PDF settings access)

---

### MBOM (Master BOM)

**Module Owns:**
- Master BOM CRUD
- Master BOM template structure
- Master BOM item relationships

**Module May Call:**
- SHARED CatalogLookupContract (for catalog lookups)
- SHARED ReuseSearchContract (for reuse searches)

**Module Must Not Call:**
- Quotation V2 logic directly
- Protected services directly

**Allowed Cross-Module Entrypoints:**
- `masterbom.*` routes
- Apply touchpoint: `quotation.v2.applyMasterBom` (as consumer, via contract)

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Any module directly mutating MBOM internals (tables/structure) outside MBOM controllers/services
- Any behavior change to apply as part of S2 (planning-only)

**Adapter Seams:**
- `MbomApplyContract` (for V2 apply operations)

---

### FEED (Feeder Library)

**Module Owns:**
- Feeder template CRUD
- Feeder template structure
- Feeder item relationships

**Module May Call:**
- SHARED CatalogLookupContract (for catalog lookups)
- SHARED ReuseSearchContract (for reuse searches)

**Module Must Not Call:**
- Quotation V2 logic directly
- Protected services directly

**Allowed Cross-Module Entrypoints:**
- `feeder-library.*` routes
- Apply touchpoint: `quotation.v2.applyFeederTemplate` (as consumer, via contract)

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Any module directly mutating FEED internals outside FEED controllers/services
- Any apply behavior change as part of S2 (planning-only)

**Adapter Seams:**
- `FeederApplyContract` (for V2 apply operations)

---

### PBOM (Proposal BOM)

**Module Owns:**
- Proposal BOM CRUD
- Proposal BOM structure
- Proposal BOM item relationships
- Proposal BOM to Master BOM promotion

**Module May Call:**
- SHARED CatalogLookupContract (for catalog lookups)
- SHARED ReuseSearchContract (for reuse searches)
- MBOM (via promotion contract, future)

**Module Must Not Call:**
- Quotation V2 logic directly
- Protected services directly

**Allowed Cross-Module Entrypoints:**
- `proposal-bom.*` routes
- Apply touchpoint: `quotation.v2.applyProposalBom` (as consumer, via contract)
- Search touchpoint: `api.proposalBom.search` (currently owned by QUO; must follow contract)

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Any module directly mutating PBOM internals outside PBOM controllers/services
- Any apply behavior change as part of S2 (planning-only)

**Adapter Seams:**
- `ProposalBomApplyContract` (for V2 apply operations)

---

### QUO (Quotation Legacy + V2)

**Module Owns:**
- Legacy quotation workflow
- V2 quotation workflow (PROTECTED)
- Quotation models (PROTECTED)
- CostingService (PROTECTED)
- QuotationQuantityService (PROTECTED)
- Discount rule services (PROTECTED)
- DeletionPolicyService (SHARED, but QUO-owned)
- Shared catalog lookup APIs (to be extracted to SHARED)
- Shared reuse search APIs (to be extracted to SHARED)

**Module May Call:**
- SHARED contracts (after extraction)
- BOM apply contracts (MBOM/FEED/PBOM)
- MASTER reference data (read-only)

**Module Must Not Call:**
- CIM models directly (must use SHARED contract)
- Other module internals directly

**Allowed Cross-Module Entrypoints:**
- Legacy routes: `quotation.*`
- V2 routes: `quotation.v2.*`, `reuse.*`, `api.reuse.*`
- Apply endpoints (consumer): `quotation.v2.applyMasterBom`, `quotation.v2.applyFeederTemplate`, `quotation.v2.applyProposalBom`

**Forbidden Direct DB Writes / Forbidden Service Calls:**
- Upstream modules calling Quotation internals as "services"
- Direct edits to PROTECTED V2 core and protected services outside wrapper seams
- Other modules calling CostingService/QuotationQuantityService directly

**Adapter Seams:**
- V2 wrapper seams (for apply operations)
- Costing/Quantity wrapper-only contract (for protected services)
- CatalogLookupContract extraction (to SHARED)
- ReuseSearchContract extraction (to SHARED)

---

## Evidence

**Authority References:**
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- Route Map: `trace/phase_2/ROUTE_MAP.md`
- Batch-2 Planning: `docs/PHASE_3/04_TASK_REGISTER/BATCH_2_S2.md` (Section 6.2)
- S1 Boundaries: `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md` (Section 3)

**Gate Satisfied By:**
- Boundary blocks defined for all modules
- Allowed/forbidden access patterns documented
- Adapter seams identified
- Cross-module entrypoints specified

---

**Task Status:** ✅ Complete  
**Next Task:** NSW-P4-S2-SHARED-001 (Shared Utility Contracts)

