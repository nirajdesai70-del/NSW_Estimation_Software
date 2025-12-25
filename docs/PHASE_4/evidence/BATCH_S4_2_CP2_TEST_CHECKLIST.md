# Batch-S4-2 CP2: Verification Test Checklist

**Date:** 2025-12-24  
**Status:** Ready for Testing  
**Objective:** Verify CIM screens consume SHARED catalog APIs correctly

---

## Pre-Test Setup

1. ✅ Open Browser DevTools → Network tab
2. ✅ Filter: XHR/Fetch requests
3. ✅ Clear network log
4. ✅ Ensure you're logged in

---

## Test 1: Specific Product — Create

**Screen:** `/product/create`  
**File:** `source_snapshot/resources/views/product/create.blade.php`

### Step 1.1: Select Category
**Action:** Select a Category from dropdown (e.g., "Electrical Panels")

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK  
- ✅ `GET /api/category/{id}/makes` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId=0&itemId=0` → 200 OK (via getdescription)

**Expected UI:**
- ✅ SubCategory dropdown populates
- ✅ Product Type (ItemId) dropdown populates
- ✅ Make dropdown populates
- ✅ Generic dropdown populates (if products exist)

**Verify:**
- ❌ NO call to `product.getsubcategory`
- ✅ All dropdowns are Select2-enabled and searchable

---

### Step 1.2: Select SubCategory
**Action:** Select a SubCategory from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/items?subcategory={subId}` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId={subId}&itemId=0` → 200 OK (via getdescription)

**Expected UI:**
- ✅ Product Type (ItemId) dropdown refreshes (filtered by SubCategory)
- ✅ Generic dropdown refreshes (filtered by SubCategory)

**Verify:**
- ❌ NO call to `product.getproducttype`

---

### Step 1.3: Select Product Type
**Action:** Select a Product Type (ItemId) from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK

**Expected UI:**
- ✅ Generic dropdown refreshes (filtered by Product Type)

---

### Step 1.4: Select Make
**Action:** Select a Make from dropdown

**Expected Network Calls:**
- ✅ `GET /api/make/{makeId}/series?categoryId={categoryId}` → 200 OK

**Expected UI:**
- ✅ Series dropdown populates

**Verify:**
- ❌ NO call to `product.getseries`

---

### Step 1.5: Verify Name Auto-Generation
**Action:** Change Category/SubCategory/Product Type/Description

**Expected UI:**
- ✅ Name field auto-generates (dash-separated values)

---

**Test 1 Pass Criteria:**
- ✅ All SHARED API calls work
- ✅ No COMPAT calls (except attributes - none on this screen)
- ✅ No JS console errors
- ✅ Dropdowns populate correctly
- ✅ Name auto-generation works

---

## Test 2: Specific Product — Edit

**Screen:** `/product/{id}/edit`  
**File:** `source_snapshot/resources/views/product/edit.blade.php`

### Step 2.1: Page Load
**Action:** Navigate to edit page for existing product

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/items` → 200 OK (via loadItemsForCategory if CategoryId set)

**Expected UI:**
- ✅ All dropdowns pre-populated with existing values
- ✅ Generic dropdown shows current GenericId selected

---

### Step 2.2: Change Category
**Action:** Change Category dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /api/category/{id}/makes` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId=0&itemId=0` → 200 OK

**Expected UI:**
- ✅ SubCategory, Product Type, Make dropdowns refresh
- ✅ Generic dropdown refreshes
- ✅ Existing selections preserved where applicable

---

### Step 2.3: Change SubCategory
**Action:** Change SubCategory dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/items?subcategory={subId}` → 200 OK

**Expected UI:**
- ✅ Product Type dropdown refreshes (filtered by SubCategory)
- ✅ Generic dropdown refreshes

**Verify:**
- ❌ NO call to `product.getproducttype`

---

### Step 2.4: Change Make
**Action:** Change Make dropdown

**Expected Network Calls:**
- ✅ `GET /api/make/{makeId}/series?categoryId={categoryId}` → 200 OK

**Expected UI:**
- ✅ Series dropdown refreshes

---

**Test 2 Pass Criteria:**
- ✅ Page loads without errors
- ✅ All SHARED API calls work
- ✅ Existing values preserved correctly
- ✅ No fallback errors in console

---

## Test 3: Generic Product — Create

**Screen:** `/generic/create`  
**File:** `source_snapshot/resources/views/generic/create.blade.php`

### Step 3.1: Select Category
**Action:** Select a Category from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /product/getsubcategory/{id}` → 200 OK (COMPAT - for attributes only)

**Expected UI:**
- ✅ SubCategory dropdown populates
- ✅ Product Type dropdown populates
- ✅ Attributes section populates (from COMPAT response)

