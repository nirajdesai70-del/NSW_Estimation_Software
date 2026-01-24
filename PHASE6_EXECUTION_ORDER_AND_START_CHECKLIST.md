# Phase-6 Execution Order & Start Checklist

**Document Type:** Operational Playbook  
**Purpose:** Single operational playbook to start executing Week-by-Week (after planning freeze)  
**Status:** ✅ Planning Complete - Ready for Execution  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## 1) Global Start Checklist (Before Week-0 Execution)

### 1.1 Freeze Rules (Non-Negotiable)

Before starting execution, confirm these rules are understood and will be enforced:

- ✅ **Copy-never-link** (reuse workflows must copy, never link)
- ✅ **QCD/QCA separation** (costing datasets must be separated)
- ✅ **No costing breakup in quotation view** (costing breakup only in costing pack)
- ✅ **Fabrication summary-only** (fabrication breakdown is summary-only)
- ✅ **Schema Canon frozen (Phase-6)** (no schema changes allowed)
- ✅ **Week-8.5 Gate mandatory before Week-9** (hard blocking gate)
- ✅ **D0 Gate mandatory before Week-7 Track-D execution** (hard blocking gate)

---

### 1.2 One-Command Environment Sanity (Must Be Green)

Run these three commands every execution day to verify environment:

```bash
./scripts/status_dev.sh
./scripts/smoke_dev.sh
curl -sf http://localhost:8003/health
```

All three must pass before starting any week's work.

---

### 1.3 Evidence Discipline

For every week you execute, you must produce:

1. **Runner Script:**
   - `scripts/run_weekX_checks.sh` (or `run_week4A_checks.sh` for Week-4A)

2. **Evidence Pack:**
   - `evidence/PHASE6_WEEKX_EVIDENCE_PACK.md` (or `PHASE6_WEEK4A_EVIDENCE_PACK.md` for Week-4A)
   - Test output pasted into evidence pack
   - API samples / screenshots pasted into evidence pack
   - Runner output pasted into evidence pack

3. **Documentation (if required):**
   - Design documents (as specified in weekly plans)
   - Gate signoff documents (for D0 Gate, Week-8.5 Gate)

**Rule:** No week is CLOSED until evidence pack is complete and all tests pass.

---

## 2) Phase-6 Execution Order (Strict)

### Execution Sequence

**Stage 0 — Governance Foundation:**
```
Week-0 → Week-1 → Week-2 → Week-3 → Week-4A → Week-5 → Week-6 → D0 Gate → Week-7 → Week-8 → Week-8.5 Gate → Week-9 → Week-10 → Week-11 → Week-12
```

### Dependency Rationale

**Why this order:**
- **Week-7 Track-D depends on D0 Gate:** Track D (Costing Pack) execution is blocked until D0 Gate passes (Week-6). Planning can proceed, but execution must wait.
- **Week-9 depends on Week-8.5 PASS:** Week-9 cannot start until Week-8.5 Legacy Parity Gate passes (hard blocking gate).
- **Week-12 depends on Week-11 CLOSED:** Week-12 (formal closure) requires Week-11 to be closed first.

**Hard Blocking Gates:**
- **D0 Gate:** Must pass before Week-7 Track-D execution
- **Week-8.5 Legacy Parity Gate:** Must PASS before Week-9 execution
- **Week-11 CLOSED:** Must be CLOSED before Week-12 execution

---

## 3) Weekly Start Template (Use Every Week)

### 3.1 Start-of-Week Checklist

Before starting any week's work:

1. ✅ **Confirm prior week closure pack exists**
   - Check evidence pack for prior week
   - Verify prior week marked as CLOSED
   - Verify prior week tests passed

2. ✅ **Run prior consolidated checks (regression)**
   - Run prior week's runner to ensure no regressions
   - Fix any regressions before proceeding

3. ✅ **Create week runner script (or extend)**
   - Create `scripts/run_weekX_checks.sh` (or extend existing)
   - Include all week-specific tests
   - Include week-specific API checks
   - Include week-specific validation

4. ✅ **Create week evidence pack (empty template)**
   - Create `evidence/PHASE6_WEEKX_EVIDENCE_PACK.md`
   - Use template structure from weekly detailed plan
   - Prepare sections for test outputs, API samples, screenshots

