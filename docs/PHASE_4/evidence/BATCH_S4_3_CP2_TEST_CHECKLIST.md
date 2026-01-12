# Batch-S4-3 CP2: Verification Test Checklist

**Date:** 2025-12-24  
**Status:** Ready for Testing  
**Objective:** Verify MBOM screens consume SHARED catalog APIs correctly

---

## Pre-Test Setup

1. ✅ Open Browser DevTools → Network tab
2. ✅ Filter: XHR/Fetch requests
3. ✅ Clear network log
4. ✅ Ensure you're logged in

---

## Test 1: Master BOM — Create

**Screen:** `/masterbom/create`  
**File:** `source_snapshot/resources/views/masterbom/create.blade.php`

### Step 1.1: Add Item Row
**Action:** Click "Add More" button to add a new item row

**Expected UI:**
- ✅ New row appears in table
- ✅ Category dropdown appears
- ✅ SubCategory, Product Type, Generic dropdowns appear (empty initially)

---

### Step 1.2: Select Category
**Action:** Select a Category from dropdown (e.g., "Electrical Panels")

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId=0&itemId=0` → 200 OK (via getdescription)

**Expected UI:**
- ✅ SubCategory dropdown populates
- ✅ Product Type (ItemId) dropdown populates
- ✅ Generic dropdown populates (if products exist)

**Verify:**
- ❌ NO call to `masterbom.getsubcategory`
- ❌ NO call to `masterbom.getdescription`
- ✅ All dropdowns populate correctly

---

### Step 1.3: Select SubCategory
**Action:** Select a SubCategory from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/products?subcategoryId={subId}&itemId=0` → 200 OK (via getdescription)

**Expected UI:**
- ✅ Generic dropdown refreshes (filtered by SubCategory)

**Verify:**
- ❌ NO call to `masterbom.getdescription` (COMPAT)

---

### Step 1.4: Select Product Type
**Action:** Select a Product Type (ItemId) from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK (via getdescription)

**Expected UI:**
- ✅ Generic dropdown refreshes (filtered by Product Type)

**Verify:**
- ❌ NO call to `masterbom.getdescription` (COMPAT)

---

### Step 1.5: Select Generic
**Action:** Select a Generic product from dropdown

**Expected UI:**
- ✅ Generic dropdown shows selected value
- ✅ Quantity field is editable

---

**Test 1 Pass Criteria:**
- ✅ All SHARED API calls work (`/api/category/*/subcategories`, `/api/category/*/items`, `/api/category/*/products`)
- ✅ No COMPAT calls (`masterbom.getsubcategory`, `masterbom.getdescription`)
- ✅ No JS console errors
- ✅ Dropdowns populate correctly
- ✅ Multiple rows can be added and populated independently

---

## Test 2: Master BOM — Edit

**Screen:** `/masterbom/{id}/edit`  
**File:** `source_snapshot/resources/views/masterbom/edit.blade.php`

### Step 2.1: Page Load
**Action:** Navigate to edit page for existing Master BOM

**Expected UI:**
- ✅ All existing items displayed in table
- ✅ Category, SubCategory, Product Type dropdowns pre-populated
- ✅ **B4 Change:** ResolutionStatus dropdown visible (L0/L1)
- ✅ **B4 Change:** GenericDescriptor or DefinedSpecJson fields visible (based on ResolutionStatus)
- ✅ **B4 Change:** NO Generic dropdown (ProductId not used in B4)

**Verify:**
- ✅ No hidden `#Description_{count}` element exists
- ✅ ResolutionStatus selector works correctly

---

### Step 2.2: Change Category (Existing Item)
**Action:** Change Category dropdown for an existing item

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK

**Expected UI:**
- ✅ SubCategory dropdown refreshes
- ✅ Product Type dropdown refreshes
- ✅ ResolutionStatus preserved (L0 or L1)
- ✅ GenericDescriptor/DefinedSpecJson fields remain visible based on ResolutionStatus

**Verify:**
- ❌ NO call to `masterbom.getsubcategory` (COMPAT)
- ❌ NO call to `masterbom.getdescription` (not used in B4)
- ✅ ResolutionStatus fields toggle correctly

---

### Step 2.3: Change ResolutionStatus
**Action:** Change ResolutionStatus from L0 to L1 (or vice versa)

**Expected UI:**
- ✅ GenericDescriptor field hides (if L1)
- ✅ DefinedSpecJson field shows (if L1)
- ✅ GenericDescriptor field shows (if L0)
- ✅ DefinedSpecJson field hides (if L0)

**Verify:**
- ✅ Toggle function works correctly
- ✅ No Generic dropdown appears
- ✅ No network calls triggered (local UI only)

---

### Step 2.4: Add New Item
**Action:** Click "Add More" button to add new item row

**Expected Network Calls:**
- ✅ None (until Category selected)

**Expected UI:**
- ✅ New row appears with empty dropdowns
- ✅ ResolutionStatus defaults to L0
- ✅ GenericDescriptor field visible (L0 default)

---

### Step 2.5: Select Category (New Item)
**Action:** Select Category for newly added item

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK

**Expected UI:**
- ✅ SubCategory and Product Type dropdowns populate
- ✅ ResolutionStatus remains L0
- ✅ GenericDescriptor field remains visible

**Verify:**
- ❌ NO call to `masterbom.getdescription` (B4 change - not used)

---

**Test 2 Pass Criteria:**
- ✅ Page loads without errors
- ✅ All SHARED API calls work
- ✅ B4 ResolutionStatus (L0/L1) behavior intact
- ✅ No Generic dropdown dependency
- ✅ No fallback errors in console
- ✅ Existing values preserved correctly

---

## Test 3: Master BOM — Copy

