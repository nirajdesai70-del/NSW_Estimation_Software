# NSW Master Data Creation & Import Governance

**Version:** 1.0  
**Date:** 2025-12-18  
**Status:** FROZEN - Authoritative Policy  
**Purpose:** Define enforceable rules for master data creation and import to prevent legacy semantic contamination  
**Integration:** This document is part of Phase 5 Step-1 (NSW Data Dictionary v1.0)

---

## 🎯 Executive Summary

This governance document establishes the **firewall rules** that prevent legacy interpretation patterns from contaminating NSW canonical structure. It defines:

1. **No Auto-Create Masters Rule** - Prevents accidental category/subcategory/item explosion
2. **Import Approval Queue Policy** - Requires human review for unknown master references
3. **Canonical Resolver Rules** - Defines how imports must match canonical entities

**Critical Principle:** NSW canonical meaning is the only truth. No controller, import, or API endpoint may create Category/Subcategory/Item/Product/Attribute on-the-fly during runtime operations.

### Non-Goals

This policy explicitly does **not** attempt to:
- **Fix legacy data** - Legacy data remains as read-only archive; this policy prevents new mistakes
- **Infer or guess business meaning** - Unknown masters are queued for human approval, not auto-interpreted
- **Guarantee import success** - Imports may fail if masters are missing; this policy guarantees semantic correctness, not convenience

This policy is **schema-enforced, not config-enforced** - The rules are primarily enforced through database constraints and exception handling, not configuration flags. The system cannot be misused accidentally.

---

## 🚫 Rule 1: No Auto-Create Masters (Hard Constraint)

### 1.1 Core Prohibition

**Rule:** No controller, service, import handler, or API endpoint may create master data entities (Category, Subcategory, Type/Item, Attribute, Product, Make, Series) during runtime operations.

**Forbidden Patterns (Legacy Anti-Patterns):**

```php
// ❌ FORBIDDEN: Auto-create during import
$category = Category::firstOrCreate(['Name' => $row['category']]);

// ❌ FORBIDDEN: Auto-create during controller action
if (!$category) {
    $category = Category::create(['Name' => $name]);
}

// ❌ FORBIDDEN: Auto-create in service layer
$item = Item::firstOrCreate([
    'Name' => $itemName,
    'CategoryId' => $categoryId
]);
```

**Why This Rule Exists:**

Evidence from legacy `ImportController` shows patterns like:
- `Category::firstOrCreate(['Name' => $row['category']])` (line 231)
- `SubCategory::firstOrCreate([...])` (line 240)
- `Item::firstOrCreate([...])` (line 253)
- `Product::firstOrCreate([...])` (line 307)
- `Attribute::create([...])` (line 123)

These patterns cause:
- **Category explosion** - Duplicate categories with slight name variations
- **Semantic drift** - Same meaning stored as different entities
- **Data quality degradation** - No validation of business meaning
- **Canonical structure contamination** - Legacy interpretation becomes permanent

### 1.2 Allowed Master Creation Pathways

**Pathway 1: UI-Only Master Creation Forms**
- **Owner:** MASTER module
- **Access:** Authorized users only (role-based)
- **Validation:** Full business rule validation before creation
- **Audit:** All master creations logged (who/when/why)
- **Examples:**
  - Category creation form (validates uniqueness, naming conventions)
  - Subcategory creation form (validates parent category exists)
  - Item creation form (validates category/subcategory hierarchy)

**Pathway 2: Controlled Import Pipeline (Approved Masters Only)**
- **Owner:** CIM module (with MASTER approval gate)
- **Access:** Import files that reference **pre-approved** master entities only
- **Validation:** Import validator checks all master references exist before processing
- **Rejection:** Import fails if any master reference is unknown
- **Queue:** Unknown masters go to approval queue (see Rule 2)

**Pathway 3: API Endpoints (Admin-Only, Explicit)**
- **Owner:** MASTER module
- **Access:** Admin-only endpoints (separate from runtime operations)
- **Validation:** Full business rule validation
- **Audit:** All API master creations logged
- **Examples:**
  - `POST /api/master/categories` (admin-only)
  - `POST /api/master/items` (admin-only)

### 1.3 Enforcement Mechanism

**Database Constraints:**
- NSW schema must enforce referential integrity (FKs cannot be 0)
- Unique constraints on canonical keys (e.g., `Category.Name` + business rules)
- Check constraints preventing "0" foreign keys where NULL is required

