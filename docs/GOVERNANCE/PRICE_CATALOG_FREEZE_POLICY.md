# Price Catalog Freeze Policy

Governance rules for managing test vs. final price list imports.

## Purpose

Prevent accidental reuse of test data in production and maintain clear audit trail between learning/calibration runs and canonical catalog imports.

---

## Core Principle

**TEST = Disposable, FINAL = Frozen**

Any XLSX/CSV used during TEST mode is invalid for routine or repeat imports. Only files explicitly marked FINAL may be reused or re-imported.

---

## File Naming Rules

### TEST Files
- Must include `_TEST1_` or `_TEST_` in filename
- Example: `schneider_easy_tesys_contactors_TEST1.xlsx`
- Location: `tools/price_normalizer/input/test/`

### FINAL Files
- Must include `_FINAL_` + date in filename
- Example: `Schneider_EasyTeSys_Contactors_FINAL_2025-12-26.xlsx`
- Location: `tools/price_normalizer/input/final/`
- Date format: `YYYY-MM-DD` (ISO 8601)

---

## Folder Structure

```
tools/price_normalizer/
├── input/
│   ├── test/          # TEST files (disposable)
│   └── final/         # FINAL files (canonical)
├── output/
│   ├── test/          # TEST outputs (disposable)
│   └── final/         # FINAL outputs (canonical)
├── errors/
│   ├── test/
│   └── final/
└── logs/
    ├── test/
    └── final/
```

---

## Promotion Workflow

### Step 1: Test-1 Phase
1. Place XLSX in `input/test/` with `_TEST1_` in filename
2. Run normalizer with `--mode test`
3. Review output against [TEST1_PASS_CHECKLIST.md](../../tools/price_normalizer/TEST1_PASS_CHECKLIST.md)
4. Iterate on profile until all criteria pass

### Step 2: Freeze Decision
When Test-1 passes:
1. ✅ Copy source XLSX to `input/final/`
2. ✅ Rename to include `_FINAL_` + date
3. ✅ Lock the profile version:
   - If profile changes later, save as `{profile}_v2.yml`
   - Document changes in profile comments

### Step 3: Final Normalization
1. Run normalizer with `--mode final`:
   ```bash
   python tools/price_normalizer/normalize.py \
     --profile profiles/schneider_easy_tesys_contactors.yml \
     --file input/final/Schneider_EasyTeSys_Contactors_FINAL_2025-12-26.xlsx \
     --mode final
   ```
2. Verify output matches Test-1 (same row count, same keys)
3. Archive Test-1 files (optional, but recommended)

### Step 4: Import to FastAPI

#### TEST Mode Import
```bash
POST /api/v1/catalog/skus/import?dry_run=true
```
- ✅ Validate structure
- ✅ Detect junk rows
- ✅ Fix profile logic if needed
- ❌ No DB writes

#### FINAL Mode Import (Only Once)
```bash
POST /api/v1/catalog/skus/import?dry_run=false
```
- ✅ Writes canonical catalog
- ✅ Audit logged
- ✅ File becomes historical reference

---

## Import Discipline

### TEST Mode Rules
- **Always** use `dry_run=true`
- Never write to production database
- Outputs are for validation only
- Can be run multiple times safely

### FINAL Mode Rules
- **First run**: Use `dry_run=true` to validate
- **Second run**: Use `dry_run=false` to import
- **After import**: File is frozen - do not re-import without new FINAL file

---

## "Final Means Final" Rule

Once a FINAL CSV is imported:

1. **Do NOT** re-import the same FINAL file
2. **Do NOT** modify FINAL files in place
3. **Do** create a new FINAL file with new date if updates are needed
4. **Do** version the profile if normalization logic changes

### Exception: Versioned Updates
If the same source data needs re-import (e.g., profile bug fix):
- Create new FINAL file: `{name}_FINAL_2025-12-27.xlsx`
- Document reason in commit message
- Consider using delta/update strategy if supported by FastAPI

---

## Profile Versioning

When profile logic changes:

1. **Minor fixes** (column index adjustments):
   - Update existing profile
   - Document change in profile comments
   - Re-run FINAL normalization

2. **Major changes** (new series detection, new filters):
   - Create new version: `{profile}_v2.yml`
   - Keep old version for reference
   - Update documentation

3. **OEM-specific changes**:
   - Create new profile: `{oem}_{product}_v1.yml`
   - Don't modify existing profiles for other products

---

## Audit Trail

For each FINAL import, maintain:

1. **Source file**: `input/final/{name}_FINAL_{date}.xlsx`
2. **Normalized CSV**: `output/final/{name}_normalized_{timestamp}.csv`
3. **Summary JSON**: `logs/final/{name}_summary_{timestamp}.json`
4. **Profile used**: `profiles/{profile}.yml` (with version)
5. **Import timestamp**: From FastAPI audit log

---

## Multi-Person Workflow

When multiple people work on price imports:

1. **Coordinate FINAL imports**: Only one person imports FINAL files
2. **TEST freely**: Anyone can run TEST mode
3. **Document decisions**: Use commit messages to explain FINAL file choices
4. **Lock profiles**: After FINAL, lock profile (read-only or versioned)

---

## Troubleshooting

### "I accidentally imported a TEST file"
- Check FastAPI audit log for import timestamp
- If recent, consider rollback (if supported)
- Document incident and prevent recurrence

### "I need to update a FINAL import"
- Create new FINAL file with new date
- Document reason for update
- Import new FINAL file (old one remains in history)

### "Profile needs changes after FINAL"
- Create profile version (e.g., `_v2.yml`)
- Re-run FINAL normalization with new profile
- Document why profile changed

---

## References

- [TEST1_PASS_CHECKLIST.md](../../tools/price_normalizer/TEST1_PASS_CHECKLIST.md) - Criteria for promotion
- [Price Normalizer README](../../tools/price_normalizer/README.md) - Tool usage
- FastAPI `/catalog/skus/import` endpoint - Import API

---

## Summary

| Aspect | TEST | FINAL |
|--------|------|-------|
| **Purpose** | Learning, calibration | Canonical catalog |
| **Reusability** | Disposable | Frozen |
| **Import** | `dry_run=true` only | `dry_run=false` once |
| **File naming** | `_TEST1_` or `_TEST_` | `_FINAL_` + date |
| **Location** | `input/test/` | `input/final/` |
| **Profile changes** | Free to iterate | Lock after use |