**Screen:** `/masterbom/{id}/copy`  
**File:** `source_snapshot/resources/views/masterbom/copy.blade.php`

### Step 3.1: Page Load
**Action:** Navigate to copy page for existing Master BOM

**Expected UI:**
- ✅ Master BOM name/UniqueNo fields pre-filled (editable)
- ✅ All existing items displayed in table
- ✅ Category, SubCategory, Product Type dropdowns pre-populated
- ✅ Generic dropdown pre-populated (if item has ProductId)

**Note:** Copy screen uses legacy ProductId-based Generic selection (not B4 ResolutionStatus)

---

### Step 3.2: Change Category (Existing Item)
**Action:** Change Category dropdown for an existing item

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK (via getdescription)

**Expected UI:**
- ✅ SubCategory dropdown refreshes
- ✅ Product Type dropdown refreshes
- ✅ Generic dropdown refreshes

**Verify:**
- ❌ NO call to `masterbom.getsubcategory` (COMPAT)
- ❌ NO call to `masterbom.getdescription` (COMPAT)

---

### Step 3.3: Select SubCategory
**Action:** Select SubCategory from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK

**Expected UI:**
- ✅ Generic dropdown refreshes (filtered by SubCategory)

---

### Step 3.4: Select Product Type
**Action:** Select Product Type from dropdown

**Expected Network Calls:**
- ✅ `GET /api/category/{categoryId}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK

**Expected UI:**
- ✅ Generic dropdown refreshes (filtered by Product Type)

---

### Step 3.5: Add New Item
**Action:** Click "Add More" button

**Expected UI:**
- ✅ New row appears
- ✅ All dropdowns empty initially

---

### Step 3.6: Select Category (New Item)
**Action:** Select Category for newly added item

**Expected Network Calls:**
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId=0&itemId=0` → 200 OK

**Expected UI:**
- ✅ SubCategory, Product Type, Generic dropdowns populate

---

**Test 3 Pass Criteria:**
- ✅ All SHARED API calls work
- ✅ No COMPAT calls
- ✅ Copy functionality works correctly
- ✅ Generic dropdown populates correctly (legacy ProductId-based)
- ✅ No JS console errors

---

## Test 4: Hard Guards Verification

### 4.1: No Payload Shape Changes
**Verify:** Check Network tab responses
- ✅ `/api/category/{id}/subcategories` returns `[{SubCategoryId, Name}]`
- ✅ `/api/category/{id}/items` returns `[{ItemId, Name}]`
- ✅ `/api/category/{id}/products` returns `[{ProductId, Name}]`

### 4.2: No Route Renames
**Verify:** Check routes/web.php
- ✅ All routes still use same names
- ✅ No route renames occurred

### 4.3: No COMPAT Deletion
**Verify:** Check routes/web.php
- ✅ `masterbom.getsubcategory` route still exists (line 231)
- ✅ `masterbom.getdescription` route still exists (line 233)
- ✅ `masterbom.getproducttype` route still exists (line 232)

**Verify:** Check Network tab (fallback scenarios)
- ✅ COMPAT endpoints still respond (if SHARED fails, fallback should work)

### 4.4: No QUO-V2 Touched
**Verify:** Check git status or file timestamps
- ✅ No files in `resources/views/quotation/v2/` modified
- ✅ No QuotationV2Controller changes
- ✅ No files in `app/Http/Controllers/QuotationV2Controller.php` modified

### 4.5: No Master Auto-Creation
**Verify:** Check browser console and network
- ✅ No POST requests to create Category/SubCategory/Item during dropdown selection
- ✅ No runtime master data creation

### 4.6: B4 ResolutionStatus Behavior (Edit Screen Only)
**Verify:** Check edit.blade.php behavior
- ✅ ResolutionStatus L0/L1 toggle works
- ✅ GenericDescriptor field shows/hides correctly
- ✅ DefinedSpecJson field shows/hides correctly
- ✅ No hidden `#Description_{count}` dependency
- ✅ getdescription() function is no-op (commented out)

---

## Test 5: Evidence Capture

### Screenshots to Take:

1. **Network Tab - MBOM Create (Category selected):**
   - Show 3 SHARED calls: `/api/category/{id}/subcategories`, `/api/category/{id}/items`, `/api/category/{id}/products`
   - NO `masterbom.getsubcategory` call
   - NO `masterbom.getdescription` call

2. **Network Tab - MBOM Edit (Category changed):**
   - Show 2 SHARED calls: `/api/category/{id}/subcategories`, `/api/category/{id}/items`
   - NO `masterbom.getsubcategory` call
   - NO `masterbom.getdescription` call (B4 - not used)

3. **Network Tab - MBOM Copy (Category selected):**
   - Show 3 SHARED calls: `/api/category/{id}/subcategories`, `/api/category/{id}/items`, `/api/category/{id}/products`
   - NO COMPAT calls

4. **UI Screenshot - MBOM Edit (B4 ResolutionStatus):**
   - Show ResolutionStatus dropdown (L0/L1)
   - Show GenericDescriptor field (L0)
   - Show DefinedSpecJson field (L1)
   - NO Generic dropdown visible

5. **Browser Console:**
   - No JS errors
   - No failed AJAX calls
   - No fallback warnings (unless testing fallback scenario)

---

## CP2 Exit Criteria

✅ **All 3 screens pass all test steps**  
✅ **No JS console errors**  
✅ **Dropdown UX intact**  
✅ **B4 ResolutionStatus behavior intact (Edit screen)**  
✅ **Governance rules respected (SHARED only, COMPAT as fallback)**  
✅ **No regressions (existing functionality works)**  
✅ **COMPAT routes still exist and functional (fallback tested)**

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

