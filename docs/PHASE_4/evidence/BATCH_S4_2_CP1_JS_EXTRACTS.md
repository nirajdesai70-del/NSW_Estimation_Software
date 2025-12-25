# Batch-S4-2 CP1: JS/AJAX Extracts for Migration

**Purpose:** Extract all COMPAT endpoint calls from CIM view files for SHARED endpoint migration  
**Date:** 2025-12-24  
**Status:** Ready for migration rewrite

---

## File 1: `product/create.blade.php`

### 1.1 `product.getsubcategory` call (CategoryId change handler)
**Location:** Lines 254-323  
**Trigger:** `#CategoryId` change event

```javascript
$(document).on('change', '#CategoryId', function (e){
    var id = this.value;
    if (id && id != '0') {
        $('#btnNewSubCategory').prop('disabled', false);
        $('#btnNewItem').prop('disabled', false);
        // Store selected category for modals
        var categoryName = $('#CategoryId option:selected').text();
        $('#newSubCategoryCategoryId').val(id);
        $('#newSubCategoryCategoryName').val(categoryName);
        $('#newItemCategoryId').val(id);
        $('#newItemCategoryName').val(categoryName);
    } else {
        $('#btnNewSubCategory').prop('disabled', true);
        $('#btnNewItem').prop('disabled', true);
    }
    $.ajax({
        url: '{{ route('product.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">*</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId').html(subcategory);
            // ... attribute handling commented out ...

            var producttype = '<option value="0">*</option>';
            if (data.producttype.length > 0) {
                var selected = data.producttype.length == 1 ? '' : '';
                data.producttype.forEach(element => {
                    producttype += '<option value="' + element.ItemId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#ItemId').html(producttype);

            var make = '<option value="0">*</option>';
            if (data.make.length > 0) {
                var selected = data.make.length == 1 ? '' : '';
                data.make.forEach(element => {
                    make += '<option value="' + element.MakeId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#MakeId').html(make);
            getdescription();
        }
    });
});
```

**Current endpoint:** `product.getsubcategory`  
**Current payload:** `{ subcategory: [...], producttype: [...], make: [...] }`  
**Migration target:** Split into:
- `api.category.subcategories` (for subcategory)
- `api.category.items` (for producttype)
- `api.category.makes` (for make)

---

### 1.2 `product.getseries` call (MakeId change handler)
**Location:** Lines 347-369  
**Trigger:** `#MakeId` change event

```javascript
$(document).on('change', '#MakeId', function (e){
    var MakeId = this.value;
    var CategoryId = $('#CategoryId').val()
    $.ajax({
        url: '{{ route('product.getseries') }}',
        type: 'GET',
        data: {
            'MakeId': MakeId,
            'CategoryId': CategoryId
        },
        dataType: 'json',
        success: function(data) {
            var series = '<option value="0">*</option>';
            if (data.series.length > 0) {
                var selected = data.series.length == 1 ? '' : '';
                data.series.forEach(element => {
                    series += '<option value="' + element.SeriesId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SeriesId').html(series);
        }
    });
});
```

**Current endpoint:** `product.getseries`  
**Current payload:** `{ series: [{SeriesId, Name}] }`  
**Migration target:** `api.make.{makeId}/series?categoryId={CategoryId}`

---

### 1.3 `product.getgeneric` call (getdescription function)
**Location:** Lines 372-397  
**Trigger:** Called after CategoryId/SubCategoryId/ItemId changes

```javascript
function getdescription(){
    var CategoryId = $('#CategoryId').val();
    var SubCategoryId = $('#SubCategoryId').val();
    var ItemId = $('#ItemId').val();
    $.ajax({
        url: '{{ route('product.getgeneric') }}',
        type: 'GET',
        data: {
            "_token": "{{ csrf_token() }}",
            'CategoryId': CategoryId,
            'SubCategoryId': SubCategoryId,
            'ItemId': ItemId
        },
        dataType: 'json',
        success: function(data) {
            var description = '<option value="0">*</option>';
            if (data.description.length > 0) {
                var selected = data.description.length == 1 ? '' : '';
                data.description.forEach(element => {
                    description += '<option value="' + element.ProductId + '">' + element.Name + '</option>';
                });
            }
            $('#GenericId').html(description);
        }
    });
}
```

