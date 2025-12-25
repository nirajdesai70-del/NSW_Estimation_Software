# Resolution-B Illegal Defaults

**File:** docs/RESOLUTION_B/RESOLUTION_B_ILLEGAL_DEFAULTS.md  
**Version:** v1.0_2025-12-19  
**Status:** 📋 INVENTORY (Analysis Phase, No Code Changes)  
**Source:** Live DB audit report + Code Evidence Pack

---

## Purpose

Identify all locations where illegal defaults are used that violate L2 (Specific Item) requirements:
- `MakeId => 0` defaults
- `SeriesId => 0` defaults
- `ProductId` reassignment without ProductType validation

---

## Summary

| Pattern | Count | Severity | Status |
|---------|-------|----------|--------|
| **MakeId => 0 defaults** | 38+ instances | HIGH | Requires fix |
| **SeriesId => 0 defaults** | 38+ instances | HIGH | Requires fix |
| **ProductId without ProductType check** | 13+ write paths | HIGH | Requires fix |
| **Raw DB inserts bypassing validation** | 2 locations | CRITICAL | Requires fix |

---

## 1. MakeId => 0 Defaults

### Pattern Description
Code uses patterns like:
```php
'MakeId' => $request->makeId ?? 0
// or
'MakeId' => 0
// or
$makeId = $makeId ?: 0; // Silent default
```

### Why Dangerous
- Violates L2 requirement: MakeId must be > 0 for ProductType=2 items
- Allows invalid state to persist (MakeId=0 with ProductType=2)
- Silent failures mask validation issues
- Downstream logic (pricing, costing, export) may fail or produce incorrect results

### Which Rule It Violates
- `RESOLUTION_B_RULES.md:§1.3` — MakeId > 0 required for L2 items
- `RESOLUTION_B_RULES.md:§8` — Validation failure handling (no silent defaults)

### Locations Found

#### QuotationV2Controller.php (10+ instances)
- **Lines:** 909, 1124, 1196, 1360, 1633, 1793, 1835, 1877, 3223 (and others)
- **Context:** Various create operations
- **Pattern:** `MakeId => $request->makeId ?? 0` or similar
- **Evidence:** Live DB audit report (2025-12-19)

#### QuotationController.php (6+ instances)
- **Lines:** 525, 863, 1075 (and others)
- **Context:** Various create operations
- **Pattern:** `MakeId => $request->makeId ?? 0` or similar
- **Evidence:** Live DB audit report (2025-12-19)

#### applyMasterBom() — QuotationV2Controller.php
- **Line:** ~1027
- **Method:** `applyMasterBom()`
- **Context:** Copy from Master BOM
- **Pattern:** Sets `MakeId => 0` explicitly
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Why:** Copy operation sets MakeId=0 as intermediate state, but no validation ensures resolution before finalization

#### applyFeederTemplate() — QuotationV2Controller.php
- **Line:** ~3114
- **Method:** `applyFeederTemplate()`
- **Context:** Copy from Feeder template
- **Pattern:** Sets `MakeId => 0` explicitly or defaults
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Why:** Same as applyMasterBom() — intermediate state may persist

#### Import Commands (Multiple instances)
- **Files:** ImportBomJson.php, ImportProposalBoms.php, ImportLegacyOffers.php
- **Context:** Import operations
- **Pattern:** `MakeId => 0` or `MakeId => $data['makeId'] ?? 0`
- **Evidence:** Live DB audit report (2025-12-19)
- **Why:** Import may not enforce MakeId requirement

---

## 2. SeriesId => 0 Defaults

### Pattern Description
Code uses patterns like:
```php
'SeriesId' => $request->seriesId ?? 0
// or
'SeriesId' => 0
// or
$seriesId = $seriesId ?: 0; // Silent default
```

### Why Dangerous
- Violates L2 requirement: SeriesId must be > 0 for ProductType=2 items (unless explicitly exempted)
- Allows invalid state to persist (SeriesId=0 with ProductType=2)
- Silent failures mask validation issues
- Downstream logic (pricing, costing, export) may fail or produce incorrect results

### Which Rule It Violates
- `RESOLUTION_B_RULES.md:§1.4` — SeriesId > 0 required for L2 items (unless exempted)
- `RESOLUTION_B_RULES.md:§8` — Validation failure handling (no silent defaults)