**Code-Level Enforcement:**
- No `firstOrCreate` patterns in import handlers
- No `create` patterns in runtime controllers (except MASTER-owned forms)
- Import validators must reject unknown master references
- Service layer must throw exceptions if master lookup fails

**Code Review Checklist:**
- [ ] No `Category::firstOrCreate` or `Category::create` in import/controller code
- [ ] No `SubCategory::firstOrCreate` or `SubCategory::create` in import/controller code
- [ ] No `Item::firstOrCreate` or `Item::create` in import/controller code
- [ ] No `Product::firstOrCreate` or `Product::create` in import/controller code
- [ ] No `Attribute::create` in import/controller code
- [ ] All master lookups use `find` or `where()->first()` (not `firstOrCreate`)
- [ ] All master lookups handle "not found" by rejecting or queuing (not creating)

---

## 📋 Rule 2: Import Approval Queue Policy

### 2.1 Core Requirement

**Rule:** If an import file references a master entity (Category/Subcategory/Item/Product/Make/Series/Attribute) that does not exist in canonical tables, the import must:

1. **Reject the row** (do not process)
2. **Log the rejection** to `IMPORT_REJECT_LIST`
3. **Queue the unknown master** to `IMPORT_PENDING_MASTER_APPROVAL_QUEUE`
4. **Continue processing** other rows (if any)
5. **Return summary** showing: processed count, rejected count, pending masters list

**No Silent Creation:** The system must never create masters automatically, even if "it seems obvious."

### 2.2 Import Processing Flow

```
Import File Upload
    │
    ├─> Parse File (validate format)
    │
    ├─> Pre-Validation Phase
    │   ├─> Extract all master references (Category, Subcategory, Item, etc.)
    │   ├─> Check each reference against canonical tables
    │   └─> Build PENDING_MASTERS list
    │
    ├─> Decision Point
    │   ├─> If PENDING_MASTERS is empty → Proceed to processing
    │   └─> If PENDING_MASTERS is not empty → Queue for approval, return summary
    │
    ├─> Row Processing Phase (only if all masters exist)
    │   ├─> For each row:
    │   │   ├─> Lookup Category (must exist, throw if not)
    │   │   ├─> Lookup Subcategory (must exist or NULL, throw if invalid)
    │   │   ├─> Lookup Item (must exist or NULL, throw if invalid)
    │   │   └─> Process row (create product, price, etc.)
    │   └─> Log to IMPORT_RUN_LOG
    │
    └─> Return Summary
        ├─> Processed: N rows
        ├─> Rejected: M rows (with reasons)
        └─> Pending Masters: [list of unknown masters requiring approval]
```

### 2.3 Pending Master Approval Queue Structure

**Table:** `import_pending_master_approval_queue`

**Columns:**
- `QueueId` (PK)
- `ImportRunId` (FK to import_run_log)
- `MasterType` (enum: Category, Subcategory, Item, Product, Make, Series, Attribute)
- `MasterName` (the name from import file)
- `Context` (JSON: parent category, row number, import file name, etc.)
- `SuggestedCanonicalMatch` (nullable: if system found a similar existing master)
- `Status` (enum: Pending, Approved, Rejected, Merged)
- `ApprovedBy` (nullable: user who approved)
- `ApprovedAt` (nullable: timestamp)
- `CreatedAt` (timestamp)
- `ResolvedMasterId` (nullable: FK to resolved master table)

**Workflow:**
1. Import creates queue entries for unknown masters
2. Admin reviews queue (UI: `/admin/import-queue`)
3. Admin decides:
   - **Approve as new master** → Creates master via MASTER module form (audited)
   - **Map to existing master** → Links to existing canonical entity
   - **Reject** → Marks as rejected, import row remains rejected
4. After approval, import can be re-run (or auto-retried if configured)

### 2.4 Import Decision Logging

**Table:** `import_decision_log`

**Purpose:** Audit trail of all import decisions (accept/reject/queue)

**Columns:**
- `DecisionId` (PK)
- `ImportRunId` (FK)
- `RowNumber` (row in import file)
- `Decision` (enum: Accepted, Rejected, Queued)
- `Reason` (text: why accepted/rejected/queued)
- `MasterReferences` (JSON: list of masters referenced in this row)
- `CreatedAt` (timestamp)

**Usage:**
- Every row processed logs a decision
- Rejected rows include rejection reason
- Queued rows include pending masters list
- Accepted rows include canonical master IDs used