**Verify:**
- ✅ COMPAT call ONLY for attributes
- ✅ SubCategory and Items come from SHARED, NOT from COMPAT response

---

### Step 3.2: Verify Attributes
**Action:** Check attributes section

**Expected UI:**
- ✅ Attribute fields appear (if category has attributes)
- ✅ Each attribute has label, input field, and hidden AttributeId

**Verify:**
- ✅ Attributes rendered correctly
- ✅ Prefix/Suffix displayed if present

---

### Step 3.3: Change SubCategory/Product Type
**Action:** Change SubCategory or Product Type

**Expected UI:**
- ✅ Dropdowns update correctly
- ✅ Attributes remain (or refresh if Category changes)

---

**Test 3 Pass Criteria:**
- ✅ SHARED calls for SubCategory and Items
- ✅ COMPAT call ONLY for attributes
- ✅ Attributes render correctly
- ✅ No duplicate attribute fields

---

## Test 4: Generic Product — Edit

**Screen:** `/generic/{id}/edit`  
**File:** `source_snapshot/resources/views/generic/edit.blade.php`

### Step 4.1: Page Load
**Action:** Navigate to edit page for existing generic product

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/items` → 200 OK (if CategoryId set)

**Expected UI:**
- ✅ All dropdowns pre-populated
- ✅ Attributes section shows existing attributes (both legacy and new editable system)

---

### Step 4.2: Change Category
**Action:** Change Category dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /product/getsubcategory/{id}` → 200 OK (COMPAT - for attributes)

**Expected UI:**
- ✅ SubCategory, Product Type refresh
- ✅ Attributes refresh (from COMPAT)

---

### Step 4.3: Change SubCategory
**Action:** Change SubCategory dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/items?subcategory={subId}` → 200 OK

**Expected UI:**
- ✅ Product Type dropdown refreshes

---

**Test 4 Pass Criteria:**
- ✅ Page loads without errors
- ✅ Attributes intact (no loss)
- ✅ Required attribute markers correct
- ✅ Both legacy and new attribute systems work

---

## Test 5: Hard Guards Verification

### 5.1: No Payload Shape Changes
**Verify:** Check Network tab responses
- ✅ `/api/category/{id}/subcategories` returns `[{SubCategoryId, Name}]`
- ✅ `/api/category/{id}/items` returns `[{ItemId, Name}]`
- ✅ `/api/category/{id}/products` returns `[{ProductId, Name}]`
- ✅ `/api/category/{id}/makes` returns map `{MakeId: Name}` or array
- ✅ `/api/make/{id}/series` returns `[{SeriesId, Name}]`

### 5.2: No Route Renames
**Verify:** Check routes/web.php
- ✅ All routes still use same names
- ✅ No route renames occurred

### 5.3: No COMPAT Deletion
**Verify:** Check routes/web.php
- ✅ `product.getsubcategory` route still exists
- ✅ `product.getgeneric` route still exists
- ✅ `product.getproducttype` route still exists
- ✅ `product.getseries` route still exists

### 5.4: No QUO-V2 Touched
**Verify:** Check git status or file timestamps
- ✅ No files in `resources/views/quotation/v2/` modified
- ✅ No QuotationV2Controller changes

### 5.5: No Master Auto-Creation
**Verify:** Check browser console and network
- ✅ No POST requests to create Category/SubCategory/Item during dropdown selection
- ✅ "Add New" buttons work but don't auto-trigger

---

## Test 6: Evidence Capture

### Screenshots to Take:
1. **Network Tab - Product Create (Category selected):**
   - Show 3 SHARED calls (subcategories, items, makes)
   - Show products call
   - NO product.getsubcategory call

2. **Network Tab - Generic Create (Category selected):**
   - Show 2 SHARED calls (subcategories, items)
   - Show 1 COMPAT call (product.getsubcategory for attributes)
   - Highlight that attributes come from COMPAT only

3. **Browser Console:**
   - No JS errors
   - No failed AJAX calls

4. **UI Screenshots:**
   - Product Create with all dropdowns populated
   - Generic Create with attributes visible

---

## CP2 Exit Criteria

✅ **All 4 screens pass all test steps**  
✅ **No JS console errors**  
✅ **Dropdown UX intact (Select2 working)**  
✅ **Attributes intact (generic screens)**  
✅ **Governance rules respected (COMPAT only for attributes)**  
✅ **No regressions (existing functionality works)**

---

## Issues Found

| Screen | Issue | Severity | Status |
|--------|-------|----------|--------|
| - | - | - | - |

---

## CP2 Result

- [ ] PASS - All tests pass, ready for CP3
- [ ] FAIL - Issues found, needs fix

**Notes:**

---

**Next Steps:**
- If PASS → Generate CP3 Evidence Pack
- If FAIL → Fix issues and re-test

