# Phase 6 Scope Gap Analysis
## Critical Missing Foundation Workflows

**Date:** 2025-01-27  
**Status:** CRITICAL GAP IDENTIFIED  
**Priority:** HIGH - Blocks full software functionality

---

## 🚨 Executive Summary

**User Concern:** Phase 6 plan appears focused on upgrading/folding NEPL quotation v2, but the actual scope should be creating a **full new software from scratch** starting from the foundational entities.

**Current Phase 6 Focus:** Quotation management, panels, feeders, BOMs, costing  
**Missing:** Complete foundational workflow from organization → customer → contact → project → quotation

**Impact:** Users cannot create quotations without first creating organizations, customers, contacts, and projects. This is a **critical workflow gap**.

---

## 📋 Complete Workflow (What Should Be Covered)

### Full Software Workflow Hierarchy

```
1. Organization Creation
   └─> 2. Customer Creation (belongs to Organization)
        └─> 3. Contact Person Creation (belongs to Customer)
             └─> 4. Project Creation (belongs to Customer)
                  └─> 5. Quotation Creation (belongs to Project)
                       ├─> 5a. Copy from other quotation (Track A-R)
                       ├─> 5b. Create panel
                       ├─> 5c. Copy panel
                       │    └─> 6. Create feeder OR copy feeder
                       │         └─> 7. Create item/parent BOM/child BOM
                       │              ├─> 7a. Create from master BOM
                       │              ├─> 7b. Copy from proposal BOM
                       │              ├─> 7c. Copy from item master
                       │              └─> 7d. Edit copy BOM
                       └─> 8. All cost rules related to the same
```

---

## 🔍 Current Phase 6 Coverage Analysis

### ✅ What Phase 6 Covers

| Entity | API Endpoints | UI/Workflow | Status |
|--------|--------------|-------------|--------|
| **Quotations** | ✅ `/api/v1/quotation/*` | ✅ Track A: Quotation overview, panel management | ✅ COVERED |
| **Panels** | ✅ Via quotation endpoints | ✅ Track A: Panel details, add panel | ✅ COVERED |
| **Feeders** | ✅ Via quotation endpoints | ✅ Track A: Feeder list, add feeder | ✅ COVERED |
| **BOMs** | ✅ `/api/v1/bom/*` | ✅ Track A: BOM hierarchy tree view | ✅ COVERED |
| **Items** | ✅ Via BOM endpoints | ✅ Track A: Component/item list display | ✅ COVERED |
| **Catalog** | ✅ `/api/v1/catalog/*` | ✅ Track B: Catalog import UI | ✅ COVERED |
| **Pricing** | ✅ `/api/v1/pricing/*` | ✅ Track A: Pricing resolution UX | ✅ COVERED |
| **Costing** | ✅ Track D0 + Track D | ✅ Track D: Costing Pack, dashboards | ✅ COVERED |
| **Reuse** | ✅ Track A-R | ✅ Track A-R: Copy quotation/panel/feeder/BOM | ✅ COVERED |

### ❌ What Phase 6 Does NOT Cover

| Entity | API Endpoints | UI/Workflow | Status |
|--------|--------------|-------------|--------|
| **Organizations** | ❌ **MISSING** | ❌ **MISSING** | ❌ **NOT COVERED** |
| **Customers** | ❌ **MISSING** | ❌ **MISSING** | ❌ **NOT COVERED** |
| **Contacts** | ❌ **MISSING** | ❌ **MISSING** | ❌ **NOT COVERED** |
| **Projects** | ❌ **MISSING** | ❌ **MISSING** | ❌ **NOT COVERED** |

---

## 🔴 Critical Gaps Identified

### Gap 1: Organization Management

**What's Missing:**
- API endpoints for CRUD operations on organizations
- UI for creating/editing organizations
- Organization list/search functionality
- Organization → Customer relationship management

**Impact:**
- Users cannot create organizations
- Cannot group customers by organization
- Breaks the hierarchy: Organization → Customer → Project → Quotation

**Required Work:**
1. **Backend API:**
   - `POST /api/v1/organizations` - Create organization
   - `GET /api/v1/organizations` - List organizations
   - `GET /api/v1/organizations/{id}` - Get organization details
   - `PUT /api/v1/organizations/{id}` - Update organization
   - `DELETE /api/v1/organizations/{id}` - Delete organization (soft delete)

2. **Frontend UI:**
   - Organization list page
   - Organization create/edit form
   - Organization selection in customer creation