### 2.5 Import Run Log

**Table:** `import_run_log`

**Purpose:** High-level summary of each import execution

**Columns:**
- `ImportRunId` (PK)
- `ImportType` (enum: Product, Price, BOM, etc.)
- `FileName` (original file name)
- `FileHash` (for duplicate detection)
- `Status` (enum: Pending, Processing, Completed, Failed, PartiallyCompleted)
- `TotalRows` (count from file)
- `ProcessedRows` (successfully processed)
- `RejectedRows` (rejected count)
- `QueuedMasters` (count of pending masters)
- `StartedAt` (timestamp)
- `CompletedAt` (nullable: timestamp)
- `StartedBy` (user who initiated)
- `ErrorSummary` (nullable: JSON of errors)

---

## 🔍 Rule 3: Canonical Resolver Rules

### 3.1 Master Entity Lookup Rules

**Rule:** All master entity lookups must use **canonical keys** (not fuzzy matching, not "create if missing").

**Canonical Keys Defined:**

| Master Entity | Canonical Key | Additional Context |
|---------------|---------------|-------------------|
| Category | `Name` (case-insensitive, trimmed) | Must be unique |
| Subcategory | `Name` + `CategoryId` | Must be unique within category |
| Item | `Name` + `CategoryId` | Must be unique within category |
| Product (Generic) | `Name` + `CategoryId` + `ProductType=1` | Must be unique |
| Product (Specific) | `SKU` (if present) OR `Name` + `CategoryId` + `MakeId` + `SeriesId` + `ProductType=2` | SKU preferred |
| Make | `Name` (case-insensitive, trimmed) | Must be unique |
| Series | `Name` + `MakeId` | Must be unique within make |
| Attribute | `Name` (case-insensitive, trimmed) | Must be unique |

### 3.2 Lookup Implementation Pattern

**Required Pattern (NSW Standard):**

```php
// ✅ CORRECT: Lookup with explicit "not found" handling
$category = Category::where('Name', trim($categoryName))
    ->where('Status', 0) // Active only
    ->first();

if (!$category) {
    // Reject or queue - DO NOT CREATE
    throw new CanonicalMasterNotFoundException(
        "Category '{$categoryName}' not found in canonical tables. " .
        "Import row rejected. Master queued for approval."
    );
}

// Use $category->CategoryId for FK
```

**Forbidden Patterns:**

```php
// ❌ FORBIDDEN: Auto-create on lookup failure
$category = Category::firstOrCreate(['Name' => $name]);

// ❌ FORBIDDEN: Fuzzy matching with auto-create
$category = Category::where('Name', 'LIKE', "%{$name}%")->first();
if (!$category) {
    $category = Category::create(['Name' => $name]);
}

// ❌ FORBIDDEN: Default to "0" or NULL without validation
$categoryId = $category ? $category->CategoryId : 0; // If 0 is invalid, this is wrong
```

### 3.3 Normalization Rules

**Input Normalization (Before Lookup):**

1. **Trim whitespace** - `trim($input)`
2. **Case normalization** - Store as provided, lookup case-insensitive
3. **Empty string handling** - Empty strings become NULL (not "0")
4. **Special character handling** - Preserve as-is (no auto-correction)

**Example Normalization:**

```php
$categoryName = trim($row['category']);
if (empty($categoryName)) {
    throw new ValidationException("Category name cannot be empty");
}

$category = Category::whereRaw('LOWER(Name) = LOWER(?)', [$categoryName])
    ->where('Status', 0)
    ->first();
```

### 3.4 Ambiguity Resolution

**Rule:** If a lookup could match multiple canonical entities (should not happen if unique constraints are enforced), the system must:

1. **Reject the row** (do not guess)
2. **Log ambiguity** to `IMPORT_DECISION_LOG`
3. **Queue for human resolution** (admin must choose correct match)

**Example Ambiguity Scenario:**

```php
// If somehow two categories exist with same name (data quality issue)
$categories = Category::where('Name', $name)->get();
if ($categories->count() > 1) {
    throw new CanonicalAmbiguityException(
        "Multiple categories found with name '{$name}'. " .
        "Data quality issue. Row rejected. Requires admin resolution."
    );
}
```

**Prevention:** Database unique constraints must prevent this scenario.

### 3.5 Suggested Match (Optional Helper)

