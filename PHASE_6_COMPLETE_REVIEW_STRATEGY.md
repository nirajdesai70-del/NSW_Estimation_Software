# Phase 6 Complete Review Strategy
## Strategy to Review ALL 88+ Committed Files & Track Renamed/Moved Files

**Date:** 2025-01-27  
**Status:** COMPREHENSIVE STRATEGY  
**Purpose:** Review ALL files including committed, renamed, and moved files

---

## 🎯 Problem Statement

### Files Not Covered Yet
1. **88+ committed files** - In git history but not in root directory
2. **Renamed files** - Files that may have been moved/renamed
3. **Moved files** - Files in different directories
4. **Files in subdirectories** - docs/PHASE_5/, docs/PHASE_6/, evidence/, etc.

### Challenge
- How to access committed files?
- How to track renamed/moved files?
- How to review files efficiently?
- How to ensure nothing is missed?

---

## 📋 Strategy Overview

### Phase 1: Identify ALL Files (Including Committed)
### Phase 2: Track Renamed/Moved Files
### Phase 3: Review Strategy for Committed Files
### Phase 4: Review Strategy for Renamed/Moved Files
### Phase 5: Comprehensive Review Execution

---

## 🔍 Phase 1: Identify ALL Files

### Step 1.1: Get Complete File List from Git

```bash
# Get all Phase 6 files from git history (excluding RAG_KB copies)
git log --all --name-only --pretty=format: -- "*PHASE*6*.md" "*PHASE6*.md" 2>/dev/null | \
  grep -v "RAG_KB" | \
  grep -v "\._" | \
  sort -u > phase6_all_files_from_git.txt
```

### Step 1.2: Categorize Files

**Category A: Files in Root (22 files)** ✅
- Already reviewed
- No action needed

**Category B: Committed Files Not in Root (88+ files)** ⚠️
- Need to review from git
- May need to checkout

**Category C: Files in Subdirectories (25+ files)** ⚠️
- docs/PHASE_5/00_GOVERNANCE/ (15 files)
- docs/PHASE_6/ (8 files)
- evidence/ (some files)
- project/nish/ (1 file)

**Category D: Renamed/Moved Files** ⚠️
- Need to track using git log --name-status
- May have different names now

---

## 🔄 Phase 2: Track Renamed/Moved Files

### Step 2.1: Find Renamed Files

```bash
# Find files that were renamed
git log --all --diff-filter=R --name-status --pretty=format: -- "*PHASE*6*.md" "*PHASE6*.md" 2>/dev/null | \
  grep "^R" | \
  sort -u > phase6_renamed_files.txt
```

### Step 2.2: Find Moved Files

```bash
# Find files that were moved (same content, different path)
git log --all --diff-filter=R --name-status --pretty=format: -- "*PHASE*6*.md" "*PHASE6*.md" 2>/dev/null | \
  grep "^R" | \
  awk '{print $2 " -> " $3}' > phase6_moved_files.txt
```

### Step 3.3: Create File Mapping

**Purpose:** Map old names to new names/locations

**Example:**
- `PHASE_6_EXECUTION_PLAN.md` (old) → `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md` (new)
- `PHASE_6_SCOPE.md` (old) → `PHASE_6_COMPLETE_SCOPE_AND_TASKS.md` (new)

---

## 📖 Phase 3: Review Strategy for Committed Files

### Method 1: Read from Git History (Recommended)

**Advantage:** No need to checkout, can read directly

```bash
# Read a specific file from git history
git show HEAD:PHASE_6_EXECUTION_PLAN.md

# Read from specific commit
git show <commit-hash>:PHASE_6_EXECUTION_PLAN.md

# Read from any branch
git show <branch-name>:PHASE_6_EXECUTION_PLAN.md
```

**Process:**
1. Get file list from git
2. For each file, read using `git show`
3. Extract key information
4. Update review documents

### Method 2: Checkout to Temporary Location

