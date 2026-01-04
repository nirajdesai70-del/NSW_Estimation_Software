# Next Execution Plan — Schneider Catalog Continuation

**Last Updated:** 2025-12-26  
**Target Family:** LP1K (TeSys K Control Relays)  
**Purpose:** Provide exact, step-by-step commands to continue Schneider catalog completion.

---

## 1. Preparation (One-Time Setup)

### 1.1 Verify Current State
```bash
# Confirm API is running on port 8011
curl http://localhost:8011/openapi.json | jq '.paths | keys | .[] | select(contains("catalog"))'

# Verify LC1E data exists
curl http://localhost:8011/api/v1/catalog/items | jq '.items | length'
# Should return: 1
```

### 1.2 Confirm Folder Structure
```bash
# Verify canonical structure exists
ls -la tools/catalog_pipeline/
# Should show: input/, profiles/, output/, errors/, logs/, normalize.py, README.md
```

---

## 2. Step-by-Step Execution Plan

### Step 1: Create LP1K WORK File
**Action:** Copy template and customize

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
cp docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/SCHNEIDER_<FAMILY>_WORK.md \
   docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/SCHNEIDER_LP1K_WORK.md
```

**Manual Edit Required:**
- Replace `<FAMILY>` with `LP1K`
- Fill in family name: "TeSys K Control Relays"
- Set status to "⚙ In Progress"
- Update source file paths

**Expected Output:** WORK file ready for execution notes

---

### Step 2: Create LP1K Profile (v1)
**Action:** Derive profile from LC1E template

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
cp tools/catalog_pipeline/profiles/schneider/schneider_lc1e_v1.yml \
   tools/catalog_pipeline/profiles/schneider/schneider_lp1k_v1.yml
```

**Manual Edit Required:**
- Update scope filter:
  ```yaml
  scope:
    include_series_contains_any:
      - "TeSys K Control Relays"
  ```
- Adjust series detection patterns if needed
- Verify column mappings (should be same as LC1E)

**Expected Output:** `schneider_lp1k_v1.yml` ready for TEST

---

### Step 3: Prepare TEST Input
**Action:** Copy source XLSX to TEST location

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
mkdir -p tools/catalog_pipeline/input/test/schneider/lp1k
cp "tools/catalog_pipeline/input/raw/schneider/master/Switching _Pricelist_WEF 15th Jul 25.xlsx" \
   "tools/catalog_pipeline/input/test/schneider/lp1k/Schneider_LP1K_TEST1.xlsx"
```

**Expected Output:** TEST XLSX ready for normalization

---

### Step 4: Run TEST Normalization (Iterate Until PASS)
**Action:** Run normalizer in TEST mode

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software/tools/catalog_pipeline
python normalize.py \
  --profile profiles/schneider/schneider_lp1k_v1.yml \
  --file input/test/schneider/lp1k/Schneider_LP1K_TEST1.xlsx \
  --mode test
```

**Check Output:**
- Review `output/test/` CSV
- Review `errors/test/` for issues
- Review `logs/test/` summary JSON

**PASS Criteria:**
- ✅ SKU validity: invalid SKUs < 1% of candidate rows
- ✅ Prices: 99%+ numeric, no obvious noise
- ✅ Series coverage: 95%+ (or profile-defined)
- ✅ Scope filter confirms LP1K-only output (no bleed)

**If FAIL:** Adjust profile and repeat Step 4.

**Expected Output:** Clean TEST CSV with LP1K SKUs only

---

### Step 5: Freeze FINAL Source
**Action:** Copy TEST XLSX to FINAL location with proper naming

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
mkdir -p tools/catalog_pipeline/input/final/schneider/lp1k
cp tools/catalog_pipeline/input/test/schneider/lp1k/Schneider_LP1K_TEST1.xlsx \
   tools/catalog_pipeline/input/final/schneider/lp1k/Schneider_LP1K_FINAL_$(date +%Y-%m-%d).xlsx
```

**Expected Output:** FINAL XLSX frozen with date stamp

---

### Step 6: Run FINAL Normalization
**Action:** Generate FINAL CSV

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software/tools/catalog_pipeline
python normalize.py \
  --profile profiles/schneider/schneider_lp1k_v1.yml \
  --file input/final/schneider/lp1k/Schneider_LP1K_FINAL_$(date +%Y-%m-%d).xlsx \
  --mode final
```