### Locations Found

#### QuotationV2Controller.php (10+ instances)
- **Lines:** 909, 1124, 1196, 1360, 1633, 1793, 1835, 1877, 3223 (and others)
- **Context:** Various create operations
- **Pattern:** `SeriesId => $request->seriesId ?? 0` or similar
- **Evidence:** Live DB audit report (2025-12-19)

#### QuotationController.php (6+ instances)
- **Lines:** 525, 863, 1075 (and others)
- **Context:** Various create operations
- **Pattern:** `SeriesId => $request->seriesId ?? 0` or similar
- **Evidence:** Live DB audit report (2025-12-19)

#### applyMasterBom() — QuotationV2Controller.php
- **Line:** ~1027
- **Method:** `applyMasterBom()`
- **Context:** Copy from Master BOM
- **Pattern:** Sets `SeriesId => 0` explicitly
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Why:** Copy operation sets SeriesId=0 as intermediate state, but no validation ensures resolution before finalization

#### applyFeederTemplate() — QuotationV2Controller.php
- **Line:** ~3114
- **Method:** `applyFeederTemplate()`
- **Context:** Copy from Feeder template
- **Pattern:** Sets `SeriesId => 0` explicitly or defaults
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Why:** Same as applyMasterBom() — intermediate state may persist

#### addItem() — QuotationV2Controller.php
- **Method:** `addItem()`
- **Context:** Manual item addition
- **Pattern:** `SeriesId => 0` or defaults to 0
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-02`
- **Why:** Manual add allows SeriesId to default to 0 without validation

#### Import Commands (Multiple instances)
- **Files:** ImportBomJson.php, ImportProposalBoms.php, ImportLegacyOffers.php
- **Context:** Import operations
- **Pattern:** `SeriesId => 0` or `SeriesId => $data['seriesId'] ?? 0`
- **Evidence:** Live DB audit report (2025-12-19)
- **Why:** Import may not enforce SeriesId requirement

---

## 3. ProductId Reassignment Without ProductType Check

### Pattern Description
Code assigns ProductId without validating ProductType:
```php
QuotationSaleBomItem::create([
    'ProductId' => $masterBomItem->ProductId, // Generic product (ProductType=1)
    // No check that ProductType=2 is required
]);
```

### Why Dangerous
- Allows Generic products (ProductType=1) to persist in Proposal BOM
- Violates L2 requirement: Proposal BOM must use Specific products (ProductType=2)
- Breaks data integrity: Generic products cannot have Make/Series
- Downstream logic expects Specific products and may fail

### Which Rule It Violates
- `RESOLUTION_B_RULES.md:§1.1` — ProductType = 2 required for L2 items
- `RESOLUTION_B_RULES.md:§3` — Proposal BOM is ALWAYS L2 at final state

### Locations Found

#### applyMasterBom() — QuotationV2Controller.php
- **Line:** ~1027
- **Method:** `applyMasterBom()`
- **Context:** Copy from Master BOM
- **Pattern:** 
  ```php
  QuotationSaleBomItem::create([
      'ProductId' => $masterBomItem->ProductId, // Generic product copied directly
      'MakeId' => 0,
      'SeriesId' => 0,
      // No ProductType validation
  ]);
  ```
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Why:** Copy operation copies Generic ProductId directly without conversion to Specific

#### applyFeederTemplate() — QuotationV2Controller.php
- **Line:** ~3114
- **Method:** `applyFeederTemplate()`
- **Context:** Copy from Feeder template
- **Pattern:** Copies ProductId from template items without enforcing ProductType=2
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`
- **Why:** Same as applyMasterBom() — no ProductType validation

#### addItem() — QuotationV2Controller.php
- **Method:** `addItem()`
- **Context:** Manual item addition
- **Pattern:** Validates product exists but does not enforce ProductType=2
- **Evidence:** `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-02`
- **Why:** Manual add allows Generic products to be added

#### All Create Paths (13+ locations)
- **Files:** QuotationV2Controller.php, QuotationController.php, Import commands
- **Context:** All create operations
- **Pattern:** ProductId assigned without ProductType validation
- **Evidence:** Live DB audit report (2025-12-19)
- **Why:** No centralized validation enforces ProductType=2 requirement