**Rule:** When a master lookup fails, the system may suggest a similar existing master (fuzzy match), but **must not auto-select it**.

**Implementation:**

```php
$category = Category::where('Name', $categoryName)->first();

if (!$category) {
    // Optional: Find similar (for UI suggestion only)
    $suggested = Category::where('Name', 'LIKE', "%{$categoryName}%")
        ->where('Status', 0)
        ->first();
    
    // Queue with suggestion (admin decides)
    ImportPendingMasterQueue::create([
        'MasterType' => 'Category',
        'MasterName' => $categoryName,
        'SuggestedCanonicalMatch' => $suggested ? $suggested->CategoryId : null,
        'Status' => 'Pending'
    ]);
    
    throw new CanonicalMasterNotFoundException("Category not found");
}
```

**UI Display:** Admin sees suggested match in approval queue, but must explicitly approve or map manually.

---

## 📊 Rule 4: Import Validation Pipeline

### 4.1 Pre-Import Validation (Gate-0)

**Rule:** Before processing any import rows, validate all master references exist.

**Validation Steps:**

1. **Extract all master references** from import file
2. **Deduplicate** master references (same master may appear in multiple rows)
3. **Lookup each master** in canonical tables
4. **Build missing masters list**
5. **Decision:**
   - If missing masters exist → **Reject entire import**, return missing masters list
   - If all masters exist → **Proceed to row processing**

**Implementation Pattern:**

```php
class ImportValidator
{
    public function validateMasterReferences(array $rows): ValidationResult
    {
        $missingMasters = [];
        
        // Extract all unique master references
        $categoryNames = array_unique(array_column($rows, 'category'));
        $subcategoryNames = array_unique(array_column($rows, 'subcategory'));
        // ... etc
        
        // Validate each master exists
        foreach ($categoryNames as $name) {
            if (!Category::where('Name', $name)->where('Status', 0)->exists()) {
                $missingMasters[] = ['type' => 'Category', 'name' => $name];
            }
        }
        
        // Return validation result
        if (!empty($missingMasters)) {
            return ValidationResult::rejected($missingMasters);
        }
        
        return ValidationResult::approved();
    }
}
```

### 4.2 Row-Level Validation

**Rule:** Even if Gate-0 passes, each row must validate its master references before processing.

**Why:** Defensive programming - Gate-0 may miss edge cases, row-level validation catches them.

**Pattern:**

```php
foreach ($rows as $rowNumber => $row) {
    try {
        // Validate masters for this row
        $category = $this->resolveCategory($row['category']);
        $subcategory = $this->resolveSubcategory($row['subcategory'], $category);
        $item = $this->resolveItem($row['item'], $category);
        
        // Process row (create product, etc.)
        $this->processRow($row, $category, $subcategory, $item);
        
        // Log success
        ImportDecisionLog::create([
            'RowNumber' => $rowNumber,
            'Decision' => 'Accepted',
            'MasterReferences' => [
                'CategoryId' => $category->CategoryId,
                'SubCategoryId' => $subcategory?->SubCategoryId,
                'ItemId' => $item?->ItemId
            ]
        ]);
    } catch (CanonicalMasterNotFoundException $e) {
        // Log rejection
        ImportDecisionLog::create([
            'RowNumber' => $rowNumber,
            'Decision' => 'Rejected',
            'Reason' => $e->getMessage()
        ]);
        
        // Queue missing master
        ImportPendingMasterQueue::create([...]);
    }
}
```

---

## 🔐 Rule 5: Database Schema Enforcement

**Design Principle:** These rules are enforced primarily through schema constraints and exceptions, not configuration flags. The system cannot be misused accidentally - database constraints prevent invalid data at the lowest level.

### 5.1 Foreign Key Constraints

**Rule:** NSW schema must enforce referential integrity. Foreign keys cannot be "0" (use NULL instead).

**Schema Requirements:**

```sql
-- ✅ CORRECT: FK allows NULL (if optional)
CREATE TABLE products (
    ProductId INT PRIMARY KEY,
    CategoryId INT NOT NULL,  -- Required
    SubCategoryId INT NULL,   -- Optional (NULL, not 0)
    ItemId INT NULL,           -- Optional (NULL, not 0)
    FOREIGN KEY (CategoryId) REFERENCES categories(CategoryId),
    FOREIGN KEY (SubCategoryId) REFERENCES sub_categories(SubCategoryId),
    FOREIGN KEY (ItemId) REFERENCES items(ItemId)
);

-- ❌ FORBIDDEN: FK defaulting to 0
CREATE TABLE products (
    CategoryId INT DEFAULT 0,  -- WRONG: 0 is not a valid FK
    FOREIGN KEY (CategoryId) REFERENCES categories(CategoryId)  -- Will fail if 0 inserted
);
```