**Current endpoint:** `product.getgeneric`  
**Current payload:** `{ description: [{ProductId, Name}] }`  
**Migration target:** `api.category.{categoryId}/products?subcategoryId={SubCategoryId}&itemId={ItemId}`

---

## File 2: `product/edit.blade.php`

### 2.1 `product.getsubcategory` call (loadItemsForCategory function)
**Location:** Lines 382-398  
**Trigger:** Called on page load if CategoryId is set

```javascript
function loadItemsForCategory(categoryId, preserveItemId) {
    $.ajax({
        url: '{{ route('product.getsubcategory',['_group_id']) }}'.replace('_group_id', categoryId),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var producttype = '<option value="0">*</option>';
            if (data.producttype && data.producttype.length > 0) {
                data.producttype.forEach(element => {
                    var selected = (preserveItemId && element.ItemId == preserveItemId) ? 'selected' : '';
                    producttype += '<option value="' + element.ItemId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#ItemId').html(producttype).trigger('change.select2');
        }
    });
}
```

**Current endpoint:** `product.getsubcategory`  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `api.category.{categoryId}/items` (may need subcategory filter)

---

### 2.2 `product.getsubcategory` call (CategoryId change handler)
**Location:** Lines 400-444  
**Trigger:** `#CategoryId` change event

```javascript
$(document).on('change', '#CategoryId', function (e){
    var id = this.value;
    $.ajax({
        url: '{{ route('product.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">*</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId').html(subcategory).trigger('change.select2');

            var producttype = '<option value="0">*</option>';
            if (data.producttype && data.producttype.length > 0) {
                data.producttype.forEach(element => {
                    producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
                });
            }
            $('#ItemId').html(producttype).trigger('change.select2');

            var series = '<option value="0">*</option>';
            if (data.series.length > 0) {
                var selected = data.series.length == 1 ? '' : '';
                data.series.forEach(element => {
                    series += '<option value="' + element.SeriesId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SeriesId').html(series);

            var make = '<option value="0">*</option>';
            if (data.make.length > 0) {
                var selected = data.make.length == 1 ? '' : '';
                data.make.forEach(element => {
                    make += '<option value="' + element.MakeId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#MakeId').html(make);
            getdescription();
        }
    });
});
```

**Current endpoint:** `product.getsubcategory`  
**Current payload:** `{ subcategory: [...], producttype: [...], series: [...], make: [...] }`  
**Migration target:** Split into multiple SHARED endpoints

---

### 2.3 `product.getproducttype` call (SubCategoryId change handler)
**Location:** Lines 445-482  
**Trigger:** `#SubCategoryId` change event

```javascript
$(document).on('change', '#SubCategoryId', function (e){
    var id = this.value;
    var categoryId = $('#CategoryId').val();
    
    // Update ItemId based on SubCategory (if available) or Category
    if (id && id != '0') {
        $.ajax({
            url: '{{ route('product.getproducttype',['_group_id']) }}'.replace('_group_id', id),
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                var producttype = '<option value="0">*</option>';
                if (data.producttype && data.producttype.length > 0) {
                    data.producttype.forEach(element => {
                        producttype += '<option value="' + element.ItemId + '">' + element.Name + '</option>';
                    });
                }
                $('#ItemId').html(producttype).trigger('change.select2');
                getdescription();
            },
            error: function() {
                // Fallback: load items by category if subcategory API fails
                if (categoryId && categoryId != '0') {
                    var currentItemId = $('#ItemId').val();
                    loadItemsForCategory(categoryId, currentItemId);
                }
                getdescription();
            }
        });
    } else if (categoryId && categoryId != '0') {
        // If SubCategory is cleared, reload items by Category
        var currentItemId = $('#ItemId').val();
        loadItemsForCategory(categoryId, currentItemId);
        getdescription();
    } else {
        getdescription();
    }
});
```

