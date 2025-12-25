# S2.4 — EMP Isolation Pack (Employee/Role Reference Interface Declaration)
#
# Task coverage:
# - NSW-P4-S2-EMP-001 (G2) Employee/Role touchpoints as cross-cutting
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase-4 execution.
- **No QUO‑V2 work** is authorized here (fenced by `NSW-P4-S2-QUO-REVERIFY-001`, G4).
- **No behavior change** in S2: only reference interfaces, boundaries, and forbidden access rules.
- **No route/controller moves** in S2: only planning and boundary declaration.
- **Routes canonical note:** In this snapshot, `/api/*` endpoints live in `routes/web.php` with `/api` prefix. Treat this as canonical until S4 propagation.

---

## 1) EMP Reference Interface Declaration

### 1.1 What EMP Exposes (Read-Only Reference Surfaces)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`, `trace/phase_2/ROUTE_MAP.md`

EMP exposes identity and authorization data to other modules as read-only consumption. CRUD routes are EMP-only UI flows. Other modules may only read via future contracts.

#### Employee/User (UserController)
- **Routes:** `user.*` (index, create, store, edit, update, destroy)
- **Purpose:** System user accounts, authentication credentials, user status (active/inactive)
- **Current consumers:** All modules (authentication/authorization via middleware; user references in audit/logging)
- **Reference surface:** User entity data (read-only for consumers)
- **Route ownership:** CRUD routes are owned and used only by EMP UI. Other modules may only read via future contracts.

#### Role/Permission (RoleController)
- **Routes:** `role.*` (index, create, store, edit, update, destroy)
- **Purpose:** Role definitions, JSON-based permission structure (RBAC)
- **Current consumers:** All modules (authorization checks; role-based access control)
- **Reference surface:** Role entity data and permission structure (read-only for consumers)
- **Route ownership:** CRUD routes are owned and used only by EMP UI. Other modules may only read via future contracts.

### 1.2 Cross-Cutting Nature (Authentication/Authorization)

**Important distinction:** EMP is fundamentally cross-cutting because:
- **Authentication:** All modules use `auth` middleware (requires User model)
- **Authorization:** All modules may check role permissions (requires Role model)
- **Audit/Logging:** Many modules reference current user for audit trails
- **UI Context:** Many views display user name, role, or permission-based UI elements

**Boundary statement:** While EMP is cross-cutting, direct table access by consumers is still forbidden. All access must route through declared reference interfaces.

---

## 2) Inbound Consumers (Inventory Only)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md` (cross-module references), `trace/phase_2/FEATURE_CODE_MAP.md`

### 2.1 CIM (Component/Item Master)
- **Consumption:** User references (audit/logging), role/permission checks (authorization)
- **Current state:** Direct model access via `auth` middleware; direct `User`/`Role` queries (to be migrated to contract in S4)
- **Future contract:** `EmployeeReferenceContract`, `RolePermissionReferenceContract`

### 2.2 MBOM (Master BOM)
- **Consumption:** User references (audit/logging), role/permission checks (authorization)
- **Current state:** Direct model access via `auth` middleware; direct `User`/`Role` queries (to be migrated to contract in S4)
- **Future contract:** `EmployeeReferenceContract`, `RolePermissionReferenceContract`

### 2.3 FEED (Feeder Library)
- **Consumption:** User references (audit/logging), role/permission checks (authorization)
- **Current state:** Direct model access via `auth` middleware; direct `User`/`Role` queries (to be migrated to contract in S4)
- **Future contract:** `EmployeeReferenceContract`, `RolePermissionReferenceContract`

### 2.4 PBOM (Proposal BOM)
- **Consumption:** User references (audit/logging), role/permission checks (authorization)
- **Current state:** Direct model access via `auth` middleware; direct `User`/`Role` queries (to be migrated to contract in S4)
- **Future contract:** `EmployeeReferenceContract`, `RolePermissionReferenceContract`

### 2.5 QUO (Quotation — Legacy + V2)
- **Consumption:** User references (audit/logging), role/permission checks (authorization)
- **Current state:** Direct model access via `auth` middleware; direct `User`/`Role` queries (to be migrated to contract in S4)
- **Future contract:** `EmployeeReferenceContract`, `RolePermissionReferenceContract`

### 2.6 All Other Modules (Cross-Cutting)
- **Consumption:** Authentication via `auth` middleware, authorization checks, audit references
- **Current state:** Direct model access via `auth` middleware (Laravel standard); direct `User`/`Role` queries where needed
- **Future contract:** `EmployeeReferenceContract`, `RolePermissionReferenceContract`

**Note:** The `auth` middleware itself is a Laravel framework component and is not subject to EMP isolation rules. However, any direct `User` or `Role` model queries outside middleware should migrate to contracts.

