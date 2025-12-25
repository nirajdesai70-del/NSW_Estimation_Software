# Batch-S4-3 CP1: JS/AJAX Extracts for Migration

**Purpose:** Extract all COMPAT endpoint calls from MBOM view files for SHARED endpoint migration  
**Date:** 2025-12-24  
**Status:** Ready for migration rewrite  
**Authority:** BATCH_S4_3_CP0_BASELINE.md, S3_CIM_ALIGNMENT.md pattern

---

## File 1: `masterbom/create.blade.php`

### 1.1 `masterbom.getsubcategory` call (getSubcategory function)
**Location:** Lines 114-142  
**Trigger:** `#CategoryId_{count}` change event (via `onchange='getSubcategory(this.value,{count})'`)

```javascript
function getSubcategory(id,count){
    $.ajax({
        url: '{{ route('masterbom.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">Sub Category</option>';
            // var producttype = '<option value="0">Product Type</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '">' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId_' + count).html(subcategory);


            var producttype = '<option value="0">Product Type</option>';
            if (data.producttype.length > 0) {
                // var selected = data.producttype.length == 1 ? '' : '';
                data.producttype.forEach(element => {
                    producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
                });
            }
            $('#ItemId_' + count).html(producttype);
            getdescription(count)
        }
    });
}
```

**Current endpoint:** `masterbom.getsubcategory`  
**Current payload:** `{ subcategory: [{SubCategoryId, Name}], producttype: [{ItemId, Name}] }`  
**Migration target:** Split into:
- `GET /api/category/{categoryId}/subcategories` (for subcategory)
- `GET /api/category/{categoryId}/items` (for producttype)

**Parameter mapping:**
- Current: `{id}` (path param) → `categoryId`
- Target: `{categoryId}` (path param) for both endpoints

**Response transformation:**
- Extract `data.subcategory` array → map `SubCategoryId` → `id`, `Name` → `text`
- Extract `data.producttype` array → map `ItemId` → `id`, `Name` → `text`
- SHARED endpoints return `[{id, label}]` format

---

### 1.2 `masterbom.getproducttype` call (getproductType function)
**Location:** Lines 143-160  
**Status:** ⚠️ **COMMENTED OUT** (not actively used)

```javascript
function getproductType(id, count){
    // $.ajax({
    //     url: '{{ route('masterbom.getproducttype',['_group_id']) }}'.replace('_group_id', id),
    //     type: 'GET',
    //     dataType: 'json',
    //     success: function(data) {
    //         var producttype = '<option value="0">Product Type</option>';
    //         if (data.producttype.length > 0) {
    //             data.producttype.forEach(element => {
    //                 producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
    //             });
    //         }
    //         $('#ItemId_' + count).html(producttype);
                getdescription(count)
    //     }
    // });
}
```

**Current endpoint:** `masterbom.getproducttype` (commented)  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `GET /api/category/{categoryId}/items?subcategory={subCategoryId}` (if needed)

**Note:** This function is commented out and only calls `getdescription(count)`. No migration needed unless uncommented.

---

### 1.3 `masterbom.getdescription` call (getdescription function)
**Location:** Lines 161-186  
**Trigger:** Called after CategoryId/SubCategoryId/ItemId changes

```javascript
function getdescription(count){
    var CategoryId = $('#CategoryId_' + count).val();
    var SubCategoryId = $('#SubCategoryId_' + count).val();
    var ItemId = $('#ItemId_' + count).val();
    $.ajax({
        url: '{{ route('masterbom.getdescription') }}',
        type: 'GET',
        data: {
            "_token": "{{ csrf_token() }}",
            'CategoryId': CategoryId,
            'SubCategoryId': SubCategoryId,
            'ItemId': ItemId
        },
        dataType: 'json',
        success: function(data) {
            var description = '<option value="0">Generic</option>';
            if (data.description.length > 0) {
                var selected = data.description.length == 1 ? '' : '';
                data.description.forEach(element => {
                    description += '<option value="' + element.ProductId + '">' + element.Name + '</option>';
                });
            }
            $('#Description_' + count).html(description);
        }
    });
}
```