**Advantage:** Can use file tools, easier to read

```bash
# Create temporary directory
mkdir -p /tmp/phase6_review

# Checkout specific files
git checkout HEAD -- PHASE_6_EXECUTION_PLAN.md
mv PHASE_6_EXECUTION_PLAN.md /tmp/phase6_review/

# Review files
# Then cleanup
rm -rf /tmp/phase6_review
```

### Method 3: Use Git Archive

**Advantage:** Get all files at once

```bash
# Archive all Phase 6 files from specific commit
git archive HEAD --output=phase6_files.tar.gz -- "*PHASE*6*.md" "*PHASE6*.md"

# Extract and review
tar -xzf phase6_files.tar.gz
```

---

## 🔄 Phase 4: Review Strategy for Renamed/Moved Files

### Step 4.1: Identify Current Location

**For each renamed file:**
1. Check if new name exists in current filesystem
2. If exists, review current version
3. If not, read from git using old name
4. Document the rename/move

### Step 4.2: Review Both Versions

**If file was renamed:**
- Review old version (from git)
- Review new version (if exists)
- Compare differences
- Document changes

**If file was moved:**
- Review old location (from git)
- Review new location (if exists)
- Document move

---

## 📊 Phase 5: Comprehensive Review Execution

### Step 5.1: Create Complete File Inventory

**Include:**
- Files in root (22 files) ✅
- Committed files (88+ files) ⚠️
- Files in subdirectories (25+ files) ⚠️
- Renamed files (TBD) ⚠️
- Moved files (TBD) ⚠️

**Total: 135+ files**

### Step 5.2: Prioritize Review Order

**Priority 1: Core Files (40 files)**
- Already identified
- 10-11 hours estimated

**Priority 2: Committed Core Files (30+ files)**
- Similar to Priority 1 but committed
- 7-8 hours estimated

**Priority 3: Subdirectory Files (25+ files)**
- docs/PHASE_5/, docs/PHASE_6/, etc.
- 5-6 hours estimated

**Priority 4: Renamed/Moved Files (TBD)**
- Need to identify first
- 2-3 hours estimated

**Priority 5: Other Committed Files (20+ files)**
- Remaining committed files
- 3-4 hours estimated

### Step 5.3: Review Process

**For each file:**
1. **Access File**
   - If in filesystem: Read directly
   - If committed: Use `git show`
   - If renamed: Check both old and new

2. **Review Content**
   - Read and understand
   - Extract key findings
   - Extract tasks/todos
   - Identify gaps

3. **Document Findings**
   - Update master consolidated document
   - Update review tracker
   - Mark as reviewed

4. **Track Status**
   - Mark file status (reviewed/pending)
   - Note any issues
   - Document findings

---

## ⏱️ Updated Time Estimation

### Original Estimate (40 files): 10-11 hours

### Additional Files to Review:

| Category | Files | Time Estimate |
|----------|-------|---------------|
| Committed Core Files | 30+ | 7-8 hours |
| Subdirectory Files | 25+ | 5-6 hours |
| Renamed/Moved Files | TBD | 2-3 hours |
| Other Committed Files | 20+ | 3-4 hours |
| **TOTAL ADDITIONAL** | **75+ files** | **17-21 hours** |

### Complete Review Estimate:

| Category | Files | Time Estimate |
|----------|-------|---------------|
| Priority 1 (Original) | 40 | 10-11 hours |
| Priority 2 (Committed Core) | 30+ | 7-8 hours |
| Priority 3 (Subdirectories) | 25+ | 5-6 hours |
| Priority 4 (Renamed/Moved) | TBD | 2-3 hours |
| Priority 5 (Other Committed) | 20+ | 3-4 hours |
| **TOTAL** | **115+ files** | **27-32 hours** |

### Realistic Estimate: **28-30 hours**

---

## 🛠️ Tools & Scripts Needed

### Script 1: Get All Files from Git