**Check Output:**
- FINAL CSV in `output/final/`
- Error file should be minimal
- Summary JSON confirms expected SKU count

**Expected Output:** FINAL CSV ready for import

---

### Step 7: Dry-Run Import (Mandatory)
**Action:** Validate FINAL CSV before commit

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
FINAL_CSV=$(ls -t tools/catalog_pipeline/output/final/*LP1K*normalized*.csv | head -1)

curl -X POST \
  "http://localhost:8011/api/v1/catalog/skus/import?dry_run=true" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@${FINAL_CSV}"
```

**Check Response:**
- `rows_error` must be `0`
- Review any error samples if present
- Confirm expected SKU count matches

**If ERRORS:** Fix profile or source, regenerate FINAL CSV, repeat Step 7.

**Expected Output:** Dry-run passes with 0 errors

---

### Step 8: Commit Import
**Action:** Import FINAL CSV into database

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
FINAL_CSV=$(ls -t tools/catalog_pipeline/output/final/*LP1K*normalized*.csv | head -1)

curl -X POST \
  "http://localhost:8011/api/v1/catalog/skus/import?dry_run=false" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@${FINAL_CSV}"
```

**Check Response:**
- `items_created` or `items_updated`
- `skus_created` or `skus_updated`
- `prices_inserted`
- `batch_id` (save this for audit)

**Expected Output:** Import successful, batch_id returned

---

### Step 9: Verify Import
**Action:** Confirm data in database

```bash
# Check items
curl http://localhost:8011/api/v1/catalog/items | jq '.items[] | select(.make == "Schneider")'

# Check SKUs
curl "http://localhost:8011/api/v1/catalog/skus?make=Schneider&limit=50" | jq '.total'

# Check specific SKU (if known)
curl http://localhost:8011/api/v1/catalog/skus/<sku_id> | jq '.current_price'
```

**Expected Output:** LP1K data visible in API responses

---

### Step 10: Update Documentation
**Action:** Mark LP1K as complete

**Update Files:**
1. `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER_CATALOG_MASTER.md`
   - Mark LP1K row as ✅ Complete
   - Add FINAL CSV path
   - Add SKU count
   - Add import date

2. `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/SCHNEIDER_LP1K_WORK.md`
   - Mark status as ✅ Complete
   - Fill in import batch_id
   - Document any exceptions

**Expected Output:** Documentation reflects LP1K completion

---

## 3. Definition of "DONE" for LP1K

LP1K is considered **complete** when:

- ✅ Profile `schneider_lp1k_v1.yml` created and frozen
- ✅ FINAL XLSX frozen with date stamp
- ✅ FINAL CSV generated successfully
- ✅ Dry-run import passes (0 errors)
- ✅ Commit import successful
- ✅ Data visible in API endpoints
- ✅ Documentation updated
- ✅ No pending issues

---

## 4. Expected Results

### 4.1 Database Counts (After LP1K)
- **CatalogItems:** 2 (LC1E + LP1K)
- **CatalogSKUs:** 23 + N (where N = LP1K SKU count)
- **SkuPrices:** 23 + N (archive rows)

### 4.2 API Verification
- `GET /api/v1/catalog/items` returns 2 items
- `GET /api/v1/catalog/skus?make=Schneider` returns all SKUs
- Each SKU has valid `current_price`

---

## 5. Troubleshooting

### Issue: TEST normalization finds no SKUs
**Solution:**
- Check scope filter in profile
- Verify series detection patterns
- Check column mappings match source structure

### Issue: Dry-run returns errors
**Solution:**
- Review error samples in response
- Fix profile or source data
- Regenerate FINAL CSV

### Issue: Import fails
**Solution:**
- Ensure dry-run passed first
- Check database connection
- Review API logs

---

## 6. Next Family After LP1K

After LP1K is complete, repeat this plan for:
- **LC1D** (TeSys Deca Power Contactors)

---

**Ready to Execute:** ✅  
**All prerequisites met. Begin with Step 1.**

