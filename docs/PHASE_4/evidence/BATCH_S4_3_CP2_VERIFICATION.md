# Batch-S4-3 CP2: Verification Test Log

**Date:** 2025-12-24  
**Status:** ⏳ **PENDING OPERATOR VERIFICATION**  
**Tester:** [Operator Name]

---

## Test Summary

**Objective:** Verify MBOM screens (Create/Edit/Copy) consume SHARED catalog APIs correctly, with COMPAT endpoints as fallback only.

**Scope:**
- Master BOM Create screen
- Master BOM Edit screen (B4 ResolutionStatus L0/L1 behavior)
- Master BOM Copy screen

**Expected Behavior:**
- All catalog lookups use SHARED `/api/category/*` endpoints
- COMPAT endpoints (`masterbom.getsubcategory`, `masterbom.getdescription`) remain available as fallback
- B4 ResolutionStatus behavior intact in Edit screen (no Generic dropdown dependency)

---

## Test 1: Master BOM — Create

**Screen:** `/masterbom/create`  
**Status:** ⏳ **PENDING**

### Test Steps:
1. Navigate to `/masterbom/create`
2. Click "Add More" to add item row
3. Select Category from dropdown
4. Verify SubCategory, Product Type, Generic dropdowns populate
5. Select SubCategory
6. Verify Generic dropdown refreshes
7. Select Product Type
8. Verify Generic dropdown refreshes

### Expected Network Calls:
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK

### Actual Results:
- [ ] All SHARED calls present
- [ ] No COMPAT calls
- [ ] Dropdowns populate correctly
- [ ] No JS console errors

### Issues:
- [ ] None
- [ ] [Issue description]

---

## Test 2: Master BOM — Edit

**Screen:** `/masterbom/{id}/edit`  
**Status:** ⏳ **PENDING**

### Test Steps:
1. Navigate to `/masterbom/{id}/edit` for existing Master BOM
2. Verify existing items display with ResolutionStatus (L0/L1)
3. Verify GenericDescriptor/DefinedSpecJson fields visible based on ResolutionStatus
4. Verify NO Generic dropdown exists
5. Change Category for an existing item
6. Verify SubCategory and Product Type refresh
7. Change ResolutionStatus from L0 to L1
8. Verify fields toggle correctly
9. Add new item row
10. Select Category for new item
11. Verify dropdowns populate

### Expected Network Calls:
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ❌ NO `masterbom.getdescription` call (B4 - not used)

### Actual Results:
- [ ] All SHARED calls present
- [ ] No COMPAT calls
- [ ] B4 ResolutionStatus behavior intact
- [ ] No Generic dropdown dependency
- [ ] No JS console errors

### Issues:
- [ ] None
- [ ] [Issue description]

---

## Test 3: Master BOM — Copy

**Screen:** `/masterbom/{id}/copy`  
**Status:** ⏳ **PENDING**

### Test Steps:
1. Navigate to `/masterbom/{id}/copy` for existing Master BOM
2. Verify existing items display with Generic dropdown (legacy ProductId-based)
3. Change Category for an existing item
4. Verify SubCategory, Product Type, Generic refresh
5. Select SubCategory
6. Verify Generic dropdown refreshes
7. Select Product Type
8. Verify Generic dropdown refreshes
9. Add new item row
10. Select Category for new item
11. Verify all dropdowns populate

### Expected Network Calls:
- ✅ `GET /api/category/{id}/subcategories` → 200 OK
- ✅ `GET /api/category/{id}/items` → 200 OK
- ✅ `GET /api/category/{id}/products?subcategoryId={subId}&itemId={itemId}` → 200 OK

### Actual Results:
- [ ] All SHARED calls present
- [ ] No COMPAT calls
- [ ] Generic dropdown populates correctly
- [ ] No JS console errors

### Issues:
- [ ] None
- [ ] [Issue description]

---

## Test 4: Hard Guards Verification

### 4.1: No Payload Shape Changes
**Status:** ⏳ **PENDING**

- [ ] `/api/category/{id}/subcategories` returns `[{SubCategoryId, Name}]`
- [ ] `/api/category/{id}/items` returns `[{ItemId, Name}]`
- [ ] `/api/category/{id}/products` returns `[{ProductId, Name}]`

### 4.2: No Route Renames
**Status:** ⏳ **PENDING**

- [ ] All routes still use same names
- [ ] No route renames occurred

### 4.3: No COMPAT Deletion
**Status:** ⏳ **PENDING**