**Migration Pattern:**

```php
// ✅ CORRECT: Use NULL for optional FKs
$table->foreignId('SubCategoryId')->nullable()->constrained('sub_categories');

// ❌ FORBIDDEN: Default to 0
$table->foreignId('SubCategoryId')->default(0);  // Wrong
```

### 5.2 Unique Constraints

**Rule:** Canonical keys must have unique constraints to prevent duplicate "same meaning" rows.

**Required Unique Constraints:**

```sql
-- Categories: Name must be unique
ALTER TABLE categories ADD CONSTRAINT uk_categories_name UNIQUE (Name);

-- Subcategories: Name + CategoryId must be unique
ALTER TABLE sub_categories ADD CONSTRAINT uk_subcategories_name_category 
    UNIQUE (Name, CategoryId);

-- Items: Name + CategoryId must be unique
ALTER TABLE items ADD CONSTRAINT uk_items_name_category 
    UNIQUE (Name, CategoryId);

-- Products (Generic): Name + CategoryId + ProductType=1 must be unique
ALTER TABLE products ADD CONSTRAINT uk_products_generic 
    UNIQUE (Name, CategoryId) WHERE ProductType = 1;

-- Products (Specific): SKU must be unique (if present)
ALTER TABLE products ADD CONSTRAINT uk_products_sku 
    UNIQUE (SKU) WHERE SKU IS NOT NULL;
```

### 5.3 Check Constraints

**Rule:** Use check constraints to prevent invalid enum values and "0" foreign keys.

**Examples:**

```sql
-- Prevent ProductType invalid values
ALTER TABLE products ADD CONSTRAINT ck_products_producttype 
    CHECK (ProductType IN (1, 2));

-- Prevent Status invalid values
ALTER TABLE categories ADD CONSTRAINT ck_categories_status 
    CHECK (Status IN (0, 1));  -- 0=Active, 1=Inactive

-- Prevent 0 foreign keys (if column is NOT NULL)
-- Note: Use NULL for optional FKs instead
```

---

## 📝 Rule 6: Audit Trail Requirements

### 6.1 Master Creation Audit

**Rule:** All master entity creations must be audited (who/when/why).

**Audit Table:** `master_creation_audit`

**Columns:**
- `AuditId` (PK)
- `MasterType` (enum: Category, Subcategory, Item, etc.)
- `MasterId` (FK to created master)
- `MasterName` (name of created master)
- `CreatedBy` (user ID)
- `CreatedAt` (timestamp)
- `CreationSource` (enum: UI_Form, API_Admin, Import_Approved, System_Migration)
- `ApprovalQueueId` (nullable: FK to import_pending_master_approval_queue if from import)
- `Reason` (text: why created, business justification)

**Usage:**
- Every master creation logs to audit table
- Enables traceability: "Why does this category exist?"
- Enables cleanup: "Who created this duplicate?"

### 6.2 Import Run Audit

**Rule:** All import executions must be fully audited.

**Tables:**
- `import_run_log` (high-level summary)
- `import_decision_log` (row-level decisions)
- `import_pending_master_approval_queue` (pending masters)

**Audit Trail Query Example:**

```sql
-- Get full audit trail for an import run
SELECT 
    irl.ImportRunId,
    irl.FileName,
    irl.Status,
    irl.ProcessedRows,
    irl.RejectedRows,
    COUNT(idl.DecisionId) as TotalDecisions,
    COUNT(CASE WHEN idl.Decision = 'Rejected' THEN 1 END) as RejectedCount,
    COUNT(ipmaq.QueueId) as PendingMastersCount
FROM import_run_log irl
LEFT JOIN import_decision_log idl ON irl.ImportRunId = idl.ImportRunId
LEFT JOIN import_pending_master_approval_queue ipmaq ON irl.ImportRunId = ipmaq.ImportRunId
WHERE irl.ImportRunId = ?
GROUP BY irl.ImportRunId;
```

---

## 🎯 Rule 7: Exception Handling

### 7.1 Canonical Master Not Found Exception