**Current endpoint:** `masterbom.getdescription`  
**Current payload:** `{ description: [{ProductId, Name}] }`  
**Migration target:** `GET /api/category/{categoryId}/products?subcategoryId={SubCategoryId}&itemId={ItemId}`

**Parameter mapping:**
- Current: `CategoryId`, `SubCategoryId`, `ItemId` (query params)
- Target: `{categoryId}` (path param) + `?subcategoryId={SubCategoryId}&itemId={ItemId}` (query params)

**Response transformation:**
- Extract `data.description` array → map `ProductId` → `id`, `Name` → `text`
- SHARED endpoint returns `[{id, label}]` format

---

## File 2: `masterbom/edit.blade.php`

### 2.1 `masterbom.getsubcategory` call (getSubcategory function)
**Location:** Lines 187-214  
**Trigger:** `#CategoryId_{count}` change event (via `onchange='getSubcategory(this.value,{count})'`)

```javascript
function getSubcategory(id,count){
    $.ajax({
        url: '{{ route('masterbom.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">Sub Category</option>';
            var producttype = '<option value="0">Product Type</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '">' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId_' + count).html(subcategory);

            var producttype = '<option value="0">Product Type</option>';
            if (data.producttype.length > 0) {
                // var selected = data.producttype.length == 1 ? '' : '';
                data.producttype.forEach(element => {
                    producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
                });
            }
            $('#ItemId_' + count).html(producttype);
            getdescription(count)
        }
    });
}
```

**Current endpoint:** `masterbom.getsubcategory`  
**Current payload:** `{ subcategory: [{SubCategoryId, Name}], producttype: [{ItemId, Name}] }`  
**Migration target:** Split into:
- `GET /api/category/{categoryId}/subcategories` (for subcategory)
- `GET /api/category/{categoryId}/items` (for producttype)

**Parameter mapping:**
- Current: `{id}` (path param) → `categoryId`
- Target: `{categoryId}` (path param) for both endpoints

**Response transformation:**
- Extract `data.subcategory` array → map `SubCategoryId` → `id`, `Name` → `text`
- Extract `data.producttype` array → map `ItemId` → `id`, `Name` → `text`
- SHARED endpoints return `[{id, label}]` format

---

### 2.2 `masterbom.getproducttype` call (getproductType function)
**Location:** Lines 215-232  
**Status:** ⚠️ **COMMENTED OUT** (not actively used)

```javascript
function getproductType(id, count){
    // $.ajax({
    //     url: '{{ route('masterbom.getproducttype',['_group_id']) }}'.replace('_group_id', id),
    //     type: 'GET',
    //     dataType: 'json',
    //     success: function(data) {
    //         var producttype = '<option value="0">Product Type</option>';
    //         if (data.producttype.length > 0) {
    //             data.producttype.forEach(element => {
    //                 producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
    //             });
    //         }
    //         $('#ItemId_' + count).html(producttype);
                getdescription(count)
    //     }
    // });
}
```

**Current endpoint:** `masterbom.getproducttype` (commented)  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `GET /api/category/{categoryId}/items?subcategory={subCategoryId}` (if needed)

**Note:** This function is commented out and only calls `getdescription(count)`. No migration needed unless uncommented.

---

### 2.3 `masterbom.getdescription` call (getdescription function)
**Location:** Lines 261-291  
**Status:** ⚠️ **COMMENTED OUT** (B4 change - Master BOM uses L0/L1 fields instead)

