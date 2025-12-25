# Phase 5 Risk Register

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT  
**Owner:** Phase 5 Senate  

## Purpose
Identify, assess, and track risks that could impact Phase 5 success.

## Source of Truth
- **Canonical:** This is the authoritative risk register

## Risk Format

Each risk follows this structure:
- **Risk ID:** R-XXX
- **Date Identified:** YYYY-MM-DD
- **Risk:** Clear description of the risk
- **Impact:** What happens if risk materializes
- **Probability:** HIGH / MEDIUM / LOW
- **Severity:** HIGH / MEDIUM / LOW
- **Mitigation:** How to prevent or reduce risk
- **Status:** OPEN / MITIGATED / CLOSED

---

## Risks

### R-001: Skipping Freeze Discipline
**Date Identified:** 2025-01-27  
**Risk:** Schema changes after Phase 2 freeze without governance approval  
**Impact:** Rework across API/UI, timeline delays, cost overruns  
**Probability:** MEDIUM  
**Severity:** HIGH  
**Mitigation:** 
- Strict freeze gate checklist
- Governance approval required for any post-freeze changes
- Clear documentation of freeze status
**Status:** ⏳ OPEN

### R-002: Legacy Contamination
**Date Identified:** 2025-01-27  
**Risk:** Legacy patterns or code copied into canonical design  
**Impact:** Compromised canonical design, technical debt, future rework  
**Probability:** MEDIUM  
**Severity:** HIGH  
**Mitigation:**
- Read-only policy for `project/nish/`
- Mandatory legacy review documentation
- Explicit "what not to do" documentation
**Status:** ⏳ OPEN

### R-003: Missing Governance Fields
**Date Identified:** 2025-01-27  
**Risk:** BOM tracking fields, IsLocked, CostHead system not included in schema  
**Impact:** Schema rework, implementation delays  
**Probability:** MEDIUM  
**Severity:** HIGH  
**Mitigation:**
- Freeze gate checklist compliance matrix
- Pending upgrades integration guide
- Explicit verification before freeze
**Status:** ⏳ OPEN

### R-004: Scope Creep
**Date Identified:** 2025-01-27  
**Risk:** Analytics/BI or other features added to Phase 5 scope  
**Impact:** Timeline delays, diluted focus, incomplete core deliverables  
**Probability:** LOW  
**Severity:** MEDIUM  
**Mitigation:**
- Clear scope fence document
- Governance approval for scope changes
- Explicit exclusions documented
**Status:** ⏳ OPEN

### R-005: Incomplete Traceability
**Date Identified:** 2025-01-27  
**Risk:** Requirements not mapped to documents, gaps not identified  
**Impact:** Missing requirements, incomplete deliverables, rework  
**Probability:** MEDIUM  
**Severity:** MEDIUM  
**Mitigation:**
- Requirement trace matrix
- File-to-requirement mapping
- Regular traceability reviews
**Status:** ⏳ OPEN

### R-006: Schema Design Flaws
**Date Identified:** 2025-01-27  
**Risk:** Schema design has fundamental flaws discovered during implementation  
**Impact:** Major rework, timeline delays, cost overruns  
**Probability:** LOW  
**Severity:** HIGH  
**Mitigation:**
- Comprehensive review before freeze
- Seed script validation
- ER diagram review
- Stakeholder approval
**Status:** ⏳ OPEN

---

## Change Log
- v1.0: Created risk register with initial risks

