> Source: source_snapshot/SECURITY_HARDENING_PHASE1.md
> Bifurcated into: changes/employee/fixes/SECURITY_HARDENING_PHASE1.md
> Module: Employee/Role > Fixes
> Date: 2025-12-17 (IST)

# Security Hardening Phase 1 - Action Plan

**Branch:** sec/hardening-phase-1  
**Created:** December 4, 2025  
**Priority:** HIGH - Production Security

---

## 🎯 Objective

Apply remaining critical security fixes to reach production-ready security standard.

---

## ✅ Already Completed (Dec 3-4, 2025)

- [x] SQL Injection: QuotationController (6 instances) - ✅ Fixed
- [x] SQL Injection: ProjectController (1 instance) - ✅ Fixed  
- [x] CSRF Protection: Re-enabled - ✅ Fixed
- [x] .gitignore: Updated to exclude sensitive files - ✅ Fixed

**Reference:** See commits be6066e, 52effde, 5212b7f

---

## 🔴 Phase 1 Tasks (This Branch)

### Task 1: Add Form Request Validation Classes

**Why:** Move validation logic out of controllers, make it reusable and testable

**Priority:** HIGH  
**Estimated Time:** 2-3 hours  
**Risk:** Low (improves code quality)

**Files to Create:**

#### 1.1 StoreQuotationRequest
```php
// app/Http/Requests/StoreQuotationRequest.php

<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreQuotationRequest extends FormRequest
{
    public function authorize()
    {
        return true; // All authenticated users can create
    }

    public function rules()
    {
        return [
            'ClientId' => 'required|integer|exists:clients,ClientId',
            'ProjectId' => 'required|integer|exists:projects,ProjectId',
            'ContactId' => 'required|integer|exists:contacts,ContactId',
            'SalesId' => 'required|integer|exists:users,id',
            'EmployeeId' => 'required|integer|exists:users,id',
            'QuotationNo' => 'nullable|string|max:20|unique:quotations,QuotationNo',
            'CategoryId' => 'nullable|integer|exists:categories,CategoryId',
            'MakeId' => 'nullable|integer|exists:makes,MakeId',
            'SeriesId' => 'nullable|integer|exists:series,SeriesId',
            'Discount' => 'nullable|numeric|min:0|max:100',
        ];
    }

    public function messages()
    {
        return [
            'ClientId.required' => 'Please select a client.',
            'ClientId.exists' => 'Selected client does not exist.',
            'ProjectId.required' => 'Please select a project.',
            'ContactId.required' => 'Please select a contact person.',
            'QuotationNo.unique' => 'This quotation number already exists.',
        ];
    }
}
```

**Update QuotationController@store:**
```php
// Change from:
public function store(Request $request)

// To:
public function store(StoreQuotationRequest $request)
{
    // Remove manual validation - now automatic!
    // $validator = Validator::make(...) ← DELETE THIS
    
    $validated = $request->validated();
    
    // Rest of code continues...
}
```

**Documentation:** References 28_BUSINESS_RULES.md (Validation Rules section)

---

#### 1.2 UpdateQuotationRequest
```php
// app/Http/Requests/UpdateQuotationRequest.php

<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateQuotationRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'ClientId' => 'required|integer|exists:clients,ClientId',
            'ProjectId' => 'required|integer|exists:projects,ProjectId',
            'ContactId' => 'required|integer|exists:contacts,ContactId',
            'SalesId' => 'required|integer|exists:users,id',
            'EmployeeId' => 'required|integer|exists:users,id',
            'QuotationNo' => 'nullable|string|max:20|unique:quotations,QuotationNo,' . $this->route('quotation') . ',QuotationId',
        ];
    }
}
```

**Update QuotationController@update:**
```php
public function update(UpdateQuotationRequest $request, $id)
{
    $validated = $request->validated();
    // Continue with update logic...
}
```

---