```javascript
// ✅ B4: Commented out - getdescription is no longer needed (ProductId not used in Master BOM)
function getdescription(count){
    // Master BOM items use L0/L1 fields instead of ProductId
    // This function is kept for backward compatibility but not used
    return;
    /*
    var CategoryId = $('#CategoryId_' + count).val();
    var SubCategoryId = $('#SubCategoryId_' + count).val();
    var ItemId = $('#ItemId_' + count).val();
    $.ajax({
        url: '{{ route('masterbom.getdescription') }}',
        type: 'GET',
        data: {
            "_token": "{{ csrf_token() }}",
            'CategoryId': CategoryId,
            'SubCategoryId': SubCategoryId,
            'ItemId': ItemId
        },
        dataType: 'json',
        success: function(data) {
            var description = '<option value="0">Generic</option>';
            if (data.description.length > 0) {
                var selected = data.description.length == 1 ? '' : '';
                data.description.forEach(element => {
                    description += '<option value="' + element.ProductId + '">' + element.Name + '</option>';
                });
            }
            $('#Description_' + count).html(description);
        }
    });
    */
}
```

**Current endpoint:** `masterbom.getdescription` (commented)  
**Status:** ⚠️ **NOT USED** in edit.blade.php (B4 change - Master BOM uses ResolutionStatus L0/L1 fields)

**Note:** The edit screen uses ResolutionStatus (L0/L1) fields instead of ProductId dropdown. This function is kept for backward compatibility but not called. No migration needed for edit.blade.php.

---

## File 3: `masterbom/copy.blade.php`

### 3.1 `masterbom.getsubcategory` call (getSubcategory function)
**Location:** Lines 166-193  
**Trigger:** `#CategoryId_{count}` change event (via `onchange='getSubcategory(this.value,{count})'`)

```javascript
function getSubcategory(id,count){
    $.ajax({
        url: '{{ route('masterbom.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">Sub Category</option>';
            var producttype = '<option value="0">Product Type</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '">' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId_' + count).html(subcategory);

            var producttype = '<option value="0">Product Type</option>';
            if (data.producttype.length > 0) {
                // var selected = data.producttype.length == 1 ? '' : '';
                data.producttype.forEach(element => {
                    producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
                });
            }
            $('#ItemId_' + count).html(producttype);
            getdescription(count)
        }
    });
}
```

**Current endpoint:** `masterbom.getsubcategory`  
**Current payload:** `{ subcategory: [{SubCategoryId, Name}], producttype: [{ItemId, Name}] }`  
**Migration target:** Split into:
- `GET /api/category/{categoryId}/subcategories` (for subcategory)
- `GET /api/category/{categoryId}/items` (for producttype)

**Parameter mapping:**
- Current: `{id}` (path param) → `categoryId`
- Target: `{categoryId}` (path param) for both endpoints

**Response transformation:**
- Extract `data.subcategory` array → map `SubCategoryId` → `id`, `Name` → `text`
- Extract `data.producttype` array → map `ItemId` → `id`, `Name` → `text`
- SHARED endpoints return `[{id, label}]` format

---

### 3.2 `masterbom.getproducttype` call (getproductType function)
**Location:** Lines 194-211  
**Status:** ⚠️ **COMMENTED OUT** (not actively used)

```javascript
function getproductType(id, count){
    // $.ajax({
    //     url: '{{ route('masterbom.getproducttype',['_group_id']) }}'.replace('_group_id', id),
    //     type: 'GET',
    //     dataType: 'json',
    //     success: function(data) {
    //         var producttype = '<option value="0">Product Type</option>';
    //         if (data.producttype.length > 0) {
    //             data.producttype.forEach(element => {
    //                 producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
    //             });
    //         }
    //         $('#ItemId_' + count).html(producttype);
                getdescription(count)
    //     }
    // });
}
```

**Current endpoint:** `masterbom.getproducttype` (commented)  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `GET /api/category/{categoryId}/items?subcategory={subCategoryId}` (if needed)

**Note:** This function is commented out and only calls `getdescription(count)`. No migration needed unless uncommented.

---

### 3.3 `masterbom.getdescription` call (getdescription function)
**Location:** Lines 212-237  
**Trigger:** Called after CategoryId/SubCategoryId/ItemId changes