3. **Database Schema:**
   - Verify `organizations` table exists in Schema Canon v1.0
   - Ensure relationships are properly defined

---

### Gap 2: Customer Management

**What's Missing:**
- API endpoints for CRUD operations on customers
- UI for creating/editing customers
- Customer list/search functionality
- Customer → Organization relationship
- Customer → Contact relationship
- Customer → Project relationship

**Impact:**
- Users cannot create customers
- Cannot link customers to organizations
- Cannot create projects without customers
- Cannot create quotations without customers

**Required Work:**
1. **Backend API:**
   - `POST /api/v1/customers` - Create customer
   - `GET /api/v1/customers` - List customers (with filters: organization_id, search)
   - `GET /api/v1/customers/{id}` - Get customer details
   - `PUT /api/v1/customers/{id}` - Update customer
   - `DELETE /api/v1/customers/{id}` - Delete customer (soft delete)

2. **Frontend UI:**
   - Customer list page
   - Customer create/edit form
   - Organization selection in customer form
   - Customer selection in project/quotation forms

3. **Database Schema:**
   - Verify `customers` table exists in Schema Canon v1.0
   - Ensure `organization_id` FK is present
   - Ensure `customer_name_snapshot` field exists (for D-009)

---

### Gap 3: Contact Person Management

**What's Missing:**
- API endpoints for CRUD operations on contacts
- UI for creating/editing contacts
- Contact list/search functionality
- Contact → Customer relationship
- Contact selection in quotations

**Impact:**
- Users cannot create contact persons
- Cannot assign contacts to customers
- Cannot select contact person when creating quotations

**Required Work:**
1. **Backend API:**
   - `POST /api/v1/customers/{customer_id}/contacts` - Create contact
   - `GET /api/v1/customers/{customer_id}/contacts` - List contacts for customer
   - `GET /api/v1/contacts/{id}` - Get contact details
   - `PUT /api/v1/contacts/{id}` - Update contact
   - `DELETE /api/v1/contacts/{id}` - Delete contact (soft delete)

2. **Frontend UI:**
   - Contact list page (filtered by customer)
   - Contact create/edit form
   - Customer selection in contact form
   - Contact selection in quotation form

3. **Database Schema:**
   - Verify `contacts` table exists in Schema Canon v1.0
   - Ensure `customer_id` FK is present

---

### Gap 4: Project Management

