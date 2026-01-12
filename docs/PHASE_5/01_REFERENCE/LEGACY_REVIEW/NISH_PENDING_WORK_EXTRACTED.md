# NISH Pending Work - Extracted Master List

**Date:** 2025-12-18  
**Source:** `/Users/nirajdesai/Projects/nish/` (actual codebase)  
**Purpose:** Consolidated pending work from nish folder for Phase-5 backlog merge  
**Status:** Ready for Phase-5 planning

---

## 📊 EXECUTIVE SUMMARY

**Total Pending Work:** ~100-120 hours  
**Categories:** 8 major areas  
**Priority Breakdown:**
- **Critical:** ~35 hours
- **High:** ~45 hours
- **Medium:** ~20 hours
- **Low:** ~10 hours

**Key Sources:**
- `COMPLETE_PENDING_WORK_AUDIT.md` (comprehensive)
- `PENDING_BACKEND_WORK.md` (backend-specific)
- `PENDING_UI_WORK.md` (UI-specific)
- `INTEGRATED_TODO_LIST.md` (sequential plan)
- `SPRINT4_UI_TODO_LIST.md` (Sprint-4 deferred UI)

---

## 🔴 CRITICAL PRIORITY (Must Do)

### 1. Security Hardening Phase 1 ⏸️ **PARTIALLY COMPLETE**

**Status:** 2/8 tasks complete (Quotation ✅, Project ✅)  
**Reference:** `SECURITY_HARDENING_PHASE1.md`  
**Total Effort:** 13-15 hours (2-3 hours completed, 10-12 hours remaining)

#### Completed:
- ✅ Form Request Validation - Quotation (StoreQuotationRequest, UpdateQuotationRequest)
- ✅ Form Request Validation - Project (StoreProjectRequest, UpdateProjectRequest)

#### Pending:
1. **Form Request Validation - Remaining** (1-2 hours)
   - Product, Client, Price controllers
   - Create Form Request classes
   - Remove manual validation

2. **Dynamic Field Sanitization** (2 hours)
   - Audit all `$request->$dynamicField` usage
   - Add `filter_var()` validation
   - Add database existence checks

3. **CSRF Verification** (2 hours)
   - Audit all Blade views for `@csrf`
   - Check all AJAX calls have token
   - Verify meta tag in layouts

4. **Rate Limiting** (2 hours)
   - Configure throttle middleware
   - Apply to login (5 attempts/minute)
   - Apply to AJAX (60/minute)

5. **Transaction Wrappers** (2 hours)
   - Wrap critical operations in transactions
   - Add try-catch blocks
   - Test rollback scenarios