5. ✅ **Implement tasks**
   - Follow weekly detailed plan task breakdown
   - Implement all tasks for the week
   - Follow non-negotiable rules for the week

6. ✅ **Run week checks**
   - Run `scripts/run_weekX_checks.sh`
   - Ensure all checks pass
   - Fix any failures before proceeding

7. ✅ **Paste outputs + samples into evidence pack**
   - Paste test output into evidence pack
   - Paste API samples into evidence pack
   - Paste screenshots into evidence pack
   - Paste runner output into evidence pack

8. ✅ **Commit with week tag**
   - Commit with tag: `P6-WEEK{X}: <summary>`
   - Prefer: one commit per day, one branch per week
   - Minimum: one commit per week with clean message

9. ✅ **Mark week CLOSED**
   - Update weekly detailed plan status to CLOSED
   - Verify all closure criteria met
   - Verify all compliance alarms resolved

---

### 3.2 Mandatory Structure for Commits

**Prefer:** one commit per day, one branch per week

**Minimum:** one commit per week with clean message format:
```
P6-WEEK{X}: <summary>
```

Examples:
- `P6-WEEK0: entry gate + governance pack`
- `P6-WEEK1: Add Panel API+UI + snapshot enforcement`
- `P6-WEEK6: Error/warning surfacing + D0 Gate signoff`

---

## 4) Execution Sequence — Week by Week (Concrete)

### Week-0 (Governance Pack & Entry Gate)

**Runner:** `./scripts/run_week0_checks.sh` (or equivalent)

**Deliverables:**
- Governance docs (naming conventions, module ownership, task register)
- Entry gate proofs (Phase-5 freeze references, entry gate documented)
- QCD Contract v1.0 (frozen)
- D0 Gate definition (checklist only, not passed)
- Cost template seed definition (spec-only)
- Unresolved alarm list

**Closure:** Only when compliance alarms resolved. Week-0 is governance-closed when all governance artifacts exist and are verified.

---

### Week-1 (Quotation + Panels + Customer Snapshot)

**Must implement:**
- Add Panel API + UI
- Customer snapshot enforcement (D-009 obligation)
- Frontend Add Panel modal + refresh list
- Tests: add panel + snapshot rules

**Runner:** `./scripts/run_week1_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK1_EVIDENCE_PACK.md`

**Exit Gate:** Add Panel API+UI + snapshot enforcement + tests green.

---

### Week-2 (Feeder/BOM CRUD + Tracking + Guardrails Start)

**Must implement:**
- Add Feeder/BOM/Item APIs + UI
- BOM tracking fields runtime behavior
- Guardrails foundations (G1-G8 start)
- Reuse workflows (copy feeder, copy BOM)

**Runner:** `./scripts/run_week2_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK2_EVIDENCE_PACK.md`

**Exit Gate:** CRUD works, tracking fields populated, guardrails tests present.

---

### Week-3 (Pricing UX + QCD Foundations + Guardrails)

**Must implement:**
- RateSource modes (PRICELIST / MANUAL_WITH_DISCOUNT / FIXED_NO_DISCOUNT)
- Guardrails runtime enforcement (G1-G8)
- QCD generator + JSON endpoint
- EffectiveQty logic
- Cost heads seeding

**Runner:** `./scripts/run_week3_checks.sh` (extend to include pricing+guardrails+QCD)

**Evidence pack:** `evidence/PHASE6_WEEK3_EVIDENCE_PACK.md`

**Exit Gate:** Pricing modes + guardrails green + QCD stable output.

**Note:** Guardrails must be implemented here or Phase-6 cannot close. This is a compliance requirement.

---

### Week-4A (Resolution UX + Multi-SKU + Reuse Validations)

**Must implement:**
- L0→L1→L2 resolution UX
- Resolution constraints enforcement
- Error taxonomy mapping
- Multi-SKU linkage (parent_line_id grouping, metadata_json safe edit)
- Post-reuse editability verification
- Guardrails validation after reuse

**Runner:** `./scripts/run_week4A_checks.sh` (or `./scripts/run_phase6_week4_checks.sh` if Week-4A work extends existing Week-4B runner)

**Evidence pack:** `evidence/PHASE6_WEEK4A_EVIDENCE_PACK.md`

**Exit Gate:** Resolution constraints + taxonomy + multi-SKU + reuse editability/guardrails verified.