#### 1.3 StoreProductRequest
```php
// app/Http/Requests/StoreProductRequest.php

<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreProductRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'Name' => 'required|string|max:255',
            'CategoryId' => 'required|integer|exists:categories,CategoryId',
            'SubCategoryId' => 'nullable|integer|exists:sub_categories,SubCategoryId',
            'ItemId' => 'nullable|integer|exists:items,ItemId',
            'GenericId' => 'required_if:ProductType,2|integer|exists:products,ProductId',
            'MakeId' => 'nullable|integer|exists:makes,MakeId',
            'SeriesId' => 'nullable|integer|exists:series,SeriesId',
            'SKU' => 'nullable|string|max:100|unique:products,SKU',
            'ProductType' => 'required|integer|in:1,2',
        ];
    }
}
```

---

### Task 2: Add Input Sanitization for Dynamic Fields

**Why:** Currently using dynamic field access like `$request->$CategoryId` without validation

**Priority:** HIGH  
**Risk:** Medium (potential security issue)

**File:** QuotationController.php  
**Lines:** ~98-105 (store method), ~250-260 (update method)

**Current Code (Vulnerable):**
```php
foreach($counts as $count){
    $CategoryId = 'CategoryId_'.$count;
    $value = $request->$CategoryId;  // ⚠️ No validation!
}
```

**Secure Code:**
```php
foreach($counts as $count){
    $CategoryId = 'CategoryId_'.$count;
    
    // Validate dynamic field exists and is integer
    if($request->has($CategoryId)) {
        $value = filter_var($request->$CategoryId, FILTER_VALIDATE_INT);
        
        if($value === false || $value < 0) {
            continue; // Skip invalid values
        }
        
        // Additional check: CategoryId exists in database
        if($value > 0 && !Category::where('CategoryId', $value)->exists()) {
            continue;
        }
        
        // Now safe to use $value
    }
}
```

**Documentation:** References 28_BUSINESS_RULES.md (Validation section)

---

### Task 3: Strengthen CSRF Protection

**Why:** Ensure all AJAX routes have CSRF token validation

**Priority:** MEDIUM  
**Risk:** Medium

**Check All AJAX Routes:**
```php
// routes/web.php

// These routes must have CSRF protection:
POST /quotation/addmoresale
POST /quotation/addmorebom
POST /quotation/addmoreitem
POST /quotation/revision/{id}
```

**Verify JavaScript Includes Token:**
```javascript
// In resources/views (check all quotation views)

// Should have in <head>:
<meta name="csrf-token" content="{{ csrf_token() }}">

// Should have in JavaScript:
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

// Or in each AJAX call:
$.ajax({
    url: '/quotation/addmoresale',
    type: 'POST',
    data: {
        _token: '{{ csrf_token() }}',
        // ... other data
    }
});
```

**Action:** Verify all views sending POST requests include CSRF token

**Documentation:** References 36_SECURITY_GUIDE.md (CSRF Protection section)

---

### Task 4: Add Rate Limiting

**Why:** Prevent brute force attacks and API abuse

**Priority:** MEDIUM  
**Risk:** Low

**Implementation:**
```php
// app/Http/Kernel.php

protected $middlewareGroups = [
    'web' => [
        // ... existing middleware
        \Illuminate\Routing\Middleware\ThrottleRequests::class.':web',
    ],
];

protected $middlewareAliases = [
    // ... existing
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
];
```

**Apply to Routes:**
```php
// routes/web.php

// Login route (prevent brute force)
Route::post('/login', [LoginController::class, 'login'])
    ->middleware('throttle:5,1'); // 5 attempts per minute

// AJAX routes (prevent spam)
Route::post('/quotation/addmoresale', [QuotationController::class, 'addmoresale'])
    ->middleware('throttle:60,1'); // 60 requests per minute
```

**Documentation:** References 36_SECURITY_GUIDE.md (Security Best Practices)

---

### Task 5: Add Database Transaction Wrapper