---

## 3) Forbidden Access Rules

### 3.1 No Direct Table Access
- **S2 rule:** No new direct table access introduced. Existing legacy direct access is tolerated but must be tracked.
- **S4 rule:** All known call sites migrate to contracts; remaining direct accesses are tracked as COMPAT with retirement plan.
- **Enforcement:** Code review + static analysis (S4+)
- **COMPAT exception format:** Any direct access that must temporarily remain must be logged as `DEC-EMP-DIRECT-ACCESS-<module>-001` in `PROJECT_DECISION_LOG.md` with retirement plan (S5 Bundle-C). Direct-access exceptions must also include a retirement date and Bundle-C verification reference.

### 3.2 No Cross-Module Writes
- **Rule:** EMP reference surfaces are read-only for external consumers
- **Enforcement:** Route-level authorization (EMP-owned routes only allow EMP UI flows)
- **Exception:** None (write operations are EMP-owned UI flows only)

### 3.3 No Auth/Permission Mutation Outside EMP
- **Rule:** No module may mutate user credentials, role assignments, or permission structures outside EMP-owned controllers
- **Enforcement:** Interface declaration (EMP only exposes reference data, not mutation logic)
- **Boundary:** User creation, role assignment, password changes are EMP-owned only

### 3.4 No Role Cache Duplication
- **Rule:** No module may implement local role/permission caching that diverges from EMP policy
- **Enforcement:** Contract-first access (all role/permission lookups must route through declared contracts)
- **Allowed cache:** Framework session/auth cache (Laravel standard)
- **Forbidden cache:** Module-owned shadow tables or persistent copies of role/permission data
- **Future:** If caching is needed, it must be implemented within EMP contract layer

---

## 4) Future Contract Candidates (Names Only, No Implementation)

**Planning statement:** These contracts will be designed and implemented in S3/S4. S2 only declares their names and intended scope.

### 4.1 EmployeeReferenceContract
- **Purpose:** Unified read-only reference surface for User/Employee master data
- **Scope:** User lookup (by ID, by email), user status checks, user metadata (name, email, status)
- **Consumers:** CIM, MBOM, FEED, PBOM, QUO (legacy + V2), and all other modules
- **Implementation:** S3 alignment, S4 propagation
- **Important:** `EmployeeReferenceContract` is **not** `user.*` CRUD routes. It is a new shared read-only surface (S3 freeze, S4 propagation).

### 4.2 RolePermissionReferenceContract
- **Purpose:** Unified read-only reference surface for Role and Permission (RBAC) data
- **Scope:** Role lookup (by ID, by name), permission checks (hasPermission(module, action)), role metadata
- **Consumers:** CIM, MBOM, FEED, PBOM, QUO (legacy + V2), and all other modules
- **Implementation:** S3 alignment, S4 propagation
- **Important:** `RolePermissionReferenceContract` is **not** `role.*` CRUD routes. It is a new shared read-only surface (S3 freeze, S4 propagation).

**Note:** These contracts are separate from authentication middleware (`auth`). The middleware remains a Laravel framework component. Contracts are for explicit user/role data lookups in business logic.

---

## 5) Explicit "No Moves in S2" Statement

**Hard fence:** No structural changes are authorized in S2.

### 5.1 No Controller Split
- **Current state:** `UserController` and `RoleController` are stable EMP-owned controllers
- **S2 action:** Only declare the reference surface boundaries
- **S2 forbidden:** No controller file moves, no route reassignments
- **Future:** Controller structure remains stable until S4+ after contract propagation

### 5.2 No Route Move
- **Current state:** EMP routes (`user.*`, `role.*`) are stable
- **S2 action:** Only document route ownership and reference surface boundaries
- **S2 forbidden:** No route name changes, no route file migrations
- **Future:** Route stability maintained until S4 propagation is complete

### 5.3 No Behavior Change
- **Current state:** EMP reference surfaces work as-is (direct model access by consumers via middleware and direct queries)
- **S2 action:** Only declare what should become contracts (planning-only)
- **S2 forbidden:** No migration of consumers to contracts, no interface implementation
- **Future:** Contract implementation and consumer migration happen in S3/S4

---

## 6) Trace Anchors

### 6.1 FILE_OWNERSHIP.md Rows (EMP-Owned Files)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`

| File | Owner | Feature | Risk | Notes |
|------|-------|---------|------|-------|
| `source_snapshot/app/Http/Controllers/UserController.php` | Employee/Role | Users | MEDIUM | User CRUD; authentication |
| `source_snapshot/app/Http/Controllers/RoleController.php` | Employee/Role | Roles | MEDIUM | Role CRUD; authorization |

