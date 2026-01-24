# Root Streamlining Plan v1.0 (Approved)
## NSW Estimation Software — Operational Root + Baseline Bridge

**Status:** APPROVED (planning document of record)

**Operational root (authoritative):** `/Volumes/T9/Projects/NSW_Estimation_Software/` ✅  
**Baseline root (external, read-only):** `/Volumes/T9/Projects/NSW Estimation Software V1.0/` 🔒

---

## 1) Objective
- Enforce **one operational root**: `NSW_Estimation_Software/` for all ongoing work (Cursor + dev + docs + RAG/KB).
- Freeze the V1.0 folder as an **external read-only baseline reference**.
- Prevent drift/confusion via **clear demarcation**, **full mapping**, **bridge stubs**, and **port authority**.

---

## 2) Operating Model (4 Zones)
- **Zone A (Canonical / Source of Truth):**
  - `docs/PHASE_*`, `docs/GOVERNANCE`, `docs/CONTROL_TOWER`, `trace/`, code (`backend/`, `frontend/`, `services/`, `tools/`)
- **Zone B (Legacy / non-canonical):**
  - `legacy/…` (reference only; never SoT)
- **Zone C (Adoption lane from V1.0):**
  - `docs/MIGRATION/ADOPTED_FROM_V1/…`
  - `tools/MIGRATION/ADOPTED_FROM_V1/…`
- **Zone D (External Baseline):**
  - `/Volumes/T9/Projects/NSW Estimation Software V1.0/` (read-only)

**Hard rule:** If any V1.0 doc/code/process is required, it must be **copied into Zone C**, tagged, and registered. No ad-hoc dependencies on V1.0 paths.

---


## 2.1) Navigation chart (canonical entry points)

Use this chart to navigate. **Do not browse by guesswork.**

```
NSW_Estimation_Software/                      (ONLY operational root)
├── docs/                                     (operational documentation)
│   ├── NSW_ESTIMATION_MASTER.md              (START HERE: path authority + program status)
│   ├── MASTER_EXECUTION_PLAN.md              (phase status + what’s next)
│   ├── CONTROL_TOWER/                        (gates, CI, ports, control registries)
│   ├── GOVERNANCE/                           (authority matrix, move register, rules)
│   ├── PHASE_1/..PHASE_6/                    (phase execution documentation)
│   └── MIGRATION/                            (mapping CSVs, audit reports, adopted intake)
├── trace/                                    (traceability maps, inventories, evidence pointers)
├── backend/ frontend/ services/              (code)
├── tools/                                    (tooling, migration scripts, catalog pipelines)
├── docker-compose*.yml                       (runtime stacks; must reference ops/ports.env)
├── ops/                                      (machine authority: ports.env etc.)
└── legacy/                                   (non-canonical; reference-only)

External baseline (read-only):
/Volumes/T9/Projects/NSW Estimation Software V1.0/
```

## 2.2) “Old vs new work” bifurcation rules (explicit)

### What counts as **NEW / ACTIVE** work
- Anything under **Zone A** (canonical) is current work and may be updated.

### What counts as **OLD / LEGACY** work
- Anything under **Zone B (`legacy/`)** is **not authoritative**.
- Legacy content is kept for reference only and must not be treated as SoT.
- If legacy content is needed for active work, it must be **adopted** via Zone C.

### What counts as **ADOPTED** work
- Anything copied from V1.0 into **Zone C** is an “intake item” and must carry the adoption header.
- After review, adopted items may be promoted into Zone A, leaving behind a redirect stub.

### Promotion rule (prevents Zone-C sprawl)
- Any Zone-C item that is used operationally must be promoted to Zone-A within the same phase or within 7 days, leaving behind a redirect stub and a PATH_MOVE_REGISTER entry.

### What counts as **BASELINE REFERENCE**
- The external V1.0 folder is reference-only; it must never be edited as part of ongoing execution.
- Baseline should be referenced only via `docs/V1_0_BASELINE_POINTER.md`.

## 2.3) Navigation process (how to find the right file fast)

Use this decision table:

- **Need phase execution guidance?** → `docs/PHASE_*/` and `docs/MASTER_EXECUTION_PLAN.md`
- **Need governance rules / authority?** → `docs/GOVERNANCE/` (especially `AUTHORITY_MATRIX.md`)
- **Need CI/security/ports status?** → `docs/CONTROL_TOWER/` (and `ops/ports.env`)
- **Need traceability maps?** → `trace/phase_2/` (ROUTE_MAP / FEATURE_CODE_MAP / FILE_OWNERSHIP)
- **Need baseline V1.0 reference?** → `docs/V1_0_BASELINE_POINTER.md` (never deep-link directly)
- **Need a document moved/renamed?** → `docs/GOVERNANCE/PATH_MOVE_REGISTER.md`


## 3) Governance Docs (Canonical)
Create/maintain:
1. `docs/GOVERNANCE/AUTHORITY_MATRIX.md` (required)
2. `docs/GOVERNANCE/PATH_MOVE_REGISTER.md` (append-only)
3. `docs/V1_0_BASELINE_POINTER.md` (required)
4. `docs/MIGRATION/V1_STRUCTURE_MIRROR_INDEX.md` (required)
5. `legacy/README.md` (required; explains “legacy is not authority”)

---

## 4) Full Mapping (100% coverage, auditable)

### 4.1 Inventory
Generate inventories of **operational artifacts only**:
- `.md`, `.yml/.yaml`, `.json`, `.env*`, `docker-compose*.yml`, `.sh`, `.py`, `.txt`, `.csv`

For:
- V1.0 baseline tree
- Execution repo tree

Store outputs under:
- `docs/MIGRATION/INVENTORIES/`

### 4.2 Mapping CSV
Run `tools/migration/v1_to_exec_map.py` to produce:
- `docs/MIGRATION/V1_TO_EXECUTION_FULL_PATH_MAP.csv`

Columns:
- `old_path,new_path,mapping_type,status,notes`

### 4.3 Unmapped Decision Workflow
For each `status=MISSING_IN_EXECUTION`:
- **ADOPTED** → copy into Zone C + header + register entry
- **REFERENCE_ONLY** → baseline remains external; mirror index points to baseline item
- **REJECTED/OBSOLETE** → recorded decision

### 4.4 Adoption Metadata Header
Every adopted doc/script includes standard header:
- origin path, adoption status, adoption date, owner, reason

---

## 5) Bridge Layer (to avoid link breakage)

### 5.1 Pointer doc
`docs/V1_0_BASELINE_POINTER.md` becomes the only canonical baseline reference.

### 5.2 Alias Stubs (redirect-only)
Create redirect README stubs for high-traffic legacy paths (no content duplication).  
Stubs may exist under `docs/…` purely to redirect and prevent broken links.

---

## 6) RAG/KB Ports + Links (Verify → Consolidate → Enforce)

### 6.1 Discovery
Scan both trees for ports/URLs/endpoints and store results under:
- `docs/MIGRATION/PORT_AUDIT/`

### 6.2 Consolidation (Single Authority)
Create:
- `ops/ports.env` (machine authority)
- `docs/CONTROL_TOWER/PORT_REGISTRY.md` (human authority)

Ensure compose files reference `ops/ports.env`.

### 6.3 Drift Guard
Add guard checks (pre-commit or CI):
- block absolute V1.0 path references in docs
- (optional later) block non-registry ports in docs

---

## 7) Guardrails (No Drift)
- Cursor workspace must open only `NSW_Estimation_Software/`
- repo-relative links only
- baseline referenced only via pointer doc
- legacy referenced only via `legacy/README.md`

---

## 8) Attachments/Binaries handling (separate from mapping)
Because PDFs/XLSX/DOCX create noise and false “missing” flags, they are tracked separately from the canonical path map:
- Create `docs/MIGRATION/ATTACHMENTS_REGISTRY.csv` (or `.md`) listing:
  - `baseline_path`, `execution_path` (if copied), `status` (REFERENCE_ONLY / COPIED), `notes`

---

## 9) Repo-wide link safety (additional care point)
A repo-wide audit must run before any “structure migration” is considered complete.

**Canonical audit outputs (execution repo):**
- `docs/MIGRATION/LINK_AUDIT/summary.txt`
- `docs/MIGRATION/LINK_AUDIT/all_findings.tsv`
- `docs/MIGRATION/LINK_AUDIT/broken_internal_links.tsv`

