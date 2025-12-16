> Source: source_snapshot/V2_FEEDER_LIBRARY_PHASE_1_2_TESTING_GUIDE.md
> Bifurcated into: features/feeder_library/workflows/V2_FEEDER_LIBRARY_PHASE_1_2_TESTING_GUIDE.md
> Module: Feeder Library > Workflows
> Date: 2025-12-17 (IST)

# V2 Feeder Library - Phase 1 & 2 Testing Guide

**Date:** December 11, 2025  
**Status:** 📋 **TESTING GUIDE**

---

## 🎯 TESTING OBJECTIVES

Verify that:
1. ✅ Database migration executed correctly
2. ✅ Model scopes work properly
3. ✅ Controller methods are accessible
4. ✅ Routes are registered correctly
5. ✅ CRUD operations work end-to-end

---

## 📋 TEST 1: DATABASE MIGRATION VERIFICATION

### 1.1 Check Migration Status

```bash
php artisan migrate:status | grep add_template_fields_to_master_boms
```

**Expected:** Migration should show as "Ran"

### 1.2 Verify Database Schema

```bash
php artisan tinker
```

Then run:
```php
// Check if columns exist
$columns = DB::select("SHOW COLUMNS FROM master_boms LIKE 'TemplateType'");
print_r($columns);

$columns = DB::select("SHOW COLUMNS FROM master_boms LIKE 'IsActive'");
print_r($columns);

$columns = DB::select("SHOW COLUMNS FROM master_boms LIKE 'DefaultFeederName'");
print_r($columns);

// Check indexes
$indexes = DB::select("SHOW INDEXES FROM master_boms WHERE Column_name IN ('TemplateType', 'IsActive')");
print_r($indexes);
```

**Expected:**
- All 3 columns should exist
- `TemplateType` and `IsActive` should have indexes
- `IsActive` should have default value = 1

### 1.3 Test Column Defaults

```php
// In tinker
$bom = new App\Models\MasterBom();
$bom->Name = 'Test BOM';
$bom->save();

// Check IsActive default
echo $bom->IsActive; // Should be 1 (true)
```

---

## 📋 TEST 2: MODEL SCOPES VERIFICATION

### 2.1 Test FeederTemplates Scope

```bash
php artisan tinker
```

```php
// Test feederTemplates scope
$feeders = App\Models\MasterBom::feederTemplates()->get();
echo "Feeder templates count: " . $feeders->count() . "\n";

// Should return empty collection initially (no FEEDER templates yet)
// But should not throw errors
```

**Expected:** Returns empty collection, no errors

### 2.2 Test Templates Scope

```php
// Test templates scope (all TemplateType values)
$allTemplates = App\Models\MasterBom::templates()->get();
echo "All templates count: " . $allTemplates->count() . "\n";
```

**Expected:** Returns empty collection (no templates with TemplateType set yet)

### 2.3 Test Active Scope

```php
// Test active scope
$active = App\Models\MasterBom::active()->get();
echo "Active templates count: " . $active->count() . "\n";
```

**Expected:** Returns all MasterBoms where IsActive = 1

### 2.4 Create Test Template and Verify Scopes

```php
// Create a test feeder template
$template = App\Models\MasterBom::create([
    'Name' => 'Test Feeder Template',
    'DefaultFeederName' => 'Test Feeder',
    'TemplateType' => 'FEEDER',
    'IsActive' => 1,
]);

// Verify it appears in feederTemplates scope
$feeders = App\Models\MasterBom::feederTemplates()->get();
echo "Feeder templates after creation: " . $feeders->count() . "\n";
echo "First feeder name: " . $feeders->first()->Name . "\n";

// Verify it appears in templates scope
$allTemplates = App\Models\MasterBom::templates()->get();
echo "All templates after creation: " . $allTemplates->count() . "\n";

// Test inactive
$template->IsActive = 0;
$template->save();

$feeders = App\Models\MasterBom::feederTemplates()->get();
echo "Feeder templates after deactivation: " . $feeders->count() . "\n";
// Should be 0 (feederTemplates only returns active)

// Cleanup
$template->delete();
```

**Expected:**
- After creation: feederTemplates count = 1
- After deactivation: feederTemplates count = 0
- templates scope still shows it (but not active)

---

## 📋 TEST 3: ROUTES VERIFICATION

### 3.1 List All Feeder Library Routes

```bash
php artisan route:list | grep feeder-library
```