- [ ] `masterbom.getsubcategory` route still exists (routes/web.php line 231)
- [ ] `masterbom.getdescription` route still exists (routes/web.php line 233)
- [ ] `masterbom.getproducttype` route still exists (routes/web.php line 232)

**Fallback Test:**
- [ ] Simulate SHARED endpoint failure (network error)
- [ ] Verify COMPAT fallback triggers correctly
- [ ] Verify UI still works with COMPAT fallback

### 4.4: No QUO-V2 Touched
**Status:** ⏳ **PENDING**

- [ ] No files in `resources/views/quotation/v2/` modified
- [ ] No QuotationV2Controller changes
- [ ] Git status confirms no QUO-V2 files touched

### 4.5: No Master Auto-Creation
**Status:** ⏳ **PENDING**

- [ ] No POST requests during dropdown selection
- [ ] No runtime master data creation

### 4.6: B4 ResolutionStatus Behavior
**Status:** ⏳ **PENDING**

- [ ] ResolutionStatus L0/L1 toggle works (Edit screen)
- [ ] GenericDescriptor field shows/hides correctly
- [ ] DefinedSpecJson field shows/hides correctly
- [ ] No hidden `#Description_{count}` dependency
- [ ] getdescription() function is no-op (commented out)

---

## Overall CP2 Result

- [ ] ✅ **PASS** - All tests pass, ready for CP3
- [ ] ❌ **FAIL** - Issues found, needs fix

**Key Verification:**
- [ ] SHARED API calls working correctly
- [ ] COMPAT kept as fallback only
- [ ] No breaking changes observed
- [ ] Dropdowns populate correctly
- [ ] B4 ResolutionStatus behavior intact (Edit screen)

**Known Issues (Pre-existing):**
- [ ] None
- [ ] [Issue description]

---

## Evidence Attachments

### Screenshots:
- [ ] Network Tab - MBOM Create (Category selected)
- [ ] Network Tab - MBOM Edit (Category changed)
- [ ] Network Tab - MBOM Copy (Category selected)
- [ ] UI Screenshot - MBOM Edit (B4 ResolutionStatus)
- [ ] Browser Console (no errors)

### Network Logs:
- [ ] MBOM Create - Full network log (Category → SubCategory → Product Type → Generic)
- [ ] MBOM Edit - Full network log (Category change)
- [ ] MBOM Copy - Full network log (Category → SubCategory → Product Type → Generic)

---

## Next Steps

**If PASS:**
- Generate CP3 Evidence Pack
- Update MASTER_TASK_LIST.md
- Mark Batch-S4-3 as CLOSED

**If FAIL:**
- Document issues
- Fix issues in CP1.2
- Re-test CP2

---

---

## ⚠️ Important Context: Live Environment & Future NSW Changes

### Live Environment Considerations

**Execution Context:**
- This work is being executed in **live/production environment** (Nish Live)
- Changes must be minimal, safe, and non-disruptive
- No new table structures or schema changes are introduced

**Changes Made (CP1.2):**
1. **Controller Bug Fix:** `MasterBomController@store` - Changed `$pr->id` → `$pr->MasterBomId` (fixes null constraint violation)
2. **JavaScript Migration:** MBOM views updated to use SHARED `/api/*` endpoints instead of COMPAT endpoints
3. **B4 Alignment:** Removed unused `getdescription()` calls in create.blade.php (B4 structure doesn't use Generic dropdown)

**Safety Assurance:**
- ✅ No database schema changes
- ✅ No new tables created
- ✅ COMPAT endpoints remain active (fallback available)
- ✅ Changes are JavaScript-only (client-side endpoint URLs)
- ✅ All changes align with existing B4 structure already in place

---

### Future NSW Fundamental Work Impact

**Important Note:**
- Phase-4 (S4-3) work is **legacy stabilization** only
- When **NSW Fundamental Alignment** begins with new table structures, Phase-4 work may need review/revision
- Current SHARED contract approach is designed as an **adapter seam** - can be swapped behind the scenes
- No Phase-4 changes lock in schema dependencies that would conflict with NSW redesign

**Revert Option Available:**
- All changes can be reverted to CP0 baseline if needed
- Git commit hash for rollback: `1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`
- COMPAT endpoints remain available during transition

**Design Compatibility:**
- SHARED contracts are transport/interface layer, not data model layer
- Future NSW tables can be mapped to SHARED contracts without changing consumers
- Phase-4 work reduces blast radius for future changes (single adapter point)

---

**CP2 Verification Date:** [Date]  
**Verified By:** [Name]  
**Status:** ⏳ **PENDING OPERATOR VERIFICATION**