**Note:** 
- Week-4B (read-only governance hardening) already exists as evidence (`evidence/PHASE6_WEEK4_EVIDENCE_PACK.md` exists). Week-4B work is complete.
- Week-4A is the planned UX scope that needs to be executed.
- Do not mix Week-4A and Week-4B work. Week-4A should have its own evidence pack.
- Existing script `run_phase6_week4_checks.sh` is for Week-4B (already complete). Week-4A may need a new runner or extend the existing one.

---

### Week-5 (Locking Visibility + Catalog Validation Previews)

**Must implement:**
- Lock status summary
- Lock/unlock controls (admin)
- Lock visibility indicators
- Catalog validation preview system
- Pre-import validation
- Validation results display

**Runner:** `./scripts/run_week5_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK5_EVIDENCE_PACK.md`

**Exit Gate:** Line-item lock visibility enforced + P6-LOCK-000 verified (no higher-level locking).

---

### Week-6 (Error/Warning Surfacing + D0 Gate Completion)

**Must implement:**
- Error/warning surfacing UX (price missing, unresolved resolution, validation errors)
- Error summary panel
- User-friendly error messages
- D0 Gate signoff (QCD/QCA stable, costing engine foundations complete)

**Runner:** `./scripts/run_week6_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK6_EVIDENCE_PACK.md`

**Exit Gate:** Warning surfacing stable + taxonomy/request_id + D0 Gate requirements completed and signed off.

**Note:** Week-6 core closure is Error/Warning Surfacing + D0 Gate only. Catalog Governance, Discount Editor, and API Contracts are parallel work (not closure-blocking for Week-6).

---

## 5) D0 Gate (Hard Blocker)

**Must be signed off BEFORE Week-7 Track-D execution.**

**Artifacts required:**
- `docs/PHASE_6/COSTING/D0_GATE_SIGNOFF.md` (signed off)
- QCD/QCA outputs (stable, validated)
- Numeric validation proof (engine-first validation)
- Performance notes (if required, performance targets met)

**Gate Decision:** PASS / FAIL

**If PASS:** Week-7 Track-D execution can proceed.

**If FAIL:** Week-7 Track-D execution is blocked. Return to Week-6 or earlier weeks to fix D0 Gate blockers.

**Note:** Week-7 planning can proceed without D0 Gate, but Track-D execution is blocked until D0 Gate passes.

---

### Week-7 (Costing Pack Foundation + Ops Readiness Foundation)

**Must implement:**
- Costing Pack Snapshot view (QCD/QCA only)
- Panel Summary view (QCD/QCA only)
- Role-based access foundation
- Permission checks (middleware/guards)
- Approval flows design (design only, no heavy workflow)

**Runner:** `./scripts/run_week7_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK7_EVIDENCE_PACK.md`

**Exit Gate:** Snapshot + panel summary (QCD/QCA only) + permission checks.

**Precondition:** D0 Gate must be PASSED (hard blocker for Track-D execution).

---

### Week-8 (Costing Pack Details + Ops Completion)

**Must implement:**
- BOM/Feeder costing breakdown
- CostHead grouping (mandatory)
- Pivot tables
- Costing pack navigation
- Audit visibility (audit log display, audit log details)
- SOPs creation
- Audit export
- Costing pack permissions enforcement (P6-OPS-012)

**Runner:** `./scripts/run_week8_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK8_EVIDENCE_PACK.md`

**Exit Gate:** Pivots + audit visibility + export permission foundation (P6-OPS-012).

---

## 6) Week-8.5 (Legacy Parity Gate — Verification Only)

**Runner:** None (manual gate doc - verification only, no execution)

**Deliverable:** `docs/PHASE_6/GATES/PHASE6_WEEK8_5_LEGACY_PARITY_GATE.md`

**Outcome:** PASS / CONDITIONAL PASS / FAIL

**Verification Tasks:**
- P6-GATE-LEGACY-001: Quotation reuse verified
- P6-GATE-LEGACY-002: Panel reuse verified
- P6-GATE-LEGACY-003: Feeder reuse verified + post-reuse editability verified
- P6-GATE-LEGACY-004: BOM reuse verified
- P6-GATE-LEGACY-005: Post-reuse guardrails verified
- P6-GATE-LEGACY-006: Legacy parity checklist complete

