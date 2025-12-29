# S4 — Propagation Execution Checklist (Phase 4)
#
# Status: ACTIVE (S4)
# Last Updated: 2025-12-18

---

## Scope + Fence (non-negotiable)

- S4 is **propagation only**:
  - ✅ move/extract implementations according to S3 frozen contracts
  - ✅ migrate consumers from compat → canonical
  - ✅ keep route names/URIs stable unless explicitly approved
- S4 is **not behavior change**:
  - ❌ no pricing/discount/quantity formula changes
  - ❌ no optimization “for cleanliness”
- QUO-V2 is unfenced, but **still PROTECTED**:
  - any PROTECTED touchpoints require G4 controls per Rulebook

---

## Entry Conditions (must be true)

- S3 documents are ACTIVE and complete:
  - `S3_SHARED_ALIGNMENT.md`
  - `S3_CIM_ALIGNMENT.md`
  - `S3_BOM_ALIGNMENT.md`
  - `S3_QUO_ALIGNMENT.md`
- Rollback plan exists for every HIGH/PROTECTED task
- Bundles A/B/C are ready to be executed (or evidence method agreed)

---

## Safe execution order (authoritative)

1. **S4.1 SHARED propagation** (lowest blast radius)
2. **S4.2 CIM consumer migration**
3. **S4.3 BOM consumer alignment propagation**
4. **S4.4 QUO legacy cleanup propagation**
5. **S4.5 QUO-V2 propagation (only if needed; PROTECTED gates)**

---

## Gating rules (apply every time)

- HIGH tasks → G3 evidence + rollback mandatory
- PROTECTED tasks → G4 evidence + approvals mandatory
- Any gate failure → stop immediately (Rulebook abort conditions)

---

## Evidence checklist (per task)

- [ ] task ID + scope recorded
- [ ] files touched recorded
- [ ] rollback steps recorded and feasible
- [ ] test bundle mapping recorded (A/B/C)
- [ ] evidence attached (screenshots/logs/test output)
- [ ] approval recorded (as required)

---

## S4 “Done” definition

S4 is complete when:
- all planned propagations are executed or explicitly deferred
- no consumer remains on deprecated/compat endpoints unintentionally
- rollback paths are verified for HIGH/PROTECTED changes
- S5 regression gate is ready to run