**Why:** Ensure data consistency in complex operations

**Priority:** MEDIUM  
**Risk:** Low (improves reliability)

**Update QuotationController@update:**
```php
public function update(UpdateQuotationRequest $request, $id)
{
    try {
        DB::transaction(function() use ($request, $id) {
            // All update operations here
            // If ANY fails, ALL rollback!
            
            // Update quotation
            Quotation::where('QuotationId', $id)->update([...]);
            
            // Soft delete old items
            QuotationSale::where('QuotationId', $id)->update(['Status' => 1]);
            
            // Insert new items (nested loops)
            foreach($sales as $sale) {
                // ...
            }
            
            // Calculate totals
            DB::select("CALL quotationAmount(?)", [$id]);
        });
        
        return redirect()->route('quotation.index')
            ->with('success', 'Quotation updated successfully');
            
    } catch (\Exception $e) {
        Log::error('Quotation update failed: ' . $e->getMessage());
        
        return redirect()->back()
            ->with('error', 'Failed to update quotation. Please try again.')
            ->withInput();
    }
}
```

**Documentation:** References 05_DATA_FLOW.md (Transaction Flow section)

---

### Task 6: Add Logging for Critical Operations

**Why:** Audit trail and debugging

**Priority:** MEDIUM  
**Risk:** Low

**Implementation:**
```php
use Illuminate\Support\Facades\Log;

// In QuotationController@store
Log::info('Quotation created', [
    'quotation_no' => $QuotationNo,
    'client_id' => $request->ClientId,
    'user' => Auth::id(),
    'timestamp' => now()
]);

// In QuotationController@revision
Log::info('Quotation revision created', [
    'original_id' => $id,
    'revision_no' => $QuotationNo,
    'user' => Auth::id()
]);

// In QuotationController@destroy
Log::warning('Quotation deleted', [
    'quotation_id' => $id,
    'quotation_no' => $quotation->QuotationNo,
    'user' => Auth::id()
]);
```

---

## 📋 **Implementation Order**

```
PRIORITY ORDER (Do in this sequence):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Week 1, Day 1-2 (4 hours):
└── Task 1: Form Request Classes
    ├── Create StoreQuotationRequest
    ├── Create UpdateQuotationRequest
    ├── Create StoreProductRequest
    ├── Update controllers to use them
    └── Test validation works

Week 1, Day 3 (2 hours):
└── Task 2: Sanitize Dynamic Fields
    ├── Identify all dynamic field access
    ├── Add validation/sanitization
    └── Test with invalid inputs

Week 1, Day 4 (2 hours):
└── Task 3: Verify CSRF on AJAX
    ├── Check all Blade views
    ├── Verify token in AJAX calls
    └── Test AJAX operations work

Week 1, Day 5 (2 hours):
└── Task 4: Add Rate Limiting
    ├── Configure throttle middleware
    ├── Apply to login/AJAX routes
    └── Test limits enforced

Week 2, Day 1 (2 hours):
└── Task 5: Add Transaction Wrapper
    ├── Wrap QuotationController@update
    ├── Wrap QuotationController@revision
    └── Test rollback on errors

Week 2, Day 2 (1 hour):
└── Task 6: Add Logging
    ├── Log critical operations
    ├── Test logs written
    └── Document log format

TOTAL TIME: ~13 hours over 2 weeks
```

---

## 🎯 **Task 1 - IMMEDIATE ACTION (Start Now)**

### Create Form Request Classes

**Step 1: Create the files**

```bash
php artisan make:request StoreQuotationRequest
php artisan make:request UpdateQuotationRequest
php artisan make:request StoreProductRequest
php artisan make:request StoreClientRequest
php artisan make:request StorePriceRequest
```

