# Option A Execution Plan - Revert Mode Changes

**Date**: 2025-01-XX  
**Status**: Ready to Execute

---

## Current State

- **Files with content changes**: 16 files ✅ (should keep)
- **Files with only mode changes**: 746 files ⚠️ (should revert)

---

## Execution Steps

### Step 1: Verify Files with Content Changes

These 16 files have real content changes and should be kept:

1. `.gitignore` - 22 lines added
2. `RAG_KB/phase5_pack/08_PROMOTION_WORKFLOW.md` - timestamp update
3. `docs/PHASE_4/RISK_REGISTER.md` - 3 lines added
4. `docs/PHASE_4/S4_BATCH_2_CLOSURE.md` - 3 lines added
5. `docs/PHASE_4/evidence/BATCH_S4_2_HANDOFF.md` - 3 lines added
6. `docs/PHASE_5/00_GOVERNANCE/LEGACY_VS_NSW_COEXISTENCE_POLICY.md` - updates
7. `docs/PHASE_5/00_GOVERNANCE/PENDING_INPUTS_REGISTER.md` - 24 added, 23 deleted
8. `docs/PHASE_5/00_GOVERNANCE/PHASE_5_CHARTER.md` - 14 lines added
9. `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md` - 17 lines added
10. `docs/PHASE_5/00_GOVERNANCE/PHASE_5_MODE_POLICY.md` - 12 lines added
11. `docs/PHASE_5/00_GOVERNANCE/PHASE_5_PREREQUISITES_INTEGRATION.md` - major update
12. `docs/PHASE_5/00_GOVERNANCE/PHASE_5_TASK_LIST.md` - 40 added, 28 deleted
13. `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` - 81 added, 37 deleted
14. `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - 231 added, 2 deleted
15. `docs/PHASE_5/03_DATA_DICTIONARY/VALIDATION_GUARDRAILS_G1_G7.md` - 75 added, 4 deleted
16. `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - 224 added, 4 deleted

---

### Step 2: Revert Mode Changes

**Method 1: Use Script (Recommended)**

```bash
./scripts/revert_mode_changes_safe.sh
```

**Method 2: Manual Revert**

```bash
# Revert NSW directory (most files with mode changes)
git checkout HEAD -- "NSW  Fundmametn al Alignmetn Plan/"

# Revert other files with only mode changes
# (Check each file first to ensure it has no content changes)
```

---

### Step 3: Verify Results

After reverting, verify:
- Only 16 files with content changes remain
- No files with only mode changes remain
- All content changes are preserved

```bash
# Check remaining files
git status --short

# Verify no mode-only changes
git diff --numstat HEAD | awk '$1 == "0" && $2 == "0" {count++} END {print count}'
# Should show: 0

# Verify content changes remain
git diff --numstat HEAD | awk '$1 != "0" || $2 != "0" {count++} END {print count}'
# Should show: 16
```

---

## Expected Result

**Before**:
- 762 files modified
- 16 with content changes
- 746 with only mode changes

**After**:
- 16 files modified
- 16 with content changes ✅
- 0 with only mode changes ✅

---

## Safety Notes

1. ✅ **Content changes are preserved** - `git checkout HEAD` only reverts permissions, not content
2. ✅ **Script is safe** - Only reverts files with 0 lines added/deleted
3. ✅ **Reversible** - Can undo if needed
4. ⚠️ **Files not in git** - Will be skipped (safe)

---

## Next Steps After Reverting

1. ✅ Verify only 16 files remain
2. ⏳ Commit the 16 files with content changes
3. ⏳ Continue with other uncommitted work

---

**Ready to Execute**: ✅ Yes  
**Script Created**: `scripts/revert_mode_changes_safe.sh`

