# Canonical Extractor - Full Series vs Page-8 Only

**Date**: 2025-01-XX  
**Status**: ✅ DOCUMENTED

---

## Scope Decision

**Answer**: **Full LC1E** (not Page-8 only)

The canonical extractor extracts the **full LC1E series** from the pricelist, not just Page-8 tables.

---

## Count Differences

### Rebuild Output (Full LC1E)
- **LC1E_CANONICAL_ROWS**: 23 rows
- **LC1E_COIL_CODE_PRICES**: 59 rows

### V6 Page-8 Only Output
- **Canonical rows**: 21 rows (Page-8 Table-1 only)
- **Coil prices**: 40 rows (Page-8 Table-1 only)

**Difference**: Rebuild includes additional LC1E sections beyond Page-8.

---

## Why Full Series?

1. **Completeness**: Full series extraction provides complete catalog coverage
2. **Reusability**: Same extractor can be used for all LC1E sections
3. **Consistency**: All LC1E products follow same structure
4. **Future-proof**: Easy to add Page-8 filter later if needed

---

## Future Option: Page-8 Filter

If exact Page-8 matching is needed, add filter option:

```bash
--filter_table_id "P8_T1"  # Filter to Page-8 Table-1 only
--filter_source_page 8      # Filter to Page-8 only
```

**Current**: No filter (full series extraction)

---

## Validation

When comparing rebuild output to v6:
- ✅ **Structure matches**: NSW format sheets are identical
- ✅ **Normalization matches**: Duty/voltage normalization is correct
- ⚠️ **Counts differ**: Full series (23/59) vs Page-8 only (21/40)

**This is expected and correct** - rebuild extracts full series, v6 is Page-8 subset.

---

## Recommendation

**For LC1E validation**: Compare structure and normalization, not exact counts.

**For future series**: Use full series extraction (current approach) unless specific table filtering is required.

---

**Status**: ✅ DOCUMENTED - Full series extraction is intentional