**Triage rule (prevents waste):**
- First fix **broken links under `docs/`** (operational documentation).
- Broken links inside **reference packs** (`RAG_KB/`, `source_snapshot/`, `NSW Fundamental Alignment Plan/`, etc.) are handled as either:
  - converted to **REFERENCE_ONLY** behavior (no expectation of link validity), or
  - repaired only if they are used operationally.

**Absolute-path rule:**
- No new docs/scripts should contain absolute machine paths (e.g., `/Volumes/T9/...`). Replace with repo-relative paths or variables.

---

## 10) Implementation Sequence (after review confirmation)
1. Create zones + governance docs
2. Add mapping script + generate inventories + mapping CSV
3. Classify unmapped items (ADOPTED / REFERENCE_ONLY / REJECTED)
4. Adopt required items into Zone C (tagged + registered)
5. Add alias stubs
6. Port audit + port registry + `ops/ports.env` enforcement
7. Run repo-wide link audit; fix `docs/` broken links first
8. Add guard checks

---

## 11) To-Do List (execution checklist)
Use this as the single execution checklist. Check items off in order.

### Phase A — Foundation (no content moves yet)
- [ ] **Workspace rule enforced**: Cursor opens only `NSW_Estimation_Software/` (baseline is read-only).
- [ ] **Zone folders created**: `legacy/`, `docs/MIGRATION/ADOPTED_FROM_V1/`, `tools/MIGRATION/ADOPTED_FROM_V1/`, `docs/MIGRATION/INVENTORIES/`, `docs/MIGRATION/PORT_AUDIT/`.
- [ ] **Governance docs created**:
  - [ ] `docs/GOVERNANCE/AUTHORITY_MATRIX.md`
  - [ ] `docs/GOVERNANCE/PATH_MOVE_REGISTER.md` (append-only)
  - [ ] `docs/V1_0_BASELINE_POINTER.md`
  - [ ] `docs/MIGRATION/V1_STRUCTURE_MIRROR_INDEX.md`
  - [ ] `legacy/README.md`

### Phase B — Mapping + decisions
- [ ] **Mapping tool added**: `tools/migration/v1_to_exec_map.py`.
- [ ] **Inventories generated** (operational artifacts only) and stored under `docs/MIGRATION/INVENTORIES/`.
- [ ] **Full mapping CSV generated**: `docs/MIGRATION/V1_TO_EXECUTION_FULL_PATH_MAP.csv`.
- [ ] **Decision list produced** for `status=MISSING_IN_EXECUTION`.
- [ ] **Classify each missing item**: ADOPTED / REFERENCE_ONLY / REJECTED.

### Phase C — Adoption + bridging
- [ ] **Adopt required items**: copy into Zone C with adoption header + register entry.
- [ ] **Alias stubs created** (redirect-only) for high-traffic legacy paths (e.g. `docs/04_TASKS_AND_TRACKS/README.md`).

### Phase D — Ports authority (machine + human)
- [ ] **Create `ops/ports.env`** (single machine authority).
- [ ] **Create `docs/CONTROL_TOWER/PORT_REGISTRY.md`** (human authority).
- [ ] **Update compose files** to reference `ops/ports.env`.
- [ ] **Run port/link discovery scans** and store outputs under `docs/MIGRATION/PORT_AUDIT/`.

### Phase E — Link safety + guardrails
- [ ] **Run repo-wide link audit** (outputs under `docs/MIGRATION/LINK_AUDIT/`).
- [ ] **Fix broken links under `docs/` first** (operational docs).
- [ ] **Re-run link audit** and confirm `docs/` broken links are resolved (or explicitly documented as exceptions).
- [ ] **Guardrails added** (pre-commit/CI):
  - [ ] block absolute baseline paths (`/Volumes/...V1.0...`) in docs
  - [ ] (optional later) block non-registry ports in docs

---

## 12) Resume paused work (after transition) — checklist
Once Phases A–E are complete, resume week/gate execution.

- [ ] **Start from canonical navigation** (`docs/NSW_ESTIMATION_MASTER.md` → `docs/MASTER_EXECUTION_PLAN.md` → relevant `docs/PHASE_*`).
- [ ] **Confirm runtime ports** match `ops/ports.env` and `docs/CONTROL_TOWER/PORT_REGISTRY.md`.
- [ ] **Run the day-start sanity checks** (as defined by your active execution playbooks).
- [ ] **Continue the paused work item** with evidence discipline + no-go rules unchanged.