**Cross-cutting note:**
- Employee/Role: Used by all modules (authentication/authorization via middleware). Security policies apply system-wide.

### 6.2 ROUTE_MAP.md Entries (EMP-Owned Routes)

**Authority:** `trace/phase_2/ROUTE_MAP.md`

**User routes (UserController):**
- `GET /user` → `user.index` → `UserController@index`
- `GET /user/create` → `user.create` → `UserController@create`
- `POST /user/create` → `user.store` → `UserController@store`
- `GET /user/{id}/edit` → `user.edit` → `UserController@edit`
- `PUT /user/{id}/edit` → `user.update` → `UserController@update`
- `DELETE /user/{id}/destroy` → `user.destroy` → `UserController@destroy`

**Role routes (RoleController):**
- `GET /role` → `role.index` → `RoleController@index`
- `GET /role/create` → `role.create` → `RoleController@create`
- `POST /role/create` → `role.store` → `RoleController@store`
- `GET /role/{id}/edit` → `role.edit` → `RoleController@edit`
- `PUT /role/{id}/edit` → `role.update` → `RoleController@update`
- `DELETE /role/{id}/destroy` → `role.destroy` → `RoleController@destroy`

### 6.3 Database Touchpoints

**Authority:** `trace/phase_2/FEATURE_CODE_MAP.md`

- **Tables:** `users`, `roles`
- **Models:** `User`, `Role`
- **Cross-module usage:** All modules (authentication/authorization via middleware)

---

## Evidence / Approvals Checklist (G2)

- [ ] Architectural approval: EMP reference interface declaration accepted
- [ ] Architectural approval: Forbidden access rules accepted
- [ ] Execution approval: No behavior change; no QUO-V2 scope crossed
- [ ] Execution approval: No controller split; no route moves; no consumer migration
- [ ] Trace anchors verified: FILE_OWNERSHIP.md and ROUTE_MAP.md entries confirmed
- [ ] Cross-cutting nature documented: Authentication/authorization boundaries clear

---

## References (Authority)

- `trace/phase_2/FILE_OWNERSHIP.md` (EMP-owned controllers: UserController, RoleController)
- `trace/phase_2/ROUTE_MAP.md` (EMP-owned routes: user.*, role.*)
- `trace/phase_2/FEATURE_CODE_MAP.md` (Employee/Role module structure, database touchpoints)
- `features/employee/README.md` (EMP module overview)
- `features/employee/_general/12_USER_MANAGEMENT.md` (User and role management details)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (SHARED contract surface reference)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (S2 fences + order)

---

## Evidence

**Authority References:**
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md` (EMP-owned controller rows: UserController, RoleController)
- Route Map: `trace/phase_2/ROUTE_MAP.md` (EMP-owned route entries: user.*, role.*)
- Feature Code Map: `trace/phase_2/FEATURE_CODE_MAP.md` (Employee/Role module structure, database touchpoints)

**Evidence Pointers:**
- Controller file list: `UserController.php`, `RoleController.php`
- Route names touched: `user.*`, `role.*`
- Database tables: `users`, `roles`
- Output doc: `docs/PHASE_4/S2_EMP_ISOLATION.md`

**Gate Satisfied By:**
- Reference interface declaration complete (read-only surfaces, forbidden write paths)
- Inbound consumers inventoried (CIM, MBOM, FEED, PBOM, QUO, all modules)
- Forbidden access rules specified (S2 vs S4 enforcement)
- Future contract candidates declared (names only, no implementation)
- No moves statement explicit (no controller split, no route moves, no behavior change)
- Trace anchors verified (FILE_OWNERSHIP.md rows, ROUTE_MAP.md entries, FEATURE_CODE_MAP.md references)
- Cross-cutting nature documented (authentication/authorization boundaries)

---

## Task Status

**NSW-P4-S2-EMP-001:** ✅ Complete

**Exit Criteria Met:**
- ✅ Document exists (`docs/PHASE_4/S2_EMP_ISOLATION.md`)
- ✅ Boundaries are explicit (read-only reference surfaces, forbidden write paths)
- ✅ Consumers inventoried (CIM, MBOM, FEED, PBOM, QUO, all modules)
- ✅ Forbidden access rules specified (no direct table access, no cross-module writes, no auth/permission mutation)
- ✅ Future contract names declared (EmployeeReferenceContract, RolePermissionReferenceContract)
- ✅ Trace anchors verified (FILE_OWNERSHIP.md rows, ROUTE_MAP.md entries)
- ✅ Evidence link added to Master Task List

**Next Tasks:** S2.5 MBOM-001 (with cleaner EMP reference surface foundation)

---

**Last Updated:** 2025-12-18  
**Status:** ACTIVE (Execution Support)