**Rule:** Create a dedicated exception class for "master not found" scenarios.

**Implementation:**

```php
class CanonicalMasterNotFoundException extends \Exception
{
    public function __construct(
        string $masterType,
        string $masterName,
        ?string $context = null
    ) {
        $message = "Canonical master '{$masterType}' with name '{$masterName}' not found.";
        if ($context) {
            $message .= " Context: {$context}";
        }
        parent::__construct($message);
    }
}
```

**Usage:**

```php
$category = Category::where('Name', $name)->first();
if (!$category) {
    throw new CanonicalMasterNotFoundException(
        'Category',
        $name,
        "Import row #{$rowNumber}, file: {$fileName}"
    );
}
```

### 7.2 Canonical Ambiguity Exception

**Rule:** Create exception for ambiguous lookups (multiple matches).

**Implementation:**

```php
class CanonicalAmbiguityException extends \Exception
{
    public function __construct(
        string $masterType,
        string $masterName,
        array $matches
    ) {
        $matchIds = implode(', ', array_column($matches, 'id'));
        $message = "Ambiguous lookup: {$masterType} '{$masterName}' matched multiple records (IDs: {$matchIds}). Data quality issue.";
        parent::__construct($message);
    }
}
```

---

## ✅ Compliance Checklist

### For Import Handlers

- [ ] No `firstOrCreate` patterns for masters
- [ ] No `create` patterns for masters (except in MASTER module)
- [ ] All master lookups use `where()->first()` with explicit "not found" handling
- [ ] Unknown masters trigger exception → rejection → queue
- [ ] Pre-import validation (Gate-0) checks all masters exist
- [ ] Row-level validation validates masters before processing
- [ ] All decisions logged to `import_decision_log`
- [ ] Unknown masters queued to `import_pending_master_approval_queue`
- [ ] Import summary includes: processed, rejected, pending masters

### For Controllers

- [ ] No master creation in runtime controllers (except MASTER-owned forms)
- [ ] All master lookups throw exceptions if not found (no silent defaults)
- [ ] No "0" foreign keys (use NULL for optional)
- [ ] All master creations (if any) logged to audit table

### For Database Schema

- [ ] Foreign keys use NULL for optional (not 0)
- [ ] Unique constraints on canonical keys
- [ ] Check constraints prevent invalid enum values
- [ ] Referential integrity enforced (FKs cannot be invalid)

### For Service Layer

- [ ] Master resolution methods throw exceptions (no auto-create)
- [ ] All master lookups validate existence
- [ ] Ambiguity handling rejects (does not guess)

### Emergency Controls (Optional Safeguard)

**Kill-Switch for Imports:**

System admin may globally disable imports via configuration flag if abnormal master queue growth is detected. This provides an emergency brake if:
- Import volume exceeds review capacity
- Suspicious import patterns are detected
- Master queue grows beyond acceptable threshold

**Implementation:**
- Configuration flag: `imports.enabled` (default: true)
- Admin UI: Toggle import enable/disable
- When disabled: All import endpoints return `503 Service Unavailable` with message
- Audit log: All enable/disable toggles logged

**Note:** This is an optional safeguard for operational control, not a core governance rule.

---

## 📋 Integration with Phase 5 Step-1

This governance document is **integrated into** `NSW_DATA_DICTIONARY_v1.0.md` as:

**Section:** "Master Data Creation & Import Governance"  
**Location:** After entity definitions, before schema design  
**Purpose:** Lock these rules as part of canonical definition

**When Phase 5 Step-1 completes:**
- This document becomes part of the frozen Data Dictionary
- All NSW code must comply with these rules
- Code review checklist includes these rules
- Database schema must enforce these constraints

---

## 🔗 References

**Authority Documents:**
- `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md` - Scope separation decision
- `docs/PHASE_5/00_GOVERNANCE/PHASE_5_EXECUTION_SUMMARY.md` - Phase 5 overview
- `source_snapshot/app/Http/Controllers/ImportController.php` - Legacy anti-pattern evidence

**Related Governance:**
- Phase 4 S2 isolation boundaries
- NSW canonical structure definition (Phase 5 Step-1)
- NSW schema design (Phase 5 Step-2)

---

**Document Status:** FROZEN - Authoritative Policy  
**Last Updated:** 2025-12-18  
**Owner:** Phase 5 Governance Team  
**Next Review:** After Phase 5 Step-1 completion (Data Dictionary freeze)