**What's Missing:**
- API endpoints for CRUD operations on projects
- UI for creating/editing projects
- Project list/search functionality
- Project → Customer relationship
- Project → Quotation relationship
- Auto-generated project numbers (YYMMDD### format)

**Impact:**
- Users cannot create projects
- Cannot link quotations to projects
- Breaks the hierarchy: Customer → Project → Quotation

**Required Work:**
1. **Backend API:**
   - `POST /api/v1/customers/{customer_id}/projects` - Create project
   - `GET /api/v1/customers/{customer_id}/projects` - List projects for customer
   - `GET /api/v1/projects/{id}` - Get project details
   - `PUT /api/v1/projects/{id}` - Update project
   - `DELETE /api/v1/projects/{id}` - Delete project (soft delete)
   - Auto-generate `project_no` (YYMMDD### format)

2. **Frontend UI:**
   - Project list page (filtered by customer)
   - Project create/edit form
   - Customer selection in project form
   - Project selection in quotation form

3. **Database Schema:**
   - Verify `projects` table exists in Schema Canon v1.0
   - Ensure `customer_id` FK is present
   - Ensure `project_no` field with unique constraint

---

## 📊 Workflow Comparison

### Current Phase 6 Assumption (INCORRECT)

```
[Assumes these exist] → Quotation Creation → Panel → Feeder → BOM → Items
```

### Actual Required Workflow (CORRECT)

```
Organization Creation
  └─> Customer Creation
       └─> Contact Person Creation
            └─> Project Creation
                 └─> Quotation Creation
                      ├─> Copy from other quotation
                      ├─> Create panel
                      ├─> Copy panel
                      └─> [Rest of quotation workflow...]
```

---

## 🎯 Required Additions to Phase 6

### New Track: Track F - Foundation Entities Management

**Purpose:** Build complete CRUD workflows for organizations, customers, contacts, and projects

**Duration:** 3-4 weeks  
**Tasks:** ~20 tasks

#### Week 1: Organization & Customer Management (6 tasks)

1. **P6-FOUND-001:** Design organization management UI
   - Organization list page
   - Organization create/edit form
   - Organization → Customer relationship display

2. **P6-FOUND-002:** Implement organization API endpoints
   - `POST /api/v1/organizations`
   - `GET /api/v1/organizations`
   - `GET /api/v1/organizations/{id}`
   - `PUT /api/v1/organizations/{id}`
   - `DELETE /api/v1/organizations/{id}`

3. **P6-FOUND-003:** Implement organization UI
   - Organization list page
   - Organization create/edit form
   - Integration with customer creation

4. **P6-FOUND-004:** Design customer management UI
   - Customer list page (with organization filter)
   - Customer create/edit form
   - Customer → Contact/Project relationship display

5. **P6-FOUND-005:** Implement customer API endpoints
   - `POST /api/v1/customers`
   - `GET /api/v1/customers` (with filters: organization_id, search)
   - `GET /api/v1/customers/{id}`
   - `PUT /api/v1/customers/{id}`
   - `DELETE /api/v1/customers/{id}`
   - Ensure `customer_name_snapshot` handling (D-009)

6. **P6-FOUND-006:** Implement customer UI
   - Customer list page
   - Customer create/edit form
   - Organization selection dropdown
   - Integration with project/quotation creation

#### Week 2: Contact & Project Management (6 tasks)

7. **P6-FOUND-007:** Design contact person management UI
   - Contact list page (filtered by customer)
   - Contact create/edit form

8. **P6-FOUND-008:** Implement contact API endpoints
   - `POST /api/v1/customers/{customer_id}/contacts`
   - `GET /api/v1/customers/{customer_id}/contacts`
   - `GET /api/v1/contacts/{id}`
   - `PUT /api/v1/contacts/{id}`
   - `DELETE /api/v1/contacts/{id}`

9. **P6-FOUND-009:** Implement contact UI
   - Contact list page
   - Contact create/edit form
   - Customer selection
   - Integration with quotation creation

10. **P6-FOUND-010:** Design project management UI
    - Project list page (filtered by customer)
    - Project create/edit form
    - Project number auto-generation display

11. **P6-FOUND-011:** Implement project API endpoints
    - `POST /api/v1/customers/{customer_id}/projects`
    - `GET /api/v1/customers/{customer_id}/projects`
    - `GET /api/v1/projects/{id}`
    - `PUT /api/v1/projects/{id}`
    - `DELETE /api/v1/projects/{id}`
    - Auto-generate `project_no` (YYMMDD### format)

12. **P6-FOUND-012:** Implement project UI
    - Project list page
    - Project create/edit form
    - Customer selection
    - Project number display (auto-generated)
    - Integration with quotation creation

#### Week 3: Integration & Workflow (5 tasks)

13. **P6-FOUND-013:** Integrate foundation entities into quotation creation
    - Organization selection in quotation form
    - Customer selection (filtered by organization)
    - Contact selection (filtered by customer)
    - Project selection (filtered by customer)
    - Ensure proper hierarchy validation

14. **P6-FOUND-014:** Implement foundation entity search/filter
    - Search organizations by name
    - Search customers by name/organization
    - Search contacts by name/customer
    - Search projects by name/customer

15. **P6-FOUND-015:** Implement foundation entity relationships display
    - Show customers under organization
    - Show contacts under customer
    - Show projects under customer
    - Show quotations under project

16. **P6-FOUND-016:** End-to-end workflow test
    - Create organization → customer → contact → project → quotation
    - Verify all relationships work correctly
    - Verify data integrity

17. **P6-FOUND-017:** Foundation entity validation & error handling
    - Validate required fields
    - Validate relationships (customer must belong to organization, etc.)
    - User-friendly error messages
    - Integration with error taxonomy (B3)

#### Week 4: Polish & Documentation (3 tasks)

18. **P6-FOUND-018:** Foundation entity UI polish
    - Improve form layouts
    - Add loading states
    - Add success/error notifications
    - Improve navigation flow

19. **P6-FOUND-019:** Foundation entity documentation
    - API documentation
    - User guide for creating organizations/customers/contacts/projects
    - Workflow diagrams

20. **P6-FOUND-020:** Foundation entity testing
    - Unit tests for API endpoints
    - Integration tests for workflows
    - E2E tests for complete hierarchy creation

---

## 📈 Impact on Phase 6 Timeline

### Current Phase 6 Timeline: 10-12 weeks

### Revised Timeline with Track F: 13-16 weeks

**Additional Time:** +3-4 weeks for Track F

**Critical Path Impact:**
- Track F must complete **before** Track A (Quotation UI) can fully function
- Track F Week 1-2 can run in parallel with Track E (Database implementation)
- Track F Week 3-4 must complete before Track A Week 1-2

---

## 🔗 Dependencies

### Track F Dependencies

**Depends On:**
- Track E (Database): Schema Canon v1.0 must include `organizations`, `customers`, `contacts`, `projects` tables
- Track E (Database): Relationships must be properly defined

**Required By:**
- Track A (Quotation UI): Cannot create quotations without customers/projects
- Track A-R (Reuse): Copy quotation requires source quotation to have valid customer/project

---

## ✅ Verification Checklist

### Schema Canon Verification

**Status:** ✅ VERIFIED (2025-01-27)

- [x] `customers` table exists in Schema Canon v1.0 ✅
  - [x] `customer_name_snapshot` field exists (for D-009) ✅
  - [ ] `organization_id` FK exists ❌ **MISSING** (organizations table not in Schema Canon)
- [x] `projects` table exists in Schema Canon v1.0 ✅
  - [x] `customer_id` FK exists ✅
  - [x] `project_no` field with unique constraint ✅
- [ ] `organizations` table exists in Schema Canon v1.0 ❌ **MISSING**
- [ ] `contacts` table exists in Schema Canon v1.0 ❌ **MISSING**
  - [ ] `customer_id` FK exists ❌ **MISSING**

**Critical Finding:** Schema Canon v1.0 includes `customers` and `projects` tables, but **does NOT include** `organizations` and `contacts` tables. This is a **Schema Canon gap** that must be addressed.

### API Endpoint Verification

- [ ] Organization CRUD endpoints exist
- [ ] Customer CRUD endpoints exist
- [ ] Contact CRUD endpoints exist
- [ ] Project CRUD endpoints exist

### UI Workflow Verification

- [ ] Organization creation UI exists
- [ ] Customer creation UI exists
- [ ] Contact creation UI exists
- [ ] Project creation UI exists
- [ ] Quotation creation integrates with all foundation entities

---

## 🎯 Recommendations

### Immediate Actions Required

1. **Review Schema Canon v1.0**
   - Verify `organizations`, `customers`, `contacts`, `projects` tables exist
   - If missing, this is a Phase 5 issue (Schema Canon incomplete)

2. **Add Track F to Phase 6 Scope**
   - Add Track F: Foundation Entities Management (3-4 weeks, ~20 tasks)
   - Update Phase 6 timeline to 13-16 weeks
   - Update task count from ~133 to ~153 tasks

3. **Prioritize Track F**
   - Track F must start in Week 0-1 (parallel with Track E)
   - Track F must complete before Track A Week 1-2

4. **Update Phase 6 Documentation**
   - Update `PHASE_6_COMPLETE_SCOPE_AND_TASKS.md` with Track F
   - Update execution plan with Track F timeline
   - Update exit criteria to include foundation entity workflows

### Alternative Approach (Schema Canon Missing Tables - CONFIRMED)

**Status:** Schema Canon v1.0 is **missing** `organizations` and `contacts` tables.

**Required Actions:**

1. **Phase 5.5: Schema Canon Extension (REQUIRED)**
   - Add `organizations` table to Schema Canon
   - Add `contacts` table to Schema Canon
   - Add `organization_id` FK to `customers` table
   - Add `customer_id` FK to `contacts` table
   - Update Schema Canon to v1.1
   - Go through Phase 5 decision process for schema changes
   - **OR** Document decision to defer organizations/contacts to Phase 7

2. **Then Proceed with Track F in Phase 6**
   - If organizations/contacts added to Schema Canon → Full Track F implementation
   - If organizations/contacts deferred → Simplified Track F (customers + projects only)

---

## 📝 Conclusion

**Critical Finding:** Phase 6 scope is **incomplete** without foundation entity management (organizations, customers, contacts, projects).

**User's Concern is VALID:** The full software workflow must start from organization creation, not quotation creation.

**Required Action:** Add Track F (Foundation Entities Management) to Phase 6 scope, or verify these entities are handled elsewhere (e.g., in Phase 5 or pre-existing system).

**Impact:** Without Track F, users cannot create quotations, making Phase 6 deliverables non-functional for end-to-end workflows.

---

**Document Status:** DRAFT - Requires review and decision on Track F inclusion  
**Next Steps:** 
1. Review Schema Canon v1.0 for foundation entity tables
2. Decide on Track F inclusion in Phase 6
3. Update Phase 6 scope and timeline accordingly