```javascript
function getdescription(count){
    var CategoryId = $('#CategoryId_' + count).val();
    var SubCategoryId = $('#SubCategoryId_' + count).val();
    var ItemId = $('#ItemId_' + count).val();
    $.ajax({
        url: '{{ route('masterbom.getdescription') }}',
        type: 'GET',
        data: {
            "_token": "{{ csrf_token() }}",
            'CategoryId': CategoryId,
            'SubCategoryId': SubCategoryId,
            'ItemId': ItemId
        },
        dataType: 'json',
        success: function(data) {
            var description = '<option value="0">Generic</option>';
            if (data.description.length > 0) {
                var selected = data.description.length == 1 ? '' : '';
                data.description.forEach(element => {
                    description += '<option value="' + element.ProductId + '">' + element.Name + '</option>';
                });
            }
            $('#Description_' + count).html(description);
        }
    });
}
```

**Current endpoint:** `masterbom.getdescription`  
**Current payload:** `{ description: [{ProductId, Name}] }`  
**Migration target:** `GET /api/category/{categoryId}/products?subcategoryId={SubCategoryId}&itemId={ItemId}`

**Parameter mapping:**
- Current: `CategoryId`, `SubCategoryId`, `ItemId` (query params)
- Target: `{categoryId}` (path param) + `?subcategoryId={SubCategoryId}&itemId={ItemId}` (query params)

**Response transformation:**
- Extract `data.description` array → map `ProductId` → `id`, `Name` → `text`
- SHARED endpoint returns `[{id, label}]` format

---

## Summary: Migration Mapping

| COMPAT Endpoint | Current Payload Shape | SHARED Target | Response Transformation | Active Usage |
|---|---|---|---|---|
| `masterbom.getdescription` | `{ description: [{ProductId, Name}] }` | `GET /api/category/{categoryId}/products?subcategoryId={SubCategoryId}&itemId={ItemId}` | Extract `description` array, map `ProductId` → `id`, `Name` → `text` | ✅ create.blade.php, copy.blade.php |
| `masterbom.getproducttype` | `{ producttype: [{ItemId, Name}] }` | `GET /api/category/{categoryId}/items?subcategory={subCategoryId}` | Extract `producttype` array, map `ItemId` → `id`, `Name` → `text` | ⚠️ Commented out (not used) |
| `masterbom.getsubcategory` | `{ subcategory: [...], producttype: [...] }` | Split: `GET /api/category/{categoryId}/subcategories` + `GET /api/category/{categoryId}/items` | Multiple calls, extract nested arrays, map to `{id, text}` | ✅ create.blade.php, edit.blade.php, copy.blade.php |

**Note:** `masterbom.getdescription` is commented out in `edit.blade.php` due to B4 change (Master BOM uses ResolutionStatus L0/L1 fields instead of ProductId dropdown).

---

## Migration Order (CP1.2 Execution Sequence)

**Phase 1: `masterbom.getdescription` → `api.category.products`**
- ✅ Migrate in `create.blade.php` (line 161-186)
- ✅ Migrate in `copy.blade.php` (line 212-237)
- ⏭️ Skip `edit.blade.php` (commented out, B4 change)

**Phase 2: `masterbom.getproducttype` → `api.category.items`**
- ⏭️ Skip (commented out in all files, not actively used)

**Phase 3: `masterbom.getsubcategory` → Split into multiple SHARED calls**
- ✅ Migrate in `create.blade.php` (line 114-142)
- ✅ Migrate in `edit.blade.php` (line 187-214)
- ✅ Migrate in `copy.blade.php` (line 166-193)

**Migration Pattern (from S4-2):**
1. Replace COMPAT endpoint URL with SHARED endpoint URL
2. Update parameter format (path params vs query params)
3. Transform response: extract nested arrays, map field names (`SubCategoryId` → `id`, `Name` → `text`)
4. Keep COMPAT endpoints alive (no deletions)
5. No payload reshaping (use client-side transformation only)

---

**Ready for migration rewrite in CP1.2 phase order:**
1. Phase-1: `masterbom.getdescription` → `api.category.products` (create, copy)
2. Phase-3: `masterbom.getsubcategory` → Split into `api.category.subcategories` + `api.category.items` (create, edit, copy)