6. **Audit Logging** (1 hour)
   - Log critical operations
   - Test logs written correctly

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (security hardening doesn't touch locked routes/contracts)

---

### 2. Sprint-4 UI Components ⏸️ **ON HOLD**

**Status:** Backend 100% complete, UI 0% complete  
**Reference:** `SPRINT4_PROGRESS_REVIEW.md`, `SPRINT4_UI_TODO_LIST.md`  
**Total Effort:** ~25-35 hours

**Backend Status:** ✅ All APIs ready (12/12 tickets complete)

#### Pending UI Components (10 tasks):

1. **S4-07: Discount Rules Table** (4-6 hours)
   - File: `resources/views/quotation/v2/discount_rules/_panel.blade.php`
   - Use `nepl-standard-table` class
   - Show rules with priority ordering
   - Actions: Edit, Delete, Toggle Status

2. **S4-08: Add/Edit Rule Modal** (5-7 hours)
   - File: `resources/views/quotation/v2/discount_rules/_rule_modal.blade.php`
   - Form with all rule fields
   - Scope type selector (GLOBAL, MAKE, MAKE_SERIES, PRODUCT_TYPE, PRODUCT)
   - Conditional fields based on scope
   - Select2 for dropdowns

3. **S4-09: Preview Modal** (3-4 hours)
   - File: `resources/views/quotation/v2/discount_rules/_preview_modal.blade.php`
   - Show preview summary
   - Show sample matches
   - Show FIXED items sample
   - Override manual checkbox

4. **S4-10: Apply Rules Action** (2-3 hours)
   - Apply button in UI
   - Confirmation dialog
   - Success/error notifications
   - Refresh table after apply

5. **S4-15: Reset Button** (2-3 hours)
   - Reset button (only visible when audit exists)
   - Confirmation dialog
   - Success/error notifications

6. **S4-16: Make Selector** (1 hour)
   - Select2 dropdown
   - Load from lookup endpoint

7. **S4-17: Series Selector** (1-2 hours)
   - Select2 dropdown
   - Filtered by Make (AJAX dependency)

8. **S4-18: Product Type Selector** (1 hour)
   - Select2 dropdown
   - Load from lookup endpoint

9. **S4-19: Product Selector** (1-2 hours)
   - Select2 dropdown
   - Searchable, min 2 chars

10. **JavaScript Integration** (3-4 hours)
    - File: `public/js/quotation_discount_rules.js`
    - Select2 initialization
    - Make → Series dependency
    - AJAX form submissions
    - Table refresh
    - Modal handling

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (UI-only, backend APIs already exist)

---

### 3. Phase 1 Backend Tasks ⏸️ **PARTIALLY COMPLETE**

**Status:** 1/3 Complete (Discount fix ✅, BOM Identity ✅, Guardrails ✅ but testing pending)  
**Reference:** `INTEGRATED_TODO_LIST.md`  
**Total Effort:** 6-8 hours remaining (testing only)

#### Completed:
- ✅ Task 1.1: Discount Calculation Bug Fix
- ✅ Task 1.2: BOM Instance Identity Enhancement (migration, model, controller updated)
- ✅ Task 1.3: Validation Guardrails Implementation (all 7 guardrails implemented)

#### Pending:
1. **Task 1.3: Validation Guardrails Testing** (6-8 hours)
   - Test G1: Master BOM rejects ProductId
   - Test G2: Production BOM requires ProductId
   - Test G3: IsPriceMissing normalizes Amount
   - Test G4: RateSource consistency
   - Test G5: UNRESOLVED normalizes values
   - Test G6: FIXED_NO_DISCOUNT forces Discount=0
   - Test G7: All discounts are percentage-based

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (testing only, no behavior changes)

---

## 🟡 HIGH PRIORITY (Should Do)

### 4. Phase 2: Discount Application Table ⏸️ **PENDING**

**Status:** Not started  
**Reference:** `FINAL_CONSOLIDATED_IMPLEMENTATION_PLAN.md`  
**Total Effort:** 5-8 days (40-64 hours)

#### Backend Tasks (24-40 hours):
1. **Task 2.1: Enhance Discount Table Schema** (2 hours)
   - Migration + Model updates
   - Note: `quotation_discount_rules` is new system, `quotation_discounts` is legacy

2. **Task 2.2: Discount Resolution Service** (2-3 days / 16-24 hours)
   - File: `app/Services/QuotationDiscountService.php` (new)
   - Rule matching logic
   - Priority system

3. **Task 2.4: Bulk Apply Functionality** (1-2 days / 8-16 hours)
   - Service + Controller
   - Bulk operations

#### UI Tasks (16-24 hours):
4. **Task 2.3: Discount Application UI** (2-3 days / 16-24 hours)
   - Views + Controllers
   - Rule management interface

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (new feature, doesn't touch locked contracts)

---

### 5. Phase 3: Customer/Division/Contact ⏸️ **PENDING**

**Status:** Not started  
**Reference:** `FINAL_CONSOLIDATED_IMPLEMENTATION_PLAN.md`  
**Total Effort:** 3-4 days (24-32 hours)

#### Backend Tasks (16-24 hours):
1. **Task 3.1: Database Schema** (1 day / 8 hours)
   - Migration files

2. **Task 3.2: Models & Relationships** (1 day / 8 hours)
   - Model files

3. **Task 3.3: Controllers & Routes** (1 day / 8 hours)
   - Controller files

#### UI Tasks (8 hours):
4. **Task 3.4: UI Forms & Lists** (1 day / 8 hours)
   - View files
   - Form layouts
   - List views

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (new feature)

---

### 6. UI Standardization Global Audit ⏸️ **IN PROGRESS**

**Status:** 7/29+ pages complete  
**Reference:** `UI_STANDARDIZATION_GLOBAL_AUDIT.md`  
**Total Effort:** 15-20 hours (estimated)

#### Completed Pages (7):
- ✅ Make
- ✅ Series
- ✅ Category
- ✅ Product
- ✅ Product Type (Item)
- ✅ Generic
- ✅ Attribute

#### Pending Pages (22+):
**High Priority (11 pages):**
1. SubCategory
2. Client
3. Contact
4. Project
5. Quotation (list page)
6. Master BOM
7. Price List
8. User
9. Role
10. Employee
11. Company

**Medium Priority (11+ pages):**
- Catalog Health
- Catalog Cleanup
- Other admin/management pages

**Standardization Requirements:**
- Dual Search & Filters (all in ONE input-group)
- Table Styling (`nepl-standard-table` class)
- Font Styles (`nepl-page-title`, `nepl-small-text`)
- Colors (consistent color scheme)
- Filter Types (Select2 dropdowns, client-side filtering)
- No Full Page Reloads (AJAX updates only)
- Table Layout (`table-layout: auto` with `min-width`)

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (UI-only changes)

---

## 🟢 MEDIUM PRIORITY (Nice to Have)

### 7. Phase 4-6: Backend Features ⏸️ **PENDING**

**Status:** Not started  
**Reference:** `FINAL_CONSOLIDATED_IMPLEMENTATION_PLAN.md`  
**Total Effort:** 15-19 days (120-152 hours)

#### Phase 4: Revision Workflow Wizard (8-10 days / 64-80 hours)
- Revision tracking
- Make/Series change wizard
- Comparison UI
- Approval workflow

#### Phase 5: PDF Template Versioning (3-4 days / 24-32 hours)
- Template storage
- Version management
- Template selection UI
- PDF generation integration

#### Phase 6: Accessory Dependency Rules (4-5 days / 32-40 hours)
- Dependency schema
- Validation rules
- Auto-suggestion UI
- Conflict resolution

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (new features)

---

### 8. Documentation Gaps ⏸️ **PENDING**

**Status:** Some gaps identified  
**Reference:** `MASTER_ACTION_PLAN_V2.md`  
**Total Effort:** 10-15 hours

#### Critical Gaps (HIGH PRIORITY):
1. **44_BACKUP_RESTORE.md** (3-4 hours)
   - Database backup strategy
   - Automated backup scripts
   - File backup procedures
   - Restore procedures
   - Disaster recovery plan
   - **Status:** Draft ready, needs customization

2. **45_ENVIRONMENT_SETUP.md** (3-4 hours)
   - Prerequisites (PHP, MySQL, Composer, Node)
   - Clone and install
   - Database setup
   - .env configuration
   - First user creation
   - **Status:** Needs creation

3. **47_TEST_STRATEGY.md** (3-4 hours)
   - Test file examples
   - QuotationTest.php example
   - CalculationsTest.php example
   - **Status:** Draft ready, needs customization

#### Important Gaps (MEDIUM PRIORITY):
4. **46_ERROR_HANDLING.md** (2-3 hours)
5. **48_RELEASE_PROCESS.md** (3 hours)

#### Optional Gaps (LOW PRIORITY):
6. **49_LOGGING_MONITORING.md**
7. **50_MIGRATION_GUIDE.md** (Laravel upgrade)
8. **51_INTEGRATION_GUIDE.md** (NS Ware)

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (documentation only)

---

### 9. Code TODOs (In Code Comments) ⏸️ **PENDING**

**Status:** Various TODOs in codebase  
**Total Effort:** 2-4 hours

#### In Controllers:
1. **QuotationV2Controller.php** (3 TODOs)
   - Line 2084: `// TODO: recompute panel totals if needed`
   - Line 2153: `// TODO: if you want, recalc panel totals here (rate/amount)`
   - Line 2220: `// TODO: if you want, recalc panel totals here (rate/amount)`

2. **CatalogHealthController.php** (1 TODO)
   - Line 543: `// TODO: Implement after Step B1 (Attribute Schema UI per ProductType)`

3. **QuotationController.php** (1 TODO)
   - Line 98: `// TODO: Add when QuotationStatus field exists`

4. **HomeController.php** (2 TODOs)
   - Line 225: `// TODO: Add when status field exists`
   - Line 233: `// TODO: Add when status field exists`

#### In Services:
5. **DeletionPolicyService.php** (4 TODOs)
   - Lines 49, 123, 191, 250: `// TODO: Add IsLocked field check when database field is added`

#### In Views:
6. **panel.blade.php** (2 TODOs)
   - Line 2323: `// TODO: Create dedicated BOM edit modal/page later`
   - Line 2881: `// TODO: Collect form data and save via stepupdate route`

7. **_masterbom_modal.blade.php** (1 TODO)
   - Line 208: `// TODO: Send to backend to save`

**Phase-4 Governance:** Mixed - some `SAFE_FOR_PHASE_5`, some may touch protected areas (needs review)

---

### 10. Sprint-3 Polish Items ⏸️ **ON HOLD**

**Status:** On hold  
**Reference:** `SPRINT4_PROGRESS_REVIEW.md`  
**Total Effort:** 4 hours

#### Tasks:
1. **S4-20: Fix Blank Square Button** (1 hour)
   - File: `resources/views/quotation/v2/panel.blade.php`
   - Action: Remove or convert to Panel Actions dropdown

2. **S4-21: Remove Duplicate Add Feeder** (1 hour)
   - File: `resources/views/quotation/v2/_feeder.blade.php`
   - Action: Remove Add Feeder from feeder cards (keep only in panel header)

3. **S4-22: Add Discount Icon Tooltips** (2 hours)
   - File: `resources/views/quotation/v2/_items_table.blade.php`
   - Action: Add tooltips for discount icons:
     - 🏷️ Pricelist source
     - ✏️ Manual override
     - 🔒 Fixed/no discount
     - ⚠️ Missing price / unresolved
     - 🧮 Discount applied

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (UI polish only)

---

### 11. Add Component Button Fix ⏸️ **PENDING**

**Status:** Removed (to be re-implemented)  
**Reference:** `SPRINT4_UI_TODO_LIST.md`  
**Total Effort:** 2-3 hours

**Files Affected:**
- `resources/views/quotation/steppopup.blade.php`
- `resources/views/quotation/linepopup.blade.php`
- `resources/views/quotation/step.blade.php`

**Requirements:**
- Add "Add Component" button to `steppopup.blade.php` (existing panels)
- Add "Add Component" button to `linepopup.blade.php` (new panels)
- Create `addComponentDirectly()` function in `step.blade.php`
- Button should create empty BOM and allow adding components
- Follow existing button patterns and styling

**Note:** This was previously fixed but removed during restoration. Needs to be re-implemented.

**Phase-4 Governance:** `SAFE_FOR_PHASE_5` (UI-only, legacy quotation flow)

---

## 📊 SUMMARY BY PRIORITY

### Critical Priority (~35 hours)
1. Security Hardening Phase 1: 10-12 hours remaining
2. Sprint-4 UI Components: ~25-35 hours
3. Phase 1 Backend Testing: 6-8 hours

### High Priority (~45 hours)
4. Phase 2: Discount Application Table: 40-64 hours
5. Phase 3: Customer/Division/Contact: 24-32 hours
6. UI Standardization: 15-20 hours

### Medium Priority (~20 hours)
7. Phase 4-6: Backend Features: 120-152 hours (future)
8. Documentation Gaps: 10-15 hours
9. Code TODOs: 2-4 hours
10. Sprint-3 Polish: 4 hours
11. Add Component Button Fix: 2-3 hours

---

## 🎯 RECOMMENDED EXECUTION ORDER

### Immediate (This Week):
1. **Complete Security Hardening Phase 1** (if production security is priority)
   - Tasks 1-3: Form Requests (remaining), Sanitization, CSRF (6-7 hours)

2. **Complete Sprint-4 UI** (if discount rules are needed)
   - Backend is ready, can start immediately
   - ~25-35 hours estimated

3. **Phase 1 Backend Testing** (6-8 hours)
   - Complete guardrails testing

### Short-term (Next 2 Weeks):
4. **UI Standardization** (start with high-priority pages)
   - 11 high-priority pages (15-20 hours)

5. **Complete Security Hardening** (if started)
   - Tasks 4-6 (5 hours)

### Medium-term (Next Month):
6. **Phase 2: Discount Application Table** (40-64 hours)
7. **Phase 3: Customer/Division/Contact** (24-32 hours)
8. **Documentation Gaps** (10-15 hours)

### Long-term (Future):
9. **Phase 4-6: Backend Features** (120-152 hours)
10. **Code TODOs** (2-4 hours)
11. **Sprint-3 Polish** (4 hours)
12. **Add Component Button Fix** (2-3 hours)

---

## 📝 NOTES

### Exclusions (As Requested):
- ✅ V2 Final Costing Specification (`V2_FINAL_COSTING_SPECIFICATION.md`)
- ✅ Related TODOs from V2 costing work

### Completed Work (Not Included):
- ✅ **6-Phase Documentation Plan** - 100% complete
- ✅ **Sprint-1, 2, 3** - All complete
- ✅ **Sprint-4 Backend** - 100% complete
- ✅ **Phase 1 Task 1.1: Discount fix** - Done
- ✅ **Phase 1 Task 1.2: BOM Identity** - Done
- ✅ **Phase 1 Task 1.3: Guardrails implementation** - Done (testing pending)
- ✅ **Discount Field Event Handling Issues** - Fixed
- ✅ **Smoke Test Checklist** - Documented

---

**Last Updated:** 2025-12-18  
**Next Review:** After completing critical priority items  
**Source:** `/Users/nirajdesai/Projects/nish/` (actual codebase)