**Current endpoint:** `product.getproducttype`  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `api.category.{categoryId}/items?subcategory={SubCategoryId}`

---

### 2.4 `product.getseries` call (MakeId change handler)
**Location:** Lines 488-511  
**Trigger:** `#MakeId` change event

```javascript
$(document).on('change', '#MakeId', function (e){
    var MakeId = this.value;
    var CategoryId = $('#CategoryId').val()

    $.ajax({
        url: '{{ route('product.getseries') }}',
        type: 'GET',
        dataType: 'json',
        data: {
            'MakeId': MakeId,
            'CategoryId': CategoryId
        },
        success: function(data) {
            var series = '<option value="0">*</option>';
            if (data.series.length > 0) {
                var selected = data.series.length == 1 ? '' : '';
                data.series.forEach(element => {
                    series += '<option value="' + element.SeriesId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SeriesId').html(series).trigger('change.select2');
        }
    });
});
```

**Current endpoint:** `product.getseries`  
**Current payload:** `{ series: [{SeriesId, Name}] }`  
**Migration target:** `api.make.{makeId}/series?categoryId={CategoryId}`

---

### 2.5 `product.getgeneric` call (getdescription function)
**Location:** Lines 645-670  
**Trigger:** Called after CategoryId/SubCategoryId/ItemId changes

```javascript
function getdescription(){
    var CategoryId = $('#CategoryId').val();
    var SubCategoryId = $('#SubCategoryId').val();
    var ItemId = $('#ItemId').val();
    $.ajax({
        url: '{{ route('product.getgeneric') }}',
        type: 'GET',
        data: {
            "_token": "{{ csrf_token() }}",
            'CategoryId': CategoryId,
            'SubCategoryId': SubCategoryId,
            'ItemId': ItemId
        },
        dataType: 'json',
        success: function(data) {
            var description = '<option value="0">*</option>';
            if (data.description.length > 0) {
                var selected = data.description.length == 1 ? '' : '';
                data.description.forEach(element => {
                    description += '<option value="' + element.ProductId + '">' + element.Name + '</option>';
                });
            }
            $('#GenericId').html(description);
        }
    });
}
```

**Current endpoint:** `product.getgeneric`  
**Current payload:** `{ description: [{ProductId, Name}] }`  
**Migration target:** `api.category.{categoryId}/products?subcategoryId={SubCategoryId}&itemId={ItemId}`

---

## File 3: `generic/create.blade.php`

### 3.1 `product.getsubcategory` call (CategoryId change handler)
**Location:** Lines 210-295  
**Trigger:** `#CategoryId` change event

```javascript
$(document).on('change', '#CategoryId', function (e){
    var id = this.value;
    if (id && id != '0') {
        $('#btnNewSubCategory').prop('disabled', false);
        $('#btnNewItem').prop('disabled', false);
        // Store selected category for modals
        var categoryName = $('#CategoryId option:selected').text();
        $('#newSubCategoryCategoryId').val(id);
        $('#newSubCategoryCategoryName').val(categoryName);
        $('#newItemCategoryId').val(id);
        $('#newItemCategoryName').val(categoryName);
    } else {
        $('#btnNewSubCategory').prop('disabled', true);
        $('#btnNewItem').prop('disabled', true);
    }
    $.ajax({
        url: '{{ route('product.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">*</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId').html(subcategory);

            var producttype = '<option value="0">*</option>';
            if (data.producttype.length > 0) {
                var selected = data.producttype.length == 1 ? '' : '';
                data.producttype.forEach(element => {
                    producttype += '<option value="' + element.ItemId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#ItemId').html(producttype);

            $('#attribute').html('');
            if (data.attribute.length > 0) {
                data.attribute.forEach(element => {
                    // ... attribute rendering code ...
                });
            }
        }
    });
});
```

**Current endpoint:** `product.getsubcategory`  
**Current payload:** `{ subcategory: [...], producttype: [...], attribute: [...] }`  
**Migration target:** Split into:
- `api.category.subcategories` (for subcategory)
- `api.category.items` (for producttype)
- **Note:** Attributes are NOT in CatalogLookupContract - must keep COMPAT call for attributes or handle separately

