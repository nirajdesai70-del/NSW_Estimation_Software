---
Source: RAG_KB/phase5_pack/08_PROMOTION_WORKFLOW.md
KB_Namespace: rag_governance
Status: CANONICAL
Version: v1.0
Last_Updated: 2025-12-27T22:27:22.242430
KB_Path: phase5_pack/08_PROMOTION_WORKFLOW.md
---
# Promotion Workflow — WORKING → CANONICAL

**Version:** 1.0  
**Last Updated:** 2025-12-27  
**Status:** CANONICAL  
**Authority:** Phase 5 Governance

---

## Purpose

This document defines the formal promotion gates for moving documents from WORKING to CANONICAL status, ensuring governance and authority are maintained in the RAG Knowledge Base.

---

## Status Definitions

### CANONICAL
- **Definition:** Authoritative, locked content that represents the official state
- **Use Cases:**
  - Governance documents (rulebook, charter, decisions)
  - Finalized specifications and schemas
  - Approved policies and standards
- **Characteristics:**
  - Must include front-matter header with `Status: CANONICAL` or `Status: LOCKED`
  - Must have a version number
  - Must be referenced by governance charter or decision log
  - Changes require explicit approval process

### WORKING
- **Definition:** Active work-in-progress content
- **Use Cases:**
  - Feature execution plans
  - Draft specifications
  - Implementation notes
  - Chat mirror transcripts
- **Characteristics:**
  - May or may not have front-matter header
  - Default status for new files
  - Can be updated freely during active work
  - Not authoritative for policy/governance queries

### DRAFT
- **Definition:** Preliminary content under review
- **Use Cases:**
  - Early-stage proposals
  - Experimental designs
  - Review queues
- **Characteristics:**
  - Lower priority in ranking
  - Should not be used for authoritative decisions

### DEPRECATED
- **Definition:** Superseded or outdated content
- **Use Cases:**
  - Files replaced by newer versions
  - Obsolete specifications
- **Characteristics:**
  - Remains searchable for historical queries only
  - Should not appear in normal search results

---

## Promotion Gates

### Gate 1: Header Requirements
- ✅ File must include YAML front-matter header with:
  - `Status: CANONICAL` (or `Status: LOCKED`)
  - `Version: <semver>` (e.g., `v1.0`, `v1.2.3`)
  - `Owner: <authority>` (recommended)
  - `Updated: <ISO date>` (recommended)

### Gate 2: Authority Requirements
- ✅ Source file must be:
  - Referenced by governance charter/decision log, OR
  - Explicitly approved by Phase 5 governance authority, OR
  - Part of an approved batch/freeze that declares CANONICAL status

### Gate 3: Review Requirements
- ✅ Content must be:
  - Reviewed and approved by appropriate authority (Arch/Exec/Release as applicable)
  - Free of open questions or ambiguities
  - Aligned with governance rules

### Gate 4: Deprecation Handling
- ✅ If promoting supersedes an existing document:
  - Mark old document as `Status: DEPRECATED`
  - Update references in decision log
  - Ensure version numbers reflect progression

---

## Promotion Process

### Step 1: Prepare Document
1. Ensure content is complete and accurate
2. Add front-matter header with required fields
3. Set `Status: CANONICAL` or `Status: LOCKED`
4. Assign version number (semver format)

### Step 2: Request Approval
1. Document must be referenced in:
   - `02_DECISIONS_LOG.md` (if a decision), OR
   - Governance charter/rulebook (if governance doc), OR
   - Approved batch/freeze register (if part of batch)
2. Obtain explicit approval from appropriate authority

### Step 3: Execute Promotion
1. Update file header: `Status: CANONICAL`
2. Update version number if changed
3. If superseding another doc, mark old doc as `Status: DEPRECATED`
4. Run `kb_refresh` to update index

### Step 4: Verification
1. Run `kb_refresh` → verify file appears in CANONICAL count
2. Query with governance keywords → verify CANONICAL doc surfaces in top results
3. Check `01_CANONICAL_MASTER.md` → verify entry appears

---

## _ACTIVE_FILE.txt Policy

### When to Use
- Only in Phase-5 execution folders during active work
- When you need to force selection of a specific file despite newer files existing
- Temporary override during review/approval cycles

### Rules
- Must point to a WORKING or CANONICAL file only (not DRAFT)
- File must exist in the same folder
- Should be removed after promotion/work is complete
- Will be flagged as broken if file doesn't exist

### Format
```
filename.md
```
(Just the filename, one line)

---

## Deprecation Process

### When to Deprecate
- File has been superseded by a newer CANONICAL version
- Content is no longer accurate or relevant
- Policy/specification has been replaced

### How to Deprecate
1. Add/update front-matter: `Status: DEPRECATED`
2. Optionally add note: `Superseded by: <new_file_path>`
3. Update references in decision log if applicable
4. Run `kb_refresh` to update index

### Deprecated File Behavior
- Remains in index for historical queries
- Ranked lowest (score = 0)
- Only appears if explicitly requested (history queries)
- Cannot be promoted back to WORKING/CANONICAL (requires new file)

---

## Who Can Promote

### Governance Documents
- **Authority:** Phase 5 Governance / Architecture Lead
- **Required Approval:** Architectural approval
- **Gate Level:** G3/G4

### Feature Specifications
- **Authority:** Module Owner / Architecture Lead
- **Required Approval:** Architectural approval
- **Gate Level:** G3

### Decisions
- **Authority:** Phase 5 Senate / Governance
- **Required Approval:** Architectural + Executive approval
- **Gate Level:** G4
- **Recorded In:** `02_DECISIONS_LOG.md`

### Implementation Notes
- **Authority:** Technical Lead / Implementation Owner
- **Required Approval:** Executive approval
- **Gate Level:** G2/G3

---

## Enforcement

### Automated Checks
- `kb_refresh` validates:
  - Front-matter format (if present)
  - Status values (normalized)
  - Version format (if present)
  - _ACTIVE_FILE.txt validity

### Manual Reviews
- Review `RISKS_AND_GAPS.md` for:
  - Missing headers
  - Broken _ACTIVE_FILE.txt markers
  - Low CANONICAL coverage

### Query Validation
- Test governance queries → must return CANONICAL docs in top results
- Verify authority boost is working correctly

---

## References

- `01_CANONICAL_MASTER.md` — Master list of CANONICAL sources
- `02_DECISIONS_LOG.md` — Log of locked decisions
- `03_FEATURE_FLAGS.md` — Feature flags registry
- `RISKS_AND_GAPS.md` — Risk tracking and gaps report
- `00_FOLDER_MAP.md` — Folder structure and active file selection
- `RAG_RULEBOOK.md` — Overall RAG governance rules

---

## Change Control

This document is **CANONICAL**. Changes require:
- Governance task entry (NSW-P4-S0-GOV-###)
- Architectural approval
- Version update

**Last Approved:** 2025-12-27  
**Version:** 1.0

