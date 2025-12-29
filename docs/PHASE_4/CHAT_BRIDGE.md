# CHAT_BRIDGE — Phase 4 Live State (Cursor)

**Single source of truth for Phase 4 execution status**

**Last Updated:** 2025-12-18  
**Branch/Commit:** (fill during session start)  
**Operator:** (name/initials)

## Current State
- **Stage:** S2 (Isolation)
- **Current In Progress:** NSW-P4-S2-CIM-002 (Catalog resolution single-path plan)
  - **CIM-002 Exit Criteria:**
    - Classification table present (CANONICAL/COMPAT/DUPLICATE) + governance rule for new COMPAT endpoints
    - Evidence pointer in MASTER_TASK_LIST.md points to Section 2 of S2_CIM_ISOLATION.md
- **Last Completed:** NSW-P4-S2-MASTER-001, NSW-P4-S2-EMP-001
- **S2 Progress:** 7/14 tasks complete

## Recent Decisions
- SHARED contracts frozen in S2 (no behavior change)
- ReuseSearch logging: do not log raw searchTerm (log searchTermLength only)
- Router file canonical: `/api/*` routes live under `routes/web.php` with `/api` prefix (treat as canonical until S4)
- S2 boundary rule: no QUO-V2 work, no alignment/propagation, only contracts + split plan
- MASTER reference interfaces: read-only semantics, CRUD routes are MASTER-only UI flows
- EMP reference interfaces: cross-cutting (auth middleware vs explicit lookups), read-only for consumers

## Evidence Documents
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (✅ Complete)
- `docs/PHASE_4/S2_CIM_ISOLATION.md` (🔄 In Progress - CIM-002)
- `docs/PHASE_4/S2_MASTER_ISOLATION.md` (✅ Complete)
- `docs/PHASE_4/S2_EMP_ISOLATION.md` (✅ Complete)
- `docs/PHASE_4/GAP_GATEBOARD.md`
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md`
- `docs/PHASE_4/MASTER_TASK_LIST.md`

## Next Steps (Safe Order)
1. **Finish S2 Governance** (reduce drift before MBOM):
   - NSW-P4-S2-GOV-001 (exceptions → split/adapter task stubs)
   - NSW-P4-S2-GOV-002 (boundary blocks per module)
2. **Then S2.5 BOM Modules:**
   - NSW-P4-S2-MBOM-001 (MBOM contract spec - G3/HIGH)
   - NSW-P4-S2-FEED-001 + NSW-P4-S2-FEED-GAP-001 (Feeder contract + BOM-GAP-001/002)
   - NSW-P4-S2-PBOM-001
   - NSW-P4-S2-QUO-001 (legacy boundaries)
3. **QUO-V2 remains fenced** until NSW-P4-S2-QUO-REVERIFY-001 completes

## Blockers
- QUO-V2 tasks (QUO-002, QUO-003) blocked until QUO-REVERIFY-001 completes

## S2 Rules (Enforcement)
- No QUO-V2 work in S2
- No behavior change (planning-only)
- No controller split, no route moves
- No consumer migration (S3/S4)
- COMPAT exceptions require retirement date + Bundle-C verification reference

## Stop Conditions
**Stop immediately if:** any file move / route move / behavior change / QUO-V2 touched / S3 or S4 work attempted.