---

## File 4: `generic/edit.blade.php`

### 4.1 `product.getsubcategory` call (loadItemsForCategory function)
**Location:** Lines 423-452  
**Trigger:** Called on page load if CategoryId is set

```javascript
function loadItemsForCategory(categoryId, preserveItemId) {
    $.ajax({
        url: '{{ route('product.getsubcategory',['_group_id']) }}'.replace('_group_id', categoryId),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var producttype = '<option value="0">*</option>';
            if (data.producttype && data.producttype.length > 0) {
                data.producttype.forEach(element => {
                    var selected = (preserveItemId && element.ItemId == preserveItemId) ? 'selected' : '';
                    producttype += '<option value="' + element.ItemId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#ItemId').html(producttype);
            // ✅ NEPL Standard: Reinitialize Select2 after AJAX update
            if (typeof reinitSelect2 === 'function') {
                reinitSelect2($('#ItemId').closest('.card'));
            } else if (typeof window.reinitSelect2 === 'function') {
                window.reinitSelect2($('#ItemId').closest('.card'));
            } else {
                // Fallback: Manual Select2 initialization
                $('#ItemId').select2({
                    allowClear: true,
                    placeholder: 'Select...',
                    width: '100%'
                });
            }
        }
    });
}
```

**Current endpoint:** `product.getsubcategory`  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `api.category.{categoryId}/items` (may need subcategory filter)

---

### 4.2 `product.getsubcategory` call (CategoryId change handler)
**Location:** Lines 454-532  
**Trigger:** `#CategoryId` change event

```javascript
$(document).on('change', '#CategoryId', function (e){
    var id = this.value;
    $.ajax({
        url: '{{ route('product.getsubcategory',['_group_id']) }}'.replace('_group_id', id),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var subcategory = '<option value="0">*</option>';
            if (data.subcategory.length > 0) {
                var selected = data.subcategory.length == 1 ? '' : '';
                data.subcategory.forEach(element => {
                    subcategory += '<option value="' + element.SubCategoryId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#SubCategoryId').html(subcategory);
            // ✅ NEPL Standard: Reinitialize Select2 after AJAX update
            if (typeof reinitSelect2 === 'function') {
                reinitSelect2($('#SubCategoryId').closest('.card'));
            } else if (typeof window.reinitSelect2 === 'function') {
                window.reinitSelect2($('#SubCategoryId').closest('.card'));
            } else {
                // Fallback: Manual Select2 initialization
                $('#SubCategoryId').select2({
                    allowClear: true,
                    placeholder: 'Select...',
                    width: '100%'
                });
            }
            
            // Update ItemId dropdown
            var producttype = '<option value="0">*</option>';
            if (data.producttype && data.producttype.length > 0) {
                var currentItemId = $('#ItemId').val();
                data.producttype.forEach(element => {
                    var selected = (currentItemId && element.ItemId == currentItemId) ? 'selected' : '';
                    producttype += '<option value="' + element.ItemId + '" ' + selected + '>' + element.Name + '</option>';
                });
            }
            $('#ItemId').html(producttype);
            // ✅ NEPL Standard: Reinitialize Select2 after AJAX update
            if (typeof reinitSelect2 === 'function') {
                reinitSelect2($('#ItemId').closest('.card'));
            } else if (typeof window.reinitSelect2 === 'function') {
                window.reinitSelect2($('#ItemId').closest('.card'));
            } else {
                // Fallback: Manual Select2 initialization
                $('#ItemId').select2({
                    allowClear: true,
                    placeholder: 'Select...',
                    width: '100%'
                });
            }
            
            $('#attribute').html('');
            if (data.attribute.length > 0) {
                data.attribute.forEach(element => {
                    // ... attribute rendering code ...
                });
            }
        }
    });
});
```