---

## 4. Raw DB Inserts Bypassing Validation

### Pattern Description
Code uses direct DB inserts:
```php
DB::table('quotation_sale_bom_items')->insert([
    'ProductId' => $productId,
    'MakeId' => 0,
    'SeriesId' => 0,
    // Bypasses ALL validation
]);
```

### Why Dangerous
- Bypasses ALL application validation (Eloquent model, business rules, guards)
- Allows ANY invalid state to be persisted (ProductType=1, MakeId=0, SeriesId=0, etc.)
- No audit trail (Eloquent events, logging, etc.)
- Creates data integrity risks
- Harder to trace and debug

### Which Rule It Violates
- `RESOLUTION_B_RULES.md:§4` — Raw DB inserts are FORBIDDEN
- All L2 requirements (ProductType=2, MakeId>0, SeriesId>0)

### Locations Found

#### ImportProposalBoms.php
- **Line:** 282
- **Method:** Import command execution
- **Operation:** `DB::table('quotation_sale_bom_items')->insert()`
- **Evidence:** Live DB audit report (2025-12-19)
- **Severity:** CRITICAL
- **Why:** Raw insert bypasses all validation, likely inserts invalid states

#### ImportLegacyOffers.php
- **Line:** 371
- **Method:** Import command execution
- **Operation:** `DB::table('quotation_sale_bom_items')->insert()`
- **Evidence:** Live DB audit report (2025-12-19)
- **Severity:** CRITICAL
- **Why:** Raw insert bypasses all validation, likely inserts invalid states

---

## 5. Silent Default Pattern Examples

### Forbidden Pattern 1: Null Coalescing to Zero
```php
// FORBIDDEN
QuotationSaleBomItem::create([
    'ProductId' => $productId,
    'MakeId' => $request->makeId ?? 0,  // NO - silent default
    'SeriesId' => $request->seriesId ?? 0, // NO - silent default
]);
```

### Forbidden Pattern 2: Ternary to Zero
```php
// FORBIDDEN
$makeId = $makeId ?: 0;  // NO - silent default
$seriesId = $seriesId ?: 0; // NO - silent default
```

### Forbidden Pattern 3: Direct Zero Assignment
```php
// FORBIDDEN (unless transitional state with explicit flag)
QuotationSaleBomItem::create([
    'ProductId' => $masterBomItem->ProductId,
    'MakeId' => 0,  // NO - violates L2 requirement
    'SeriesId' => 0, // NO - violates L2 requirement
    // Missing: explicit "pending resolution" flag
]);
```

### Required Pattern: Explicit Validation
```php
// REQUIRED
if (!$makeId || $makeId <= 0) {
    throw new ValidationException("MakeId is required and must be > 0 for Proposal BOM items");
}
if (!$seriesId || $seriesId <= 0) {
    throw new ValidationException("SeriesId is required and must be > 0 for Proposal BOM items");
}
QuotationSaleBomItem::create([
    'ProductId' => $productId,
    'MakeId' => $makeId,
    'SeriesId' => $seriesId,
]);
```

---

## Phase-4 Fix Requirements

1. **Remove All MakeId => 0 Defaults**
   - Replace with explicit validation
   - Throw exception if MakeId is missing or <= 0 (for ProductType=2)

2. **Remove All SeriesId => 0 Defaults**
   - Replace with explicit validation
   - Throw exception if SeriesId is missing or <= 0 (for ProductType=2, unless exempted)

3. **Add ProductType Validation**
   - All write paths must validate ProductType=2
   - Exception: Transitional state (must be explicitly flagged and resolved before finalization)

4. **Convert Raw DB Inserts**
   - Replace `DB::table('quotation_sale_bom_items')->insert()` with Eloquent model or centralized write gateway
   - All validation rules must be enforced

5. **Centralize Validation**
   - Move validation to centralized write gateway
   - Ensure all write paths use gateway

---

## References

- `RESOLUTION_B_RULES.md` — L2 write enforcement rules
- `RESOLUTION_B_WRITE_PATHS.md` — Complete write path inventory
- `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md` — Code evidence findings
- Live DB audit report (2025-12-19) — Default patterns and locations