**Expected Output:**
```
GET|HEAD  feeder-library                    feeder-library.index
POST      feeder-library                    feeder-library.store
GET|HEAD  feeder-library/create             feeder-library.create
GET|HEAD  feeder-library/{id}               feeder-library.show
PUT       feeder-library/{id}               feeder-library.update
GET|HEAD  feeder-library/{id}/edit          feeder-library.edit
PATCH     feeder-library/{id}/toggle         feeder-library.toggle
```

### 3.2 Test Route Accessibility (Manual)

**Using Browser:**
1. Login to your application
2. Navigate to: `http://your-domain/feeder-library`
3. **Expected:** Should load (may show empty list or error if views don't exist yet)

**Using cURL:**
```bash
# Test index route (requires authentication)
curl -X GET http://your-domain/feeder-library \
  -H "Cookie: your_session_cookie" \
  -v
```

---

## 📋 TEST 4: CONTROLLER METHODS VERIFICATION

### 4.1 Test Index Method (JSON Response)

```bash
php artisan tinker
```

```php
// Create test request
$request = new Illuminate\Http\Request();
$request->merge(['format' => 'json']);

// Create controller instance
$controller = new App\Http\Controllers\FeederTemplateController();

// Test index method
try {
    $response = $controller->index($request);
    echo "Index method works!\n";
    if ($response instanceof Illuminate\Http\JsonResponse) {
        $data = json_decode($response->getContent(), true);
        print_r($data);
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
```

**Expected:** Returns JSON response with success: true and data array

### 4.2 Test Store Method

```php
// Create test request with data
$request = new Illuminate\Http\Request();
$request->merge([
    'Name' => 'Test Feeder Template',
    'DefaultFeederName' => 'Test Feeder',
    'Description' => 'Test description',
]);

// Test store method
$controller = new App\Http\Controllers\FeederTemplateController();
try {
    $response = $controller->store($request);
    echo "Store method works!\n";
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

// Verify template was created
$template = App\Models\MasterBom::where('Name', 'Test Feeder Template')->first();
if ($template) {
    echo "Template created successfully!\n";
    echo "TemplateType: " . $template->TemplateType . "\n";
    echo "IsActive: " . ($template->IsActive ? '1' : '0') . "\n";
    echo "DefaultFeederName: " . $template->DefaultFeederName . "\n";
    
    // Cleanup
    $template->delete();
    echo "Test template deleted.\n";
}
```

**Expected:**
- Template created with TemplateType = 'FEEDER'
- IsActive = 1
- DefaultFeederName = 'Test Feeder'

### 4.3 Test ToggleActive Method

```php
// Create test template
$template = App\Models\MasterBom::create([
    'Name' => 'Toggle Test Template',
    'TemplateType' => 'FEEDER',
    'IsActive' => 1,
]);

$id = $template->MasterBomId;

// Test toggleActive
$controller = new App\Http\Controllers\FeederTemplateController();
$response = $controller->toggleActive($id);

$data = json_decode($response->getContent(), true);
echo "Toggle response: ";
print_r($data);

// Verify toggle worked
$template->refresh();
echo "IsActive after toggle: " . ($template->IsActive ? '1' : '0') . "\n";

// Cleanup
$template->delete();
```

**Expected:**
- JSON response: `{success: true, isActive: false}`
- Template IsActive changed from 1 to 0

---

## 📋 TEST 5: END-TO-END MANUAL TESTING

### 5.1 Create Template via Controller (Full Flow)

**Step 1: Create Template**
```php
// In tinker
$controller = new App\Http\Controllers\FeederTemplateController();

$request = new Illuminate\Http\Request();
$request->merge([
    'Name' => 'DB-1 Feeder Template',
    'DefaultFeederName' => 'DB-1',
    'UniqueNo' => 'FEED-001',
    'Description' => 'Main DB feeder template',
]);

$response = $controller->store($request);
echo "Template created!\n";
```

**Step 2: List Templates**
```php
$request = new Illuminate\Http\Request();
$response = $controller->index($request);
echo "Index works!\n";
```

**Step 3: View Template**
```php
$template = App\Models\MasterBom::where('Name', 'DB-1 Feeder Template')->first();
$response = $controller->show($template->MasterBomId);
echo "Show works!\n";
```

**Step 4: Edit Template**
```php
$request = new Illuminate\Http\Request();
$request->merge([
    'Name' => 'DB-1 Feeder Template Updated',
    'DefaultFeederName' => 'DB-1 Updated',
    'Description' => 'Updated description',
    'IsActive' => 1,
]);

$response = $controller->update($request, $template->MasterBomId);
echo "Update works!\n";
```

**Step 5: Toggle Active**
```php
$response = $controller->toggleActive($template->MasterBomId);
$data = json_decode($response->getContent(), true);
echo "Toggle response: " . json_encode($data) . "\n";
```

**Step 6: Cleanup**
```php
$template->delete();
echo "Test complete!\n";
```

---

## 📋 TEST 6: VALIDATION TESTING

### 6.1 Test Required Fields

```php
// Test store with missing Name (should fail)
$request = new Illuminate\Http\Request();
$request->merge([
    'DefaultFeederName' => 'Test',
    // Name is missing
]);

$controller = new App\Http\Controllers\FeederTemplateController();
try {
    $response = $controller->store($request);
    // Should redirect with errors
    echo "Validation should have failed\n";
} catch (Exception $e) {
    echo "Validation error caught: " . $e->getMessage() . "\n";
}
```

**Expected:** Validation should fail, redirect with errors

### 6.2 Test Field Length Limits

```php
// Test with Name too long
$request = new Illuminate\Http\Request();
$request->merge([
    'Name' => str_repeat('A', 300), // Exceeds max:255
]);

// Should fail validation
```

---

## 📋 TEST 7: DATABASE INTEGRITY

### 7.1 Verify Foreign Key Relationships

```php
// Create template with items
$template = App\Models\MasterBom::create([
    'Name' => 'Test Template with Items',
    'TemplateType' => 'FEEDER',
    'IsActive' => 1,
]);

// Verify relationship works
$items = $template->masterbomitem;
echo "Items count: " . $items->count() . "\n";

// Cleanup
$template->delete();
```

---

## ✅ QUICK TEST SCRIPT

Save this as `test_phase_1_2.php` and run: `php artisan tinker < test_phase_1_2.php`

```php
<?php

echo "=== Phase 1 & 2 Testing ===\n\n";

// Test 1: Database columns
echo "1. Testing database columns...\n";
$columns = DB::select("SHOW COLUMNS FROM master_boms WHERE Field IN ('TemplateType', 'IsActive', 'DefaultFeederName')");
if (count($columns) === 3) {
    echo "   ✅ All columns exist\n";
} else {
    echo "   ❌ Missing columns\n";
}

// Test 2: Model scopes
echo "\n2. Testing model scopes...\n";
$feeders = App\Models\MasterBom::feederTemplates()->get();
echo "   ✅ feederTemplates() scope works (count: " . $feeders->count() . ")\n";

$templates = App\Models\MasterBom::templates()->get();
echo "   ✅ templates() scope works (count: " . $templates->count() . ")\n";

$active = App\Models\MasterBom::active()->get();
echo "   ✅ active() scope works (count: " . $active->count() . ")\n";

// Test 3: Create and verify template
echo "\n3. Testing template creation...\n";
$template = App\Models\MasterBom::create([
    'Name' => 'Test Feeder Template',
    'DefaultFeederName' => 'Test Feeder',
    'TemplateType' => 'FEEDER',
    'IsActive' => 1,
]);

if ($template && $template->TemplateType === 'FEEDER') {
    echo "   ✅ Template created successfully\n";
    echo "   ✅ TemplateType: " . $template->TemplateType . "\n";
    echo "   ✅ IsActive: " . ($template->IsActive ? '1' : '0') . "\n";
    
    // Test scopes with data
    $feeders = App\Models\MasterBom::feederTemplates()->get();
    echo "   ✅ feederTemplates() now returns: " . $feeders->count() . " template(s)\n";
    
    // Cleanup
    $template->delete();
    echo "   ✅ Test template deleted\n";
} else {
    echo "   ❌ Template creation failed\n";
}

// Test 4: Controller
echo "\n4. Testing controller methods...\n";
$controller = new App\Http\Controllers\FeederTemplateController();

$request = new Illuminate\Http\Request();
$request->merge(['format' => 'json']);
try {
    $response = $controller->index($request);
    echo "   ✅ index() method works\n";
} catch (Exception $e) {
    echo "   ❌ index() method error: " . $e->getMessage() . "\n";
}

echo "\n=== Testing Complete ===\n";
```

---

## 🎯 SUCCESS CRITERIA

All tests should pass:
- ✅ Migration executed, columns exist
- ✅ Model scopes return correct results
- ✅ All 7 routes are registered
- ✅ Controller methods execute without errors
- ✅ Templates can be created with TemplateType='FEEDER'
- ✅ Validation works correctly
- ✅ Toggle active/inactive works

---

## 📝 NOTES

- If views don't exist yet, browser tests may show errors - that's expected for Phase 1 & 2
- Focus on backend functionality (database, model, controller, routes)
- Phase 3 will add the UI views

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-11 | Auto | Initial testing guide created | Comprehensive test suite for Phase 1 & 2 |