**Current endpoint:** `product.getsubcategory`  
**Current payload:** `{ subcategory: [...], producttype: [...], attribute: [...] }`  
**Migration target:** Split into:
- `api.category.subcategories` (for subcategory)
- `api.category.items` (for producttype)
- **Note:** Attributes are NOT in CatalogLookupContract - must keep COMPAT call for attributes or handle separately

---

### 4.3 `product.getproducttype` call (SubCategoryId change handler)
**Location:** Lines 534-581  
**Trigger:** `#SubCategoryId` change event

```javascript
$(document).on('change', '#SubCategoryId', function (e){
    var id = this.value;
    var categoryId = $('#CategoryId').val();
    
    // Update ItemId based on SubCategory (if available) or Category
    if (id && id != '0') {
        $.ajax({
            url: '{{ route('product.getproducttype',['_group_id']) }}'.replace('_group_id', id),
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                var producttype = '<option value="0">*</option>';
                if (data.producttype && data.producttype.length > 0) {
                    var currentItemId = $('#ItemId').val();
                    data.producttype.forEach(element => {
                        var selected = (currentItemId && element.ItemId == currentItemId) ? 'selected' : '';
                        producttype += '<option value="' + element.ItemId + '" ' + selected + '>' + element.Name + '</option>';
                    });
                }
                $('#ItemId').html(producttype);
                // ✅ NEPL Standard: Reinitialize Select2 after AJAX update
                if (typeof reinitSelect2 === 'function') {
                    reinitSelect2($('#ItemId').closest('.card'));
                } else if (typeof window.reinitSelect2 === 'function') {
                    window.reinitSelect2($('#ItemId').closest('.card'));
                } else {
                    // Fallback: Manual Select2 initialization
                    $('#ItemId').select2({
                        allowClear: true,
                        placeholder: 'Select...',
                        width: '100%'
                    });
                }
            },
            error: function() {
                // Fallback: load items by category if subcategory API fails
                if (categoryId && categoryId != '0') {
                    var currentItemId = $('#ItemId').val();
                    loadItemsForCategory(categoryId, currentItemId);
                }
            }
        });
    } else if (categoryId && categoryId != '0') {
        // If SubCategory is cleared, reload items by Category
        var currentItemId = $('#ItemId').val();
        loadItemsForCategory(categoryId, currentItemId);
    }
});
```

**Current endpoint:** `product.getproducttype`  
**Current payload:** `{ producttype: [{ItemId, Name}] }`  
**Migration target:** `api.category.{categoryId}/items?subcategory={SubCategoryId}`

---

## Summary: Migration Mapping

| COMPAT Endpoint | Current Payload Shape | SHARED Target | Response Transformation |
|---|---|---|---|
| `product.getgeneric` | `{ description: [{ProductId, Name}] }` | `api.category.{categoryId}/products?subcategoryId={SubCategoryId}&itemId={ItemId}` | Extract `description` array, map `ProductId` → `id`, `Name` → `text` |
| `product.getproducttype` | `{ producttype: [{ItemId, Name}] }` | `api.category.{categoryId}/items?subcategory={SubCategoryId}` | Extract `producttype` array, map `ItemId` → `id`, `Name` → `text` |
| `product.getseries` | `{ series: [{SeriesId, Name}] }` | `api.make.{makeId}/series?categoryId={CategoryId}` | Extract `series` array, map `SeriesId` → `id`, `Name` → `text` |
| `product.getsubcategory` | `{ subcategory: [...], producttype: [...], make: [...] }` | Split: `api.category.subcategories`, `api.category.items`, `api.category.makes` | Multiple calls, extract nested arrays, map to `{id, text}` |

**Note:** Attributes from `product.getsubcategory` are NOT in CatalogLookupContract - must handle separately (keep COMPAT call for attributes or create separate attribute endpoint).

---

**Ready for migration rewrite in CP1 phase order:**
1. Phase-1: `product.getgeneric` → `api.category.products`
2. Phase-2: `product.getproducttype` → `api.category.items`
3. Phase-3: `product.getseries` → `api.make.series`
4. Phase-4: `product.getsubcategory` → Split into multiple SHARED calls