**If PASS:** Proceed to Week-9.

**If CONDITIONAL PASS:** Fix items → re-confirm → proceed to Week-9.

**If FAIL:** Return to originating week (never patch blindly). Week-9 execution is blocked.

**Note:** This is a verification gate only - no coding, no DB changes, no UI changes, no refactoring. This is a decision gate, not an execution sprint.

---

### Week-9 (Global Dashboard + Integration Tests)

**Must implement:**
- Margins dashboard (read-only, QCD/QCA only)
- Hit rates dashboard (read-only, QCD/QCA only)
- Cost drivers dashboard (read-only, QCD/QCA only)
- Dashboard filters
- End-to-end quotation creation test
- End-to-end catalog import test
- Integration testing
- Cross-track integration
- Performance testing
- End-to-end costing pack test

**Runner:** `./scripts/run_week9_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK9_EVIDENCE_PACK.md`

**Exit Gate:** Dashboards read-only + integration test suite green.

**Precondition:** Week-8.5 Legacy Parity Gate must PASS (hard blocker).

---

### Week-10 (Excel Export + Stabilization Tasks)

**Must implement:**
- Excel export functionality design
- Costing Pack Excel export (engine-first, QCD/QCA only)
- Dashboard Excel export
- Costing calculation UI integration
- Costing pack access control
- Export permission matrix
- Export permission enforcement
- Watermarking & disclaimers
- Export audit logging
- Bug fixes
- UX polish
- Documentation updates
- User acceptance testing
- Final verification

**Runner:** `./scripts/run_week10_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK10_EVIDENCE_PACK.md`

**Exit Gate:** Exports read-only + permissions + audit logging + stabilization tasks done.

**Precondition:** Week-9 must be CLOSED (hard precondition).

---

### Week-11 (Buffer Convergence)

**Must implement:**
- Address remaining issues (consolidated fix list)
- Final testing (final regression + integration runs)
- Documentation finalisation (completed docs + evidence packs)

**Runner:** `./scripts/run_week11_checks.sh`

**Evidence pack:** `evidence/PHASE6_WEEK11_EVIDENCE_PACK.md`

**Exit Gate:** Zero critical blockers + all runners green.

**Precondition:** Week-9 integration complete (or within fixable delta), Week-10 export layer complete (or within fixable delta), no open canon violations remain.

**Note:** Week-11 does NOT add features. It is strictly for resolving remaining defects, UAT feedback closure, performance hardening (if required), documentation completion, and final readiness checks.

---

### Week-12 (Formal Closure)

**Deliverables:**
- Phase-6 exit criteria verification report
- Success metrics verification report
- Phase-6 closure report
- Handover to Phase-7 documentation
- Canon compliance signoff document
- Formal closure declaration

**Runner:** None (governance only, no execution)

**Evidence pack:** `evidence/PHASE6_WEEK12_EVIDENCE_PACK.md` (closure documentation)

**Exit Gate:** PASS/FAIL only (binary closure).

**Precondition:** Week-11 must be CLOSED, no critical or compliance alarms remain open, D0 Gate = PASSED, Week-8.5 Legacy Parity Gate = PASSED, no canon violations remain.

**Note:** Week-12 does NOT add features, fix bugs, refactor code, or tune performance. All work is verification, documentation, and sign-off only. If Week-12 feels "boring", it means Phase-6 was done correctly.

---

## 7) One-Page "Start Execution Tomorrow" Checklist

When you are ready to actually begin execution:

1. ✅ **Pick Week-0 branch:** `phase6/week0` (or create if doesn't exist)

2. ✅ **Run environment sanity checks:**
   ```bash
   ./scripts/status_dev.sh
   ./scripts/smoke_dev.sh
   curl -sf http://localhost:8003/health
   ```
   All three must pass.

3. ✅ **Create Week-0 artifacts:**
   - `scripts/run_week0_checks.sh` (create or verify exists)
   - `evidence/PHASE6_WEEK0_EVIDENCE_PACK.md` (create empty template)

4. ✅ **Execute Week-0 tasks only:**
   - Follow `PHASE6_WEEK0_DETAILED_PLAN.md` task breakdown
   - Implement governance pack tasks
   - Implement entry gate verification tasks

5. ✅ **Run week checks:**
   ```bash
   ./scripts/run_week0_checks.sh
   ```
   Ensure all checks pass.

6. ✅ **Paste output into evidence pack:**
   - Paste test output into evidence pack
   - Paste verification results into evidence pack
   - Paste any documentation into evidence pack

7. ✅ **Commit with week tag:**
   ```bash
   git commit -m "P6-WEEK0: entry gate + governance pack"
   ```

8. ✅ **Tag Week-0 as CLOSED:**
   - Update `PHASE6_WEEK0_DETAILED_PLAN.md` status to CLOSED
   - Verify all closure criteria met
   - Verify all compliance alarms resolved

9. ✅ **Then proceed Week-1 next:**
   - Follow same process for Week-1
   - Continue week-by-week in strict order

---

## 8) Gate Enforcement Rules

### D0 Gate

**Location:** Week-6 completion  
**Artifact:** `docs/PHASE_6/COSTING/D0_GATE_SIGNOFF.md`  
**Blocks:** Week-7 Track-D execution  
**Rule:** Week-7 Track-D execution cannot proceed until D0 Gate is signed off.

### Week-8.5 Legacy Parity Gate

**Location:** After Week-8 completion  
**Artifact:** `docs/PHASE_6/GATES/PHASE6_WEEK8_5_LEGACY_PARITY_GATE.md`  
**Blocks:** Week-9 execution  
**Rule:** Week-9 cannot start until Week-8.5 Gate passes (hard blocking gate).

### Week-11 Closure

**Location:** After Week-10 completion  
**Blocks:** Week-12 execution  
**Rule:** Week-12 cannot start until Week-11 is CLOSED.

---

## 9) Evidence Pack Template Structure

Each week's evidence pack should follow this structure:

```markdown
# Phase-6 Week-X Evidence Pack

**Week:** Week-X  
**Status:** ✅ CLOSED  
**Date Completed:** YYYY-MM-DD

---

## Executive Summary

Brief summary of what was delivered in this week.

---

## Test Results

### Test Suite Execution

Paste test output here.

### Test Coverage

Document test coverage for this week's tasks.

---

## API Verification

### API Endpoints

List and verify all API endpoints implemented.

### API Samples

Paste API request/response samples here.

---

## UI Screenshots

Paste UI screenshots here (if applicable).

---

## Runner Output

Paste runner script output here.

---

## Verification Checklist

- [ ] All tasks completed
- [ ] All tests passing
- [ ] All compliance alarms resolved
- [ ] Evidence pack complete
- [ ] Week marked as CLOSED
```

---

## 10) Common Pitfalls to Avoid

### Pitfall 1: Skipping Gates

**Problem:** Trying to proceed to Week-7 without D0 Gate, or Week-9 without Week-8.5 Gate.

**Solution:** Gates are hard blockers. Do not bypass. Wait for gate signoff before proceeding.

### Pitfall 2: Mixing Week-4A and Week-4B

**Problem:** Mixing planned Week-4A work with already-completed Week-4B work.

**Solution:** Week-4B is already complete (evidence exists). Week-4A is the planned UX scope. Keep them separate.

### Pitfall 3: Adding Features in Buffer Weeks

**Problem:** Adding new features in Week-11 or Week-12.

**Solution:** Week-11 and Week-12 are strictly for buffer/convergence and closure. No new features allowed.

### Pitfall 4: Incomplete Evidence Packs

**Problem:** Marking weeks as CLOSED without complete evidence packs.

**Solution:** Evidence packs are mandatory. No week is CLOSED until evidence pack is complete.

### Pitfall 5: Schema Changes

**Problem:** Introducing schema changes during Phase-6 execution.

**Solution:** Schema Canon is frozen. No schema changes allowed. If schema changes are needed, document for Phase-7.

---

## 11) References

- **Master Planning Document:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Weekly Detailed Plans:** `PHASE6_WEEK0_DETAILED_PLAN.md` through `PHASE6_WEEK12_DETAILED_PLAN.md`
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md`
- **D0 Gate Definition:** Week-0 governance pack
- **Week-8.5 Gate Definition:** `PHASE6_WEEK8_5_DETAILED_PLAN.md`

---

**Document Status:** ✅ Complete - Ready for Execution  
**Last Updated:** 2025-01-27  
**Next Step:** Begin Week-0 execution when ready
