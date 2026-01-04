# Test-1 PASS Checklist

Objective criteria to determine when Test-1 normalization is ready for promotion to FINAL.

## PASS Criteria (Must Meet All)

### 1. SKU Validity ✅
- [ ] No purely numeric `sku_code` (unless explicitly allowed in profile)
- [ ] `sku_code` matches expected pattern for the table (e.g., `LC1E*`, `LP1K*`, etc.)
- [ ] All SKUs contain at least one alphabet character
- [ ] No SKU codes shorter than 3 characters (likely junk)

**Evidence**: Check `invalid_sku_count` in summary JSON. Should be 0 or very low (< 1% of total rows).

---

### 2. Price Validity ✅
- [ ] `list_price` is numeric for ≥ 99% of output rows
- [ ] No obvious noise prices (e.g., `1.0`, `2.0`, `10600.118` unless verified as correct)
- [ ] Prices are reasonable for the product category

**Evidence**: Review first 20 lines of output CSV. All prices should be realistic.

---

### 3. Series Coverage ✅
- [ ] `series` is populated for ≥ 95% of output rows
- [ ] Remaining rows must have series inferred by SKU prefix (fallback)
- [ ] Series names are meaningful (not generic like "Item" or empty)

**Evidence**: Check `series_coverage` in summary JSON:
- `rows_with_series` / `rows_output` ≥ 0.95

---

### 4. Row Cleanliness ✅
- [ ] Zero header/footer/notes lines appear as SKU rows
- [ ] No explanatory text rows (e.g., "See page X", "Terms apply")
- [ ] Duplicates are either:
  - Skipped with a `duplicates_skipped` count, OR
  - Merged/upserted consistently (decide once per profile)

**Evidence**: 
- Review error Excel file - should be mostly empty after tuning
- Check `rows_dropped` count - should be reasonable (headers/notes)

---

### 5. Reproducibility ✅
- [ ] Running the same input file twice produces:
  - Same output row count
  - Same `(make, sku_code)` keys
  - Same prices (no floating-point drift)

**Evidence**: Run normalization twice, compare summary JSON counts.

---

## Evidence to Store

After Test-1 passes, archive these files:

1. **Summary JSON**: `logs/test/*summary.json`
   - Contains all counts and coverage metrics

2. **Error Excel**: `errors/test/*errors.xlsx`
   - Should be near-empty after tuning
   - Review to identify any remaining edge cases

3. **Output CSV Sample**: First 20 lines of `output/test/*.csv`
   - Quick visual verification
   - Verify column order and data quality

4. **Profile Used**: `profiles/{profile_name}.yml`
   - Lock this version (no edits without version bump)
   - Document any manual adjustments made

---

## Common Issues & Fixes

### Issue: Too many invalid SKUs
**Fix**: Adjust `ignore_if_contains_any` in profile to filter junk rows earlier.

### Issue: Low series coverage
**Fix**: 
- Add more `heading_patterns` to profile
- Add `sku_prefix_mappings` for common prefixes
- Check if heading detection is working (review error file)

### Issue: Duplicate SKUs
**Fix**: Decide on merge strategy:
- Keep first occurrence
- Keep latest occurrence
- Merge attributes (if applicable)

### Issue: Wrong column indexes
**Fix**: 
- Review error Excel to see raw collapsed cells
- Adjust `columns_by_index` in profile
- Re-run and verify

---

## Promotion Decision

When all 5 criteria are met:

1. ✅ Copy source XLSX to `input/final/` with `_FINAL_` in filename
2. ✅ Run normalizer with `--mode final`
3. ✅ Verify output CSV matches Test-1 output (same row count)
4. ✅ Lock profile version (rename to `{profile}_v1.yml` if needed)
5. ✅ Proceed to FastAPI import with `dry_run=true` first

---

## Notes

- Test-1 is **disposable** - feel free to experiment
- FINAL is **canonical** - treat as production artifact
- Any changes after FINAL require new FINAL file with new date

