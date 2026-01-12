# Action Plan: Uncommitted Work Review

**Date**: 2025-01-XX  
**Status**: Review Complete - Ready for Execution

---

## Summary

This document provides a step-by-step action plan to address all uncommitted work identified in the comprehensive review. Each item has been categorized and prioritized.

---

## Phase 1: Fix Blocking Issues (HIGH PRIORITY)

### 1.1 Fix Git Pack Issues ⚠️ BLOCKING

**Problem**: macOS resource fork files in `.git/objects/pack/` causing "non-monotonic index" errors

**Solution**: Run cleanup script

**Action**:
```bash
./scripts/fix_git_pack_issues.sh
```

**Expected Result**: Git commands work without errors

**Status**: ⏳ **READY TO EXECUTE**

---

### 1.2 Verify Git Operations

**Action**: After fixing pack issues, verify:
```bash
git status
git diff --stat HEAD | head -20
```

**Expected Result**: Clean git operations, no errors

**Status**: ⏳ **PENDING** (depends on 1.1)

---

## Phase 2: Review Modified Files (HIGH PRIORITY)

### 2.1 Categorize Modified Files

**Action**: After git is fixed, categorize 762 modified files:
- Documentation updates
- Code changes
- Configuration changes
- Unintended changes

**Files to Review**:
- `.github/workflows/rag_ci.yml` - CI/CD configuration
- `INDEX.md` - Documentation index
- `MASTER_PROJECT_DOCUMENTATION.md` - Master documentation
- Files in `NSW  Fundmametn al Alignmetn Plan/` - Alignment plan

**Status**: ⏳ **PENDING** (depends on 1.1)

---

### 2.2 Decision: Commit, Stash, or Revert

**Action**: For each category, decide:
- **Commit**: If changes are intentional and complete
- **Stash**: If changes are work-in-progress
- **Revert**: If changes are unintended

**Status**: ⏳ **PENDING** (depends on 2.1)

---

## Phase 3: Complete RAG KB Updates (MEDIUM PRIORITY)

### 3.1 Update KB Indexer

**Current**: Using SQLite FTS5 with BM25  
**Target**: Use `rank-bm25` library

**Action**:
1. Backup current `services/kb_indexer/indexer.py`
2. Replace with recommended implementation using `rank-bm25`
3. Update dependencies: `pip install rank-bm25`
4. Test indexing with real KB pack

**Files**:
- `services/kb_indexer/indexer.py`
- `services/kb_indexer/keyword_index.py`

**Status**: ⏳ **READY TO IMPLEMENT**

---

### 3.2 Update KB Refresh Runner

**Current**: Dict-based config, no SHA256 hashing  
**Target**: Dataclasses, SHA256 hashing

**Action**:
1. Backup current `tools/kb_refresh/run_kb_refresh.py`
2. Replace with recommended implementation
3. Ensure chat_mirror scanning is preserved
4. Test dry-run mode

**Files**:
- `tools/kb_refresh/run_kb_refresh.py`

**Status**: ⏳ **READY TO IMPLEMENT**

---

### 3.3 Test End-to-End RAG Pipeline

**Action**: After updates:
1. Run KB refresh: `python3 tools/kb_refresh/run_kb_refresh.py --dry-run`
2. Run indexer: `python3 services/kb_indexer/indexer.py --rebuild`
3. Test query service: `curl http://localhost:8011/health`
4. Verify search quality

**Status**: ⏳ **PENDING** (depends on 3.1, 3.2)

---

## Phase 4: Organize Untracked Files (MEDIUM PRIORITY)

### 4.1 Port Policy Documentation ✅ READY

**Files**:
- `PORT_POLICY.md`
- `PORT_POLICY_IMPLEMENTATION_COMPLETE.md`
- `PORT_POLICY_REVIEW_AND_IMPLEMENTATION_PLAN.md`

**Action**: Commit these files (documentation is complete)

**Status**: ✅ **READY TO COMMIT**

---

### 4.2 NSW Fundamental Alignment Plan

**Directories**:
- `NSW Fundamental Alignment Plan/` (organized structure)
- `NSW  Fundmametn al Alignmetn Plan/` (alternative spelling, duplicate?)

**Action**:
1. Review both directories
2. Determine if one is duplicate/outdated
3. Consolidate if needed
4. Decide on commit strategy

**Status**: ⏳ **NEEDS REVIEW**

---

### 4.3 Enhancement Work

**Files**:
- `Enhensment Work/P5_ENH_pg_textsearch_BM25_InDB_Search_Option.md`
- `Enhensment Work/KPI_Manual_Cost_Percentage_Conversation.md`
- `Enhensment Work/NS_Ware_Full_Conversation_Log.md`

**Action**:
1. Review enhancement proposals
2. Decide on adoption timeline
3. Commit as proposals or archive

**Status**: ⏳ **NEEDS REVIEW**

---

### 4.4 RAG KB Documentation

**Files**:
- `RAG_KB/UPDATE_RECOMMENDATION.md`
- `RAG_KB/REVIEW_AND_UPDATE_PLAN.md`
- Other RAG KB documentation

**Action**: Review and commit if documentation is current

**Status**: ⏳ **NEEDS REVIEW**

---

### 4.5 Setup/Completion Documents

**Files**:
- `DATABASE_MIGRATION_SETUP_COMPLETE.md`
- `SETUP_COMPLETE.md`
- `TWEAKS_COMPLETE.md`
- `NEW_BUILD_SETUP_COMPLETE.md`

**Action**: Review and commit if status is accurate

**Status**: ⏳ **NEEDS REVIEW**

---

### 4.6 Clean Up Resource Fork Files

**Action**: Delete all `._*` files from working directory (now ignored by `.gitignore`)

```bash
find . -name "._*" -type f -delete
```

**Status**: ⏳ **READY TO EXECUTE** (safe, files are now ignored)

---

## Phase 5: Final Verification (LOW PRIORITY)

### 5.1 Verify All Changes

**Action**: After all phases:
1. Run git status (should be clean)
2. Verify no blocking issues
3. Test critical functionality
4. Update documentation if needed

**Status**: ⏳ **PENDING** (depends on all previous phases)

---

### 5.2 Update Project Documentation

**Action**: Update main documentation to reflect:
- Port policy implementation
- RAG KB updates
- Current project status

**Status**: ⏳ **PENDING** (depends on all previous phases)

---

## Execution Order

### Immediate (Do First)
1. ✅ Fix git pack issues (Phase 1.1)
2. ✅ Verify git operations (Phase 1.2)
3. ✅ Review modified files (Phase 2)

### Short Term (This Week)
4. ⏳ Complete RAG KB updates (Phase 3)
5. ⏳ Organize untracked files (Phase 4)

### Long Term (As Needed)
6. ⏳ Final verification (Phase 5)

---

## Quick Reference: Files Created in This Review

- ✅ `scripts/fix_git_pack_issues.sh` - Git pack cleanup script
- ✅ `UNCOMMITTED_WORK_SUMMARY.md` - Comprehensive summary
- ✅ `ACTION_PLAN_UNCOMMITTED_WORK.md` - This document
- ✅ `.gitignore` - Updated to exclude `._*` files

---

## Notes

- **Git Pack Issues**: Must be fixed before any other git operations
- **Modified Files**: Need review after git is fixed
- **RAG KB Updates**: Can be done independently
- **Untracked Files**: Can be organized gradually

---

**Last Updated**: 2025-01-XX  
**Next Review**: After Phase 1 completion