**Step 2: Edit each file with validation rules (I'll provide exact code)**

**Step 3: Update controllers to use them**

**Step 4: Test that validation works**

**Step 5: Commit:**
```bash
git add app/Http/Requests/
git commit -m "security: Add Form Request validation classes

- StoreQuotationRequest: Validate quotation creation
- UpdateQuotationRequest: Validate quotation updates  
- StoreProductRequest: Validate product creation
- StoreClientRequest: Validate client creation
- StorePriceRequest: Validate pricing

References:
- 28_BUSINESS_RULES.md (Validation Rules)
- 36_SECURITY_GUIDE.md (Security Best Practices)

Impact: Stronger validation, cleaner controllers, better error messages"
```

---

## 📊 **Success Metrics**

After Phase 1 completion:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| SQL Injection Vulnerabilities | 7 | 0 | ✅ 100% |
| CSRF Coverage | 0% | 100% | ✅ 100% |
| Form Request Validation | 0 | 5+ | ✅ New |
| Input Sanitization | Partial | Complete | ✅ Improved |
| Rate Limiting | None | Yes | ✅ New |
| Transaction Safety | None | Critical paths | ✅ New |
| Audit Logging | None | Critical ops | ✅ New |
| **Security Score** | **3/10** | **8/10** | **✅ +5 points** |

---

## 🧪 **Testing Checklist**

After each task:

**Form Requests:**
- [ ] Try submitting form without required fields → Should show validation errors
- [ ] Try invalid ClientId → Should show "client does not exist"
- [ ] Try duplicate QuotationNo → Should show uniqueness error

**Dynamic Fields:**
- [ ] Try injecting invalid CategoryId → Should be sanitized/rejected
- [ ] Try negative numbers → Should be rejected
- [ ] Try non-existent IDs → Should be rejected

**CSRF:**
- [ ] Try POST without token → Should get 419 error
- [ ] Normal form submit → Should work
- [ ] AJAX calls → Should work with token

**Rate Limiting:**
- [ ] Try 6 rapid logins → 6th should be blocked
- [ ] Wait 1 minute → Should work again

**Transactions:**
- [ ] Cause database error mid-update → Should rollback all changes
- [ ] Normal update → Should commit all changes

**Logging:**
- [ ] Check storage/logs/laravel.log
- [ ] Verify critical operations logged
- [ ] Verify log format readable

---

## 📚 **Documentation References**

Each task references specific documentation:

- **Form Requests:** 23_CONTROLLER_REFERENCE.md, 28_BUSINESS_RULES.md
- **Input Sanitization:** 36_SECURITY_GUIDE.md
- **CSRF:** 36_SECURITY_GUIDE.md
- **Transactions:** 05_DATA_FLOW.md
- **Logging:** 32_ADMIN_GUIDE.md (Monitoring section)

---

## 🎯 **Ready to Start?**

**I can provide:**
1. ✅ Exact code for each Form Request class
2. ✅ Exact controller modifications
3. ✅ Line-by-line changes with context
4. ✅ Test cases to verify
5. ✅ Commit messages

**Just say: "Start Task 1" and I'll give you:**
- Complete FormRequest class code (copy-paste ready)
- Controller modifications (exact search/replace)
- Testing instructions
- Commit command

---

## 📝 **Progress Tracking**

```markdown
## Security Hardening Phase 1 Progress

### Week 1
- [ ] Task 1: Form Request Classes (Day 1-2)
- [ ] Task 2: Dynamic Field Sanitization (Day 3)
- [ ] Task 3: CSRF Verification (Day 4)
- [ ] Task 4: Rate Limiting (Day 5)

### Week 2  
- [ ] Task 5: Transaction Wrapper (Day 1)
- [ ] Task 6: Audit Logging (Day 2)
- [ ] Testing & Review (Day 3-4)
- [ ] Merge to development (Day 5)

Current: Ready to start Task 1
```

---

**End of Security Hardening Phase 1 Plan**

**Branch:** sec/hardening-phase-1  
**Status:** Plan ready, awaiting execution  
**Next:** Execute tasks 1-6 in order