```bash
#!/bin/bash
# get_all_phase6_files.sh

git log --all --name-only --pretty=format: -- "*PHASE*6*.md" "*PHASE6*.md" 2>/dev/null | \
  grep -v "RAG_KB" | \
  grep -v "\._" | \
  grep -v "WEEK[0-9]" | \
  sort -u > phase6_all_files.txt

echo "Total files found: $(wc -l < phase6_all_files.txt)"
```

### Script 2: Find Renamed Files

```bash
#!/bin/bash
# find_renamed_files.sh

git log --all --diff-filter=R --name-status --pretty=format: -- "*PHASE*6*.md" "*PHASE6*.md" 2>/dev/null | \
  grep "^R" | \
  awk '{print $2 " -> " $3}' > phase6_renamed_files.txt

echo "Renamed files found: $(wc -l < phase6_renamed_files.txt)"
```

### Script 3: Review File from Git

```bash
#!/bin/bash
# review_file_from_git.sh <file-path>

FILE=$1
COMMIT=${2:-HEAD}

echo "Reviewing: $FILE from $COMMIT"
echo "---"

git show $COMMIT:"$FILE" 2>/dev/null || echo "File not found in $COMMIT"
```

### Script 4: Batch Review Committed Files

```bash
#!/bin/bash
# batch_review_committed.sh <file-list>

while IFS= read -r file; do
  echo "Reviewing: $file"
  git show HEAD:"$file" > "/tmp/review_$(basename $file)" 2>/dev/null
  if [ $? -eq 0 ]; then
    echo "  ✅ Extracted to /tmp/review_$(basename $file)"
  else
    echo "  ❌ Not found in HEAD"
  fi
done < "$1"
```

---

## 📋 Execution Plan

### Week 1: Setup & Initial Review

**Day 1 (4 hours):**
- Run scripts to get all files
- Identify renamed/moved files
- Create complete file inventory
- Prioritize files

**Day 2-3 (10 hours):**
- Review Priority 1 files (40 files)
- Use git show for committed files
- Document findings

### Week 2: Comprehensive Review

**Day 4-5 (10 hours):**
- Review Priority 2 files (30+ committed core files)
- Review Priority 3 files (25+ subdirectory files)
- Document findings

**Day 6 (4 hours):**
- Review Priority 4 files (renamed/moved)
- Review Priority 5 files (other committed)
- Document findings

### Week 3: Consolidation

**Day 7-8 (4 hours):**
- Consolidate all findings
- Create unified task list
- Update all review documents
- Create final summary

**Total: 3 weeks, 28-30 hours**

---

## ✅ Deliverables

1. **Complete File Inventory**
   - All 135+ files listed
   - Status of each file (reviewed/pending)
   - Location of each file

2. **Renamed/Moved File Mapping**
   - Old name → New name
   - Old location → New location
   - Changes documented

3. **Updated Master Consolidated Document**
   - All findings from ALL files
   - All gaps identified
   - All tasks extracted

4. **Complete Task & Todo List**
   - From ALL reviewed files
   - Unified and prioritized
   - Mapped to tracks

5. **Final Review Summary**
   - All files reviewed
   - All findings documented
   - Work closure document

---

## 🚀 Quick Start

### Step 1: Get All Files
```bash
./scripts/get_all_phase6_files.sh
```

### Step 2: Find Renamed Files
```bash
./scripts/find_renamed_files.sh
```

### Step 3: Review Priority 1 Files
```bash
# Review each file using git show
git show HEAD:PHASE_6_EXECUTION_PLAN.md
```

### Step 4: Document Findings
- Update master consolidated document
- Update review tracker
- Mark files as reviewed

---

**Status:** STRATEGY READY  
**Total Files to Review:** 115+ files (excluding Week 0-12)  
**Estimated Time:** **28-30 hours**  
**Timeline:** **3 weeks** (or 2 weeks focused)
