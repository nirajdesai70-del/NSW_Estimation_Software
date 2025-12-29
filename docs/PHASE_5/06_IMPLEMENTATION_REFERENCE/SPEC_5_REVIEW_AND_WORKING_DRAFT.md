# SPEC-5 Review & Working Draft for Phase 5

**Date:** 2025-01-27  
**Last Updated:** 2025-01-27  
**Status:** ✅ COMPLETE - SPEC-5 v1.0 Ready for Review  
**Purpose:** Review SPEC-5 alignment with Phase 5 scope and create working draft with task list

**See Also:**
- `PHASE_5_READINESS_REVIEW_CONSOLIDATED.md` — Consolidated status (1 page, ready-to-send)
- `SPEC_5_FREEZE_GATE_CHECKLIST.md` — Compliance matrix for freeze gate
- `SPEC_5_FREEZE_RECOMMENDATIONS.md` — Executive recommendations

---

## 🔍 Executive Summary

The SPEC-5 document provides a comprehensive implementation specification for building NSW as a **full new build project**. This review assesses:
1. **Alignment** with existing Phase 5 scope and principles
2. **Technical clarifications** needed
3. **Scope positioning** (Phase 5 vs Post-Phase 5)
4. **Working draft** with task breakdown for execution

## ✅ Key Clarifications Received

### Technical Stack & Architecture
- **NS Ware:** Not a formal architecture pattern. Just use the same technical services/environment (FastAPI, Postgres, NATS, React). No ADR needed.
- **Purpose:** Consistency with proven technical stack, not architectural formalization.

### Database Design
- **Customer Table:** Will be defined per business standard. Separate discussion during Phase 5. Current approach (customers table + customer_name text field) is acceptable as placeholder.
- **Resolution Levels:** L0/L1/L2 should be supported at **ALL levels** (Master BOM items AND Quotation BOM items). Not just Master BOM = L0/L1 and Quote BOM = L2.

### BOM Hierarchy & Nested BOMs
- **Any BOM can be parent, any BOM can be child:** If a BOM is used inside another BOM, it's recognized as a child to that parent BOM.
- **Same BOM in different contexts:** The same BOM can be a parent in one context and a child in another context.
- **Implication:** Schema must support hierarchical/nested BOM structures where BOMs can contain other BOMs.
- **Resolution levels independent:** BOM hierarchy (parent-child) is independent of resolution levels (L0/L1/L2). A child BOM can have L0/L1/L2 items.

---

## ✅ SPEC-5 Completion Status

**SPEC-5 v1.0 Status:** ✅ **COMPLETE - READY FOR FREEZING**

The SPEC-5 canvas now includes a complete, end-to-end, implementable specification:

| Component | Status | Location in SPEC-5 |
|-----------|--------|-------------------|
| **UX Logic** | ✅ Complete | UI Navigation + UI Wireframe Logic (textual) |
| **DB DDL** | ✅ Complete | Complete Postgres schema with all tables, constraints, indexes |
| **Seed Data** | ✅ Complete | Full seed script (tenant, users, CIM masters, products, BOM, quotation) |
| **Local Run** | ✅ Complete | docker-compose.yml + Dockerfiles + auto-init scripts |
| **CI/CD Pipeline** | ✅ Complete | GitHub Actions workflows (CI on PRs, staging auto-deploy, prod manual-gated) |
| **OpenAPI Contracts** | ✅ Complete | Screen-driven endpoint list + common conventions + core schemas |
| **Role & Permission Matrix** | ✅ Complete | admin/estimator/reviewer/viewer + approval queue governance + rate override policy |
| **UI Handoff Spec** | ✅ Complete | Figma-ready checklist (design system + screen list + interaction rules + table standards) |
| **API Response Examples** | ✅ Complete | JSON examples for top 10 MVP APIs (Auth, Products, Apply Template, Resolve Multi-SKU, Cost Summary, etc.) |

**Recommendation:** SPEC-5 v1.0 is **READY TO BE FROZEN** and handed to implementation team. All components are complete and execution-ready.

---

## ✅ Alignment Review

### Strong Alignment ✅

The SPEC-5 document aligns well with Phase 5 principles:

| Aspect | SPEC-5 Position | Phase 5 Position | Status |
|--------|----------------|------------------|--------|
| **Full new build** | ✅ New build, not extension | ✅ Clean canonical definitions | ✅ ALIGNED |
| **No legacy dependency** | ✅ No migration required | ✅ No legacy data in Phase 5 | ✅ ALIGNED |
| **Master BOM L0/L1 only** | ✅ ProductId must be NULL | ✅ L0/L1 in Master BOM | ✅ ALIGNED |
| **Copy-never-link** | ✅ Independent instances | ✅ Copy semantics | ✅ ALIGNED |
| **Multi-tenant design** | ✅ Tenant isolation | ✅ Multi-tenant required | ✅ ALIGNED |
| **Master data governance** | ✅ No auto-create, approval queue | ✅ Governance rules | ✅ ALIGNED |
| **Tenant → Customer → Quotation** | ✅ Hierarchy defined | ✅ Locked in SPEC-5 | ✅ ALIGNED |
| **Feeder = BOM group** | ✅ No separate entity | ✅ Locked in SPEC-5 | ✅ ALIGNED |

### Scope Positioning ⚠️

**Critical Finding:** SPEC-5 includes **full implementation** (FastAPI, React, Docker, CI/CD, etc.), but **Phase 5 scope is analysis-only** (Step 1: Data Dictionary, Step 2: Schema Design).

| SPEC-5 Content | Phase 5 Scope | Post-Phase 5 Scope | Recommendation |
|----------------|---------------|-------------------|----------------|
| Data Dictionary definitions | ✅ Step 1 | - | **USE IN PHASE 5** |
| Schema DDL/SQL | ✅ Step 2 | - | **USE IN PHASE 5** |
| ER Diagram | ✅ Step 2 | - | **USE IN PHASE 5** |
| API Surface design | ⚠️ Not explicitly in Phase 5 | ✅ Post-Phase 5 | **PLANNING REFERENCE** |
| UI Wireframe logic | ⚠️ Not explicitly in Phase 5 | ✅ Post-Phase 5 | **PLANNING REFERENCE** |
| FastAPI/React implementation | ❌ Not in Phase 5 | ✅ Post-Phase 5 | **POST-PHASE 5** |
| Docker/CI/CD setup | ❌ Not in Phase 5 | ✅ Post-Phase 5 | **POST-PHASE 5** |

**Conclusion:** SPEC-5 is a **comprehensive planning document** that spans Phase 5 (analysis) and Post-Phase 5 (implementation). It should be treated as:
- **Phase 5 inputs:** Data dictionary concepts, schema design, business rules
- **Post-Phase 5 roadmap:** Implementation architecture, tech stack, UI/API design

---

## ❓ Technical Clarifications Needed

### 0. Phase 5 Prerequisites & Integration 🔴 **HIGH PRIORITY**

**Question:** Has SPEC-5 been verified against `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` requirements?

**Phase 5 Requirements (from PENDING_UPGRADES_INTEGRATION.md):**
- BOM tracking fields (origin_master_bom_id, instance_sequence_no, is_modified, modified_by, modified_at)
- Validation Guardrails G1-G7 as business rules
- CostHead system (cost_heads table + cost_head_id FKs)
- AI entities (ai_call_logs + related tables)
- IsLocked fields on quotation tables
- Audit trail requirements
- Module ownership definitions
- Naming conventions

**Clarification Needed:**
- [ ] **CRITICAL:** Has SPEC-5 schema DDL been verified to include ALL fields from PENDING_UPGRADES_INTEGRATION.md?
- [ ] **CRITICAL:** Are Validation Guardrails G1-G7 documented in SPEC-5 business rules?
- [ ] **CRITICAL:** Is module ownership defined in SPEC-5?
- [ ] **CRITICAL:** Are naming conventions defined in SPEC-5?
- [ ] Should we create a **verification checklist** to cross-check SPEC-5 against Phase 5 requirements?

**Action:** Create gap analysis checklist and verify SPEC-5 completeness against Phase 5 requirements before freezing v1.0.

---

### 1. NS Ware Structure Format ✅ **RESOLVED**

**Clarification:** NS Ware is not a formal architecture pattern requiring ADR documentation. The purpose is to use the same technical services/environment setup that was used in NS Ware project for consistency.

**SPEC-5 States:**
- Adopt NS Ware technical stack/services for same environment
- Technical stack: FastAPI backend, Postgres DB, NATS JetStream, React frontend
- This is about reusing proven technical services, not formalizing as architecture pattern

**Resolution:**
- ✅ No ADR needed - just use the same technical services/environment
- ✅ Technical stack selection is straightforward (FastAPI, Postgres, NATS, React)
- ✅ No formal documentation needed beyond what's in SPEC-5

**Action:** None required - proceed with technical stack as specified in SPEC-5.

---

### 2. Phase 5a/5b Concept 🔴 **HIGH PRIORITY**

**Question:** SPEC-5 introduces "Phase 5a (local server)" and "Phase 5b (web/cloud)". How does this relate to existing Phase 5 scope?

**Existing Phase 5:**
- Step 1: Data Dictionary (analysis-only)
- Step 2: Schema Design (design-only)
- No implementation phases

**SPEC-5 Proposes:**
- Phase 5a: Local server deployment
- Phase 5b: Web/cloud deployment

**Clarification Needed:**
- [ ] Are Phase 5a/5b **renaming** of Post-Phase 5 implementation phases?
- [ ] Or are they **extending** Phase 5 scope to include implementation?
- [ ] Should we align naming: Phase 5 (analysis) → Post-Phase 5 (implementation) → Phase 5a/5b?

**Recommendation:** Keep Phase 5 as analysis-only. Rename Phase 5a/5b to Post-Phase 5 implementation milestones.

---

### 3. API & UI Design in Phase 5? 🟡 **MEDIUM PRIORITY**

**Question:** Should API surface design and UI wireframe logic be included in Phase 5 Step 1/2?

**SPEC-5 Includes:**
- Complete API surface definition (`/v1/...` endpoints)
- UI wireframe logic (textual descriptions)

**Phase 5 Scope Says:**
- Step 1: Entity definitions, business semantics
- Step 2: Table structure, relationships

**Clarification Needed:**
- [ ] Should API design be part of Step 1 (data dictionary includes "how data is accessed")?
- [ ] Should UI wireframe logic be part of Step 2 (schema includes "how data is presented")?
- [ ] Or should these be deferred to Post-Phase 5?

**Recommendation:** Include API surface and UI wireframe logic in Phase 5 as **design artifacts** (not implementation), as they inform data dictionary and schema decisions.

---

### 4. Database Schema: Customer Table ✅ **DEFERRED - SEPARATE DISCUSSION**

**Question:** SPEC-5 DDL includes `customers` table with `tenant_id`, but quotation table references `customer_name` (text field). Should this be normalized?

**SPEC-5 Schema Shows:**
```sql
customers(id, tenant_id, code, name, status)
quotations(id, tenant_id, quote_no, customer_name, ...)  -- text field, not FK
```

**Resolution:**
- ✅ Customer table design will be defined per business standard
- ✅ Separate discussion needed to determine customer entity requirements
- ✅ Not a blocker for SPEC-5 v1.0 - can be resolved during Phase 5 Step 1/2
- ✅ Current approach (customers table + customer_name text field) is acceptable as placeholder

**Action:** Defer to separate business discussion during Phase 5 execution. Will be resolved in Data Dictionary (Step 1) and Schema Design (Step 2).

---

### 5. L1→L2 Explosion: Parent-Child Linkage 🟢 **LOW PRIORITY**

**Question:** SPEC-5 mentions preserving parent-child linkage for multi-SKU expansion via `metadata_json` or `parent_line_id`. Which approach is preferred?

**SPEC-5 States:**
- L1→L2 explosion can create N line items
- Preserve linkage via `metadata_json` or `parent_line_id` (to be added)

**Clarification Needed:**
- [ ] Should we add `parent_line_id` to `quote_bom_items` schema?
- [ ] Or use `metadata_json` for flexibility?
- [ ] What are the query/display requirements for grouped items?

**Recommendation:** Add `parent_line_id` column if hierarchical display/rollup is needed. Use `metadata_json` for additional context only.

---

### 6. Resolution Level Handling ✅ **CLARIFIED - ALL LEVELS SUPPORTED**

**Question:** How are resolution levels (L0/L1/L2) handled across all BOM levels?

**Clarification:**
- ✅ Resolution levels (L0/L1/L2) should be handled at ALL levels (Master BOM, Quotation BOM, nested BOMs)
- ✅ Any BOM can be a parent, any BOM can be a child
- ✅ If a BOM is used inside another BOM, it's recognized as a child to that parent BOM
- ✅ The same BOM can be a parent in one context and a child in another (hierarchical/nested BOMs)
- ✅ This supports nested BOM structures where BOMs can contain other BOMs

**Implications:**
- Schema must support `resolution_level` (L0/L1/L2) at all BOM item levels
- Both `master_bom_items` and `quote_bom_items` should support L0/L1/L2
- BOM hierarchy must support parent-child relationships (BOMs containing BOMs)
- Resolution levels are independent of BOM hierarchy (a child BOM can have L0/L1/L2 items)

**Action:** Update schema design to:
1. Support `resolution_level` in both `master_bom_items` and `quote_bom_items`
2. Support hierarchical BOM relationships (parent BOM → child BOM)
3. Document that any BOM can be parent or child depending on context

---

### 7. Seed Script & Development Setup 🟡 **MEDIUM PRIORITY**

**Question:** SPEC-5 includes a Postgres seed script and proposes docker-compose.yml for local development. What is the role of these in Phase 5?

**SPEC-5 Includes:**
- Complete Postgres seed script with:
  - 1 tenant (TENANT_DEMO)
  - 1 admin user + roles (admin/estimator/reviewer/viewer)
  - 1 customer (CUST_DEMO)
  - CIM masters (category/subcategory/type + attributes + mappings)
  - Make/Series + Generic(L1) + Specific(L2) products with SKU
  - Default price list + price row
  - 1 Master BOM template + 2 items (L0 + L1)
  - 1 sample quotation + 1 panel + default BOM group + 1 resolved line item
- Proposed: docker-compose.yml for one-command local run (Postgres + NATS + FastAPI + React)

**Phase 5 Scope Says:**
- Step 1: Data Dictionary (analysis-only)
- Step 2: Schema Design (design-only)
- No database creation or runtime testing

**Clarification Needed:**
- [ ] Should seed script be included in Phase 5 Step 2 as a **design validation artifact** (proves schema supports real-world data scenarios)?
- [ ] Or should seed script be deferred to Post-Phase 5 implementation (actual database setup)?
- [ ] Is seed script useful for **schema review** (demonstrates relationships and constraints work correctly)?
- [ ] Should docker-compose.yml be created in Phase 5 or Post-Phase 5?
- [ ] What is the purpose of seed script: development fixture, testing fixture, or schema validation?

**Recommendation:** 
- **Seed script as design artifact (Step 2):** Include seed script SQL in Phase 5 Step 2 deliverables as a **validation tool** to verify schema design supports real-world data patterns. This is documentation/design, not implementation.
- **Docker-compose as Post-Phase 5:** Defer docker-compose.yml to Post-Phase 5 implementation phase (actual runtime setup).
- **Use seed script for:** Schema review, relationship validation, constraint testing (without running database).

**Detailed Questions for Seed Script:**

1. **Seed Script Content Validation:**
   - [ ] Does seed script demonstrate **all resolution levels** (L0 placeholder, L1 generic descriptor, L2 resolved product)?
   - [ ] Does seed script include **Master BOM with L0/L1 items only** (no ProductId)?
   - [ ] Does seed script include **quotation with L2 resolved items** (ProductId required)?
   - [ ] Does seed script demonstrate **multi-tenant isolation** (tenant_id on all tables)?
   - [ ] Does seed script demonstrate **customer relationship** (FK vs text field)?
   - [ ] Does seed script include **price effective dating** (multiple prices with date ranges)?
   - [ ] Does seed script demonstrate **import approval queue** (pending items)?

2. **Seed Script Data Quality:**
   - [ ] Are sample data values **realistic** (representative of actual usage)?
   - [ ] Do seed data relationships **match business rules** (e.g., Specific product must reference Generic)?
   - [ ] Are **constraints validated** (e.g., Generic product has no Make/Series)?
   - [ ] Does seed script **exercise all foreign key relationships**?

3. **Seed Script Structure:**
   - [ ] Is seed script **idempotent** (can run multiple times safely)?
   - [ ] Does seed script **respect insert order** (dependencies inserted first)?
   - [ ] Are **default values** properly set (status, created_at, etc.)?
   - [ ] Is seed script **commented** (explains purpose of each section)?

**Detailed Questions for Docker-Compose Setup (Post-Phase 5):**

1. **Service Configuration:**
   - [ ] What Postgres version? (Latest stable or specific version?)
   - [ ] What NATS version? (JetStream enabled by default?)
   - [ ] What FastAPI/Python version? (Python 3.11+?)
   - [ ] What React/Node version? (Node 18+?)

2. **Development vs Production:**
   - [ ] Should docker-compose support **hot reload** for development (volume mounts)?
   - [ ] Should docker-compose include **production-like** setup or development-only?
   - [ ] How to handle **environment variables** (.env file, docker-compose env, secrets)?

3. **Database Setup:**
   - [ ] Should docker-compose **auto-run migrations** on startup?
   - [ ] Should docker-compose **auto-run seed script** on first startup?
   - [ ] How to handle **database persistence** (volumes, backups)?

4. **Service Communication:**
   - [ ] What **network configuration** (bridge, host, custom network)?
   - [ ] What **port mappings** (Postgres: 5432, NATS: 4222, API: 8000, UI: 3000)?
   - [ ] How do services **discover each other** (service names, environment variables)?

5. **One-Command Startup:**
   - [ ] Should startup script **check prerequisites** (Docker, docker-compose installed)?
   - [ ] Should startup script **wait for services** to be healthy before proceeding?
   - [ ] Should startup script **display URLs** (API docs, UI, etc.)?
   - [ ] Should startup script support **different environments** (dev, test, staging)?

---

### 8. CI/CD Pipeline & Environment Strategy 🟡 **MEDIUM PRIORITY**

**Question:** SPEC-5 proposes GitHub Actions CI/CD pipeline and environment strategy (local → staging → prod). What is the role of this in Phase 5?

**SPEC-5 Includes (✅ Complete):**
- Complete Docker Compose local server setup
- Auto-run DB init on first boot (schema + seed)
- Backend + Frontend Dockerfiles
- One-command run: `docker compose up -d --build`
- **GitHub Actions CI/CD pipeline (production-grade)**
  - CI on PRs (backend tests + frontend build)
  - Auto-deploy to staging on main branch
  - Manual-gated production deploy
  - Docker-based deployments (same artifacts everywhere)
  - Forward-only database migrations strategy
  - Observability hooks (/healthz, /readyz, logs, NATS monitor)
- **Clear environments:** local → staging → prod

**Phase 5 Scope Says:**
- Step 1: Data Dictionary (analysis-only)
- Step 2: Schema Design (design-only)
- No implementation work

**Clarification Needed:**
- [ ] Should CI/CD pipeline design be included in Phase 5 as **planning artifact** (defines how schema will be deployed)?
- [ ] Or should CI/CD pipeline be deferred to Post-Phase 5 implementation?
- [ ] Should environment strategy (local → staging → prod) be documented in Phase 5 Step 2 (schema deployment strategy)?
- [ ] Is CI/CD pipeline design useful for **validating schema migration strategy** (forward-only migrations)?

**Recommendation:**
- **CI/CD pipeline design as planning artifact (Step 2):** Document high-level CI/CD strategy and environment approach in Phase 5 Step 2 as part of schema deployment planning. This is design/planning, not implementation.
- **Environment strategy as schema deliverable:** Include environment deployment approach in `NSW_SCHEMA_CANON_v1.0.md` (how schema will be deployed to different environments).
- **Implementation deferred:** Actual GitHub Actions workflows and pipeline execution deferred to Post-Phase 5.

**Detailed Questions for CI/CD Pipeline (Post-Phase 5):**

1. **Pipeline Stages:**
   - [ ] What are the **pipeline stages** (lint → test → build → deploy)?
   - [ ] Should pipeline run on **every commit** (PR checks) or only on merge (main branch)?
   - [ ] What **quality gates** are required (test coverage %, lint errors, security scans)?
   - [ ] Should pipeline include **automated schema migration** tests (validate DDL changes)?

2. **Testing Strategy:**
   - [ ] Should pipeline run **unit tests** (backend + frontend)?
   - [ ] Should pipeline run **integration tests** (API + database)?
   - [ ] Should pipeline run **end-to-end tests** (full stack)?
   - [ ] Should pipeline include **database migration tests** (test schema changes in test DB)?
   - [ ] What **test coverage threshold** is required (e.g., 80%)?

3. **Build & Deployment:**
   - [ ] Should pipeline **build Docker images** and push to container registry?
   - [ ] Should pipeline use **multi-stage builds** for optimization?
   - [ ] Should pipeline support **feature branch deployments** (preview environments)?
   - [ ] What **deployment strategy** (blue-green, rolling, canary)?

4. **Environment Promotion:**
   - [ ] What is the **promotion path** (local → staging → prod)?
   - [ ] Should **staging require manual approval** before promotion to prod?
   - [ ] Should **database migrations run automatically** or require manual approval?
   - [ ] How to handle **rollback** (migration rollback strategy, container rollback)?

5. **GitHub Actions Specific:**
   - [ ] What **workflow triggers** (push, pull_request, manual dispatch)?
   - [ ] What **secrets** are needed (DB credentials, API keys, container registry tokens)?
   - [ ] Should workflows be **modular** (reusable workflows for common steps)?
   - [ ] What **artifact storage** (test results, build artifacts, coverage reports)?

6. **Database Migration Strategy:**
   - [ ] Should migrations be **versioned** (timestamp-based or sequential numbering)?
   - [ ] Should migrations be **idempotent** (safe to run multiple times)?
   - [ ] How to handle **migration conflicts** (multiple developers, branch merges)?
   - [ ] Should migration pipeline include **backup before migration** (production safety)?

7. **Security & Compliance:**
   - [ ] Should pipeline include **security scans** (vulnerability scanning, dependency checks)?
   - [ ] Should pipeline include **secrets scanning** (check for exposed credentials)?
   - [ ] Should pipeline enforce **code signing** or other compliance checks?
   - [ ] What **access controls** (who can trigger deployments, approve promotions)?

8. **Monitoring & Observability:**
   - [ ] Should pipeline publish **deployment notifications** (Slack, email, etc.)?
   - [ ] Should pipeline **tag releases** (Git tags, semantic versioning)?
   - [ ] Should pipeline **update deployment status** (deployment tracking system)?
   - [ ] Should pipeline include **health checks** after deployment (verify services are up)?

---

## 📋 Working Draft: Task Breakdown

### Phase 5 Tasks (Analysis & Design Only)

#### Task Group 1: Data Dictionary (Step 1)

**Duration:** 2-4 weeks  
**Prerequisite:** Phase 4 exit criteria met

- [ ] **T1.1:** Review SPEC-5 entity definitions against existing canonical model
  - Compare with `ITEM_MASTER_DETAILED_DESIGN.md`
  - Identify semantic gaps or conflicts
  - Document resolution decisions

- [ ] **T1.2:** Document technical stack selection
  - Use NS Ware technical services/environment (FastAPI, Postgres, NATS, React)
  - No formal ADR needed - just document technical stack choice
  - Define module boundaries (if not already in SPEC-5)

- [ ] **T1.3:** Finalize entity semantics
  - Category / SubCategory / Type / Attribute
  - Products (Generic L1 / Specific L2)
  - Master BOM items (L0/L1/L2 supported)
  - Quotation BOM items (L0/L1/L2 supported)
  - Resolution levels (L0/L1/L2 definitions at all levels)
  - BOM hierarchy (parent-child BOM relationships, nested BOMs)

- [ ] **T1.4:** Define business rules
  - Copy-never-link rule
  - Full editability after copy
  - History retention rules
  - Multi-SKU explosion rules
  - Master data governance (no auto-create, approval queue)

- [ ] **T1.5:** Define tenant hierarchy
  - Tenant → Customer → Quotation relationship
  - Multi-tenant isolation rules
  - RBAC definitions (admin, estimator, reviewer, viewer)

- [ ] **T1.6:** Document master data import governance
  - Approval queue workflow
  - Canonical resolver rules
  - Import validation rules

- [ ] **T1.7:** Create `NSW_DATA_DICTIONARY_v1.0.md` (FROZEN)
  - All entity definitions
  - All relationships
  - All naming conventions
  - All business rules
  - Approval and freeze

**Deliverable:** `NSW_DATA_DICTIONARY_v1.0.md` (FROZEN)

---

#### Task Group 2: Schema Design (Step 2)

**Duration:** 2-3 weeks  
**Prerequisite:** Step 1 complete and approved

- [ ] **T2.1:** Translate data dictionary to table structure
  - Review SPEC-5 DDL as starting point
  - Validate against data dictionary
  - Resolve schema clarifications (Customer FK, parent_line_id, etc.)

- [ ] **T2.2:** Design tenant + auth tables
  - `tenants`, `users`, `roles`, `user_roles`
  - `audit_log` table structure
  - Indexes for performance

- [ ] **T2.3:** Design master data (CIM) tables
  - `categories`, `subcategories`, `types`
  - `attributes`, `type_attributes`
  - `makes`, `series`
  - `products` (Generic/Specific with constraints)
  - `product_attribute_values`

- [ ] **T2.4:** Design pricing tables
  - `price_lists`
  - `prices` (effective dating)
  - `import_batches`
  - `import_approval_queue`

- [ ] **T2.5:** Design template (MBOM) tables
  - `master_boms`
  - `master_bom_items` (L0/L1 only, no product_id)
  - Constraints and validation rules

- [ ] **T2.6:** Design estimation workspace (QUO) tables
  - `customers` (design per business standard - separate discussion)
  - `quotations` (customer_name text field for now, can be FK later)
  - `quote_panels`
  - `quote_boms` (BOM groups, Feeder = BOM group, support parent-child BOM hierarchy)
  - `quote_bom_items` (with resolution_level L0/L1/L2, parent_line_id if needed, support nested BOMs)
  - `quote_bom_item_history`

- [ ] **T2.7:** Design optional tables
  - `cost_heads` (recommended)
  - `ai_call_logs` (future-ready)

- [ ] **T2.8:** Define all constraints
  - Primary keys
  - Foreign keys
  - Unique constraints
  - Check constraints (e.g., Generic vs Specific product_type rules)
  - Indexes for performance

- [ ] **T2.9:** Create ER Diagram
  - Visual representation of all tables
  - Show relationships and cardinality
  - Export in multiple formats (PNG, PDF, draw.io)

- [ ] **T2.10:** Generate table inventory
  - Excel/CSV format
  - All tables, columns, data types
  - Constraints summary
  - Module ownership mapping

- [ ] **T2.11:** Create seed script (design validation artifact)
  - Review SPEC-5 seed script as reference
  - Create seed script SQL that demonstrates:
    - Tenant + user + roles setup
    - Customer entity (if using FK)
    - Complete CIM hierarchy (Category → SubCategory → Type → Attributes)
    - Products (Generic L1 + Specific L2 with relationships)
    - Price lists and prices (effective dating)
    - Master BOM template (L0/L1 items, no ProductId)
    - Sample quotation workspace (Panel → BOM group → L2 resolved items)
  - Validate seed script against schema design (proves relationships work)
  - Document seed script as design artifact (not for execution in Phase 5)
  - Include in `NSW_SCHEMA_CANON_v1.0.md` as appendix or separate file

- [ ] **T2.12:** Create `NSW_SCHEMA_CANON_v1.0.md` (FROZEN)
  - Complete DDL (ready-to-run SQL)
  - Column definitions with business meaning
  - Relationship documentation
  - Constraints documentation
  - Seed script (design validation artifact, not for execution)
  - Approval and freeze

**Deliverables:**
- `NSW_SCHEMA_CANON_v1.0.md` (FROZEN)
- ER Diagram (PNG/PDF)
- Table Inventory (Excel/CSV)
- Seed Script (design validation artifact, SQL format)

---

#### Task Group 3: Planning Artifacts (Reference for Post-Phase 5)

**Duration:** 1 week (optional, can proceed in parallel)  
**Status:** Planning reference, not Phase 5 deliverable

- [ ] **T3.1:** Document API surface design
  - Review SPEC-5 API endpoints
  - Validate against schema
  - Document request/response formats
  - Create `NSW_API_DESIGN_v1.0.md` (draft)

- [ ] **T3.2:** Document UI wireframe logic
  - Review SPEC-5 UI navigation and wireframes
  - Validate against data model
  - Document user flows
  - Create `NSW_UI_DESIGN_v1.0.md` (draft)

- [ ] **T3.3:** Document technical architecture
  - NS Ware structure format (ADR)
  - Tech stack decisions (FastAPI, React, Postgres, NATS)
  - Module boundaries
  - Integration patterns
  - Create `NSW_TECHNICAL_ARCHITECTURE_v1.0.md` (draft)

- [ ] **T3.4:** Document CI/CD and deployment strategy (planning artifact)
  - Review SPEC-5 CI/CD pipeline proposal
  - Document environment strategy (local → staging → prod)
  - Document schema deployment approach (forward-only migrations)
  - Document database migration strategy
  - Create `NSW_DEPLOYMENT_STRATEGY_v1.0.md` (draft)

**Deliverables:** Planning reference documents (not frozen, can evolve)

**Note:** These planning artifacts have now been completed and are included in SPEC-5 v1.0:
- ✅ API contracts (OpenAPI) - Complete
- ✅ Role & permission matrix - Complete  
- ✅ UI handoff spec (Figma-ready) - Complete
- ✅ API response examples (JSON) - Complete

---

### Post-Phase 5 Tasks (Implementation - Reference Only)

**Note:** These are out of Phase 5 scope but listed here for planning reference.

#### Task Group 4: Infrastructure Setup

- [ ] **T4.1:** Repository structure
  - Monorepo setup (`/backend`, `/frontend`, `/infra`)
  - Version control configuration
  - Directory structure per NS Ware format

- [ ] **T4.2:** Docker Compose setup
  - Review SPEC-5 docker-compose proposal
  - Create docker-compose.yml for local development
  - Services: Postgres, NATS JetStream, FastAPI backend, React frontend
  - Environment configuration
  - Network setup
  - Volume mounts for development

- [ ] **T4.3:** Database setup
  - Postgres container configuration
  - Migration system (Alembic or similar)
  - Database initialization scripts
  - Use seed script from Phase 5 Step 2 (design artifact) as development fixture

- [ ] **T4.4:** Message queue setup
  - NATS JetStream container
  - Queue configuration
  - Stream configuration
  - Worker process setup

- [ ] **T4.5:** One-command local run
  - Create startup script (e.g., `./start-local.sh`)
  - Document local development setup process
  - Verify all services start correctly
  - Test connectivity between services
  - Verify auto-run DB init (schema + seed) on first boot

- [ ] **T4.6:** CI/CD pipeline setup (GitHub Actions)
  - Review SPEC-5 CI/CD pipeline plan
  - Create GitHub Actions workflows
  - Pipeline stages: lint → test → build → deploy
  - Environment-specific workflows (staging, production)
  - Database migration pipeline (forward-only)
  - Container registry setup (Docker Hub, GHCR, etc.)
  - Secrets management (GitHub Secrets)

- [ ] **T4.7:** Environment configuration
  - Local environment (docker-compose)
  - Staging environment (cloud deployment)
  - Production environment (cloud deployment)
  - Environment variable management
  - Configuration per environment (.env files, config maps)

---

#### Task Group 5: Backend Implementation

- [ ] **T5.1:** FastAPI project scaffold
  - Module structure (Auth, CIM, MBOM, QUO, Workers)
  - Dependency injection
  - Settings and configuration
  - Logging and observability

- [ ] **T5.2:** Authentication & Authorization
  - JWT token implementation
  - Tenant-aware middleware
  - RBAC implementation

- [ ] **T5.3:** Master Data (CIM) APIs
  - Category/SubCategory/Type CRUD
  - Product CRUD (Generic/Specific)
  - Import pipeline
  - Approval queue APIs

- [ ] **T5.4:** Template (MBOM) APIs
  - Master BOM CRUD
  - Master BOM items CRUD (L0/L1 only)
  - Apply template endpoint

- [ ] **T5.5:** Estimation Workspace (QUO) APIs
  - Quotation CRUD
  - Panel/BOM/item management
  - Pricing and discounting
  - History tracking

- [ ] **T5.6:** Workers (NATS)
  - Import processing worker
  - L1→L2 explosion worker
  - Recalculation worker
  - Audit trail worker

---

#### Task Group 6: Frontend Implementation

- [ ] **T6.1:** React project setup
  - TypeScript configuration
  - Component library
  - State management
  - Routing

- [ ] **T6.2:** Masters UI
  - Category/SubCategory/Type management
  - Product management (Generic/Specific tabs)
  - Price list management
  - Import & approval queue

- [ ] **T6.3:** Templates UI
  - Master BOM list
  - Master BOM editor (L0/L1 only)

- [ ] **T6.4:** Quotation Workspace UI
  - Quotation list
  - Panel tree
  - BOM groups
  - Item table editor
  - Cost summary

---

#### Task Group 7: Testing & Quality

- [ ] **T7.1:** Unit tests
  - Backend service tests
  - Frontend component tests
  - Test fixtures and mocks

- [ ] **T7.2:** Integration tests
  - API integration tests
  - Database integration tests
  - End-to-end workflows

- [ ] **T7.3:** CI/CD pipeline integration
  - Integrate unit tests into CI pipeline
  - Integrate integration tests into CI pipeline
  - Test coverage reporting
  - Quality gates enforcement

---

## 📊 Conflict Register

### Discovered Semantic Collisions

| Conflict | SPEC-5 Position | Existing Position | Resolution |
|----------|----------------|-------------------|------------|
| **Phase 5 scope** | Includes implementation (Phase 5a/5b) | Analysis-only (Step 1/2) | **RESOLVED:** SPEC-5 is planning doc spanning Phase 5 (analysis) + Post-Phase 5 (implementation). Phase 5a/5b should be renamed to Post-Phase 5 milestones. |
| **Customer table** | DDL includes `customers` table + `quotations.customer_name` text field | Business standard definition needed | **RESOLVED:** Separate business discussion during Phase 5. Current approach acceptable as placeholder. |
| **Resolution level** | SPEC-5 schema needs verification | L0/L1/L2 should be supported at ALL levels | **RESOLVED:** All BOM items (master and quote) should support L0/L1/L2. Schema must be updated to include resolution_level in quote_bom_items. |
| **BOM hierarchy (nested BOMs)** | Parent-child BOM relationships | Any BOM can be parent, any can be child | **RESOLVED:** Support hierarchical BOMs where BOMs can contain other BOMs. Same BOM can be parent in one context, child in another. |
| **Parent-child linkage** | `metadata_json` or `parent_line_id` | Not in schema yet | **PENDING:** Decide on approach for multi-SKU explosion linkage. |
| **NS Ware format** | Technical stack selection (FastAPI, Postgres, NATS, React) | Use same technical services | **RESOLVED:** No ADR needed. Just use same technical stack/services from NS Ware project. |
| **Seed script scope** | Included in SPEC-5 with full fixture data | Not explicitly in Phase 5 scope | **RESOLVED:** Use seed script as design validation artifact in Step 2 (proves schema supports real-world data). Not for execution in Phase 5. |
| **Docker-compose setup** | Proposed for local development | Not in Phase 5 scope | **RESOLVED:** Defer to Post-Phase 5 implementation. Useful planning reference but not Phase 5 deliverable. |
| **CI/CD pipeline design** | Proposed GitHub Actions pipeline | Not in Phase 5 scope | **RESOLVED:** Document high-level CI/CD strategy and environment approach in Phase 5 Step 2 as planning artifact. Actual implementation deferred to Post-Phase 5. |
| **Phase 5 Requirements Integration** | SPEC-5 may not include all fields from PENDING_UPGRADES_INTEGRATION.md | Phase 5 must consider all pending upgrades | **CRITICAL GAP:** Must verify SPEC-5 schema includes BOM tracking fields, CostHead system, IsLocked fields, Validation Guardrails G1-G7, module ownership, naming conventions. |

---

## 🎯 Recommendations

### Immediate Actions

1. **Clarify Phase 5 Scope**
   - Keep Phase 5 as analysis-only (Step 1: Data Dictionary, Step 2: Schema Design)
   - Use SPEC-5 as planning reference, not Phase 5 execution spec
   - Rename Phase 5a/5b to Post-Phase 5 implementation phases

2. **Resolve Technical Clarifications**
   - ✅ NS Ware: No ADR needed - use same technical services (FastAPI, Postgres, NATS, React)
   - ✅ Customer table: Separate business discussion during Phase 5 (current approach acceptable)
   - ✅ Resolution levels: All BOM items support L0/L1/L2 at all levels
   - ✅ BOM hierarchy: Support nested BOMs (any BOM can be parent or child)
   - ⚠️ Parent-child linkage: Decide on approach for multi-SKU explosion linkage (T2.6)

3. **Use SPEC-5 Selectively**
   - **Phase 5 inputs:** Entity definitions, schema DDL, business rules, seed script (as design artifact)
   - **Post-Phase 5 reference:** API design, UI wireframes, tech stack, docker-compose setup
   - **Do not execute** implementation tasks in Phase 5

4. **Seed Script as Design Validation**
   - Include seed script SQL in Phase 5 Step 2 as design artifact
   - Use to validate schema relationships and constraints
   - Not for database execution in Phase 5 (analysis-only)
   - Will be used in Post-Phase 5 as development fixture

5. **CI/CD & Deployment Strategy as Planning Artifact**
   - Document high-level CI/CD strategy in Phase 5 Step 2
   - Document environment approach (local → staging → prod)
   - Document schema deployment strategy (forward-only migrations)
   - Actual pipeline implementation deferred to Post-Phase 5
   - Useful for validating migration strategy fits schema design

### Phase 5 Execution Order

```
1. Phase 4 Exit (prerequisite)
   ↓
2. Phase 5 Step 1: Data Dictionary
   ├─> T1.1: Review SPEC-5 entities
   ├─> T1.2: Document technical stack selection (FastAPI, Postgres, NATS, React)
   ├─> T1.3: Finalize entity semantics (including BOM hierarchy and resolution levels)
   ├─> T1.4: Define business rules
   ├─> T1.5: Define tenant hierarchy
   ├─> T1.6: Document import governance
   └─> T1.7: Create NSW_DATA_DICTIONARY_v1.0.md (FROZEN)
   ↓
3. Phase 5 Step 2: Schema Design
   ├─> T2.1: Translate to tables
   ├─> T2.2-T2.7: Design all table groups
   ├─> T2.8: Define constraints
   ├─> T2.9: Create ER Diagram
   ├─> T2.10: Generate table inventory
   ├─> T2.11: Create seed script (design validation artifact)
   └─> T2.12: Create NSW_SCHEMA_CANON_v1.0.md (FROZEN)
   ↓
4. Phase 5 Complete
   ↓
5. Post-Phase 5 Implementation (separate project)
   └─> Use SPEC-5 as implementation roadmap
```

---

## ✅ Next Steps

### Immediate Actions (Before Freezing SPEC-5 v1.0)

1. **⚠️ CRITICAL: Verify SPEC-5 against Phase 5 Requirements**
   - [ ] **MANDATORY:** Cross-check SPEC-5 schema DDL against `PHASE_5_PENDING_UPGRADES_INTEGRATION.md`
   - [ ] **MANDATORY:** Verify BOM tracking fields are included (origin_master_bom_id, instance_sequence_no, is_modified, etc.)
   - [ ] **MANDATORY:** Verify CostHead table and FKs are included
   - [ ] **MANDATORY:** Verify IsLocked fields are included
   - [ ] **MANDATORY:** Verify Validation Guardrails G1-G7 are documented as business rules
   - [ ] **MANDATORY:** Verify AI tables (ai_call_logs) are included
   - [ ] **MANDATORY:** Verify module ownership is defined
   - [ ] **MANDATORY:** Verify naming conventions are defined

2. **Review SPEC-5 completeness**
   - ✅ UX logic complete
   - ⚠️ DB DDL complete (but needs verification against Phase 5 requirements)
   - ✅ Seed data complete
   - ✅ Local run setup complete
   - ✅ CI/CD pipeline complete

3. **Resolve remaining technical clarifications**
   - [ ] NS Ware structure format (ADR needed?)
   - [ ] Customer table design (FK vs text field in quotations)
   - [ ] Resolution level in quote_bom_items (L2 only or allow L0/L1)
   - [ ] Parent-child linkage approach (parent_line_id vs metadata_json)

3. **Decision: Freeze SPEC-5 v1.0**
   - ✅ **ALL OPTIONAL COMPONENTS ADDED:** OpenAPI contracts, Role & permission matrix, UI handoff spec, API response examples
   - ✅ **SPEC-5 v1.0 is COMPLETE and execution-ready**
   - ✅ **RECOMMENDATION: FREEZE SPEC-5 v1.0 NOW** and hand to implementation team
   - Optional next steps: ZIP handover checklist or contractor execution plan (week-by-week)

### For Review

1. **Review this document** with stakeholders
2. **Review SPEC-5 v1.0** completeness and alignment
3. **Resolve clarifications** (NS Ware format, Customer FK, resolution levels, etc.)
4. **Approve Phase 5 scope** (analysis-only, Step 1/2 only)
5. **Approve SPEC-5 v1.0** for use as planning document

### For Execution (After Approval)

1. **Wait for Phase 4 exit criteria**
2. **Begin Phase 5 Step 1** (Data Dictionary)
3. **Use SPEC-5 v1.0 selectively** (entity definitions, schema design, seed script as design artifact)
4. **Create frozen deliverables** (Data Dictionary v1.0, Schema Canon v1.0)
5. **Reference SPEC-5 v1.0** throughout Phase 5 execution

---

**Document Status:** ✅ READY FOR FREEZING - SPEC-5 v1.0 Complete & Execution-Ready  
**Last Updated:** 2025-01-27  
**Owner:** Phase 5 Governance Team  
**Review Required By:** Architecture, Execution Team, Stakeholders

---

## 🎯 SPEC-5 v1.0 Freezing Recommendation

### Status: ⚠️ FREEZE GATED ON COMPLIANCE VERIFICATION

**Critical:** SPEC-5 v1.0 is execution-ready but **CANNOT be frozen** until compliance verification is complete.

**All Components Complete:**
- ✅ Core components (UX, DB DDL, Seed, Local Run, CI/CD)
- ✅ OpenAPI contracts (screen-driven)
- ✅ Role & permission matrix (MVP)
- ✅ UI handoff spec (Figma-ready)
- ✅ API response examples (top 10 MVP endpoints)

**What SPEC-5 v1.0 Provides:**
- ✅ **No ambiguity for developers** - API ↔ UI contract is explicit
- ✅ **Fast UI build** - React devs can mock immediately
- ✅ **Clean stakeholder review** - Easy to read, business-oriented
- ✅ **Execution-ready** - Complete end-to-end specification

**Recommended Next Steps (Execution Sequence):**

### Step A: Freeze Scope Vocabulary (1-2 hours)
- [ ] Lock naming: Phase-5 = Step-1 Data Dictionary + Step-2 Schema Canon
- [ ] Replace "Phase-5a/5b" with Post-Phase-5 Milestones:
  - M1: Local Dev Pack
  - M2: Cloud/Staging Pack
- ✅ Outcome: No confusion in governance or reporting

### Step B: Complete Mandatory Verification (THE FREEZE GATE)
- [ ] Use `SPEC_5_FREEZE_GATE_CHECKLIST.md` compliance matrix
- [ ] Verify all items in compliance matrix
- [ ] Patch SPEC-5 with missing governance sections
- [ ] Lock 3 design decisions (Multi-SKU, Customer, Resolution levels)
- ✅ Outcome: SPEC-5 v1.0 can be frozen without future rework

### Step C: Lock Design Decisions
1. **Multi-SKU linkage:** Use `parent_line_id` (grouping) + `metadata_json` (flexibility)
2. **Customer normalization:** `customer_name` (text, snapshot) + `customer_id` (optional FK, forward-compatible)
3. **Resolution levels:** L0/L1/L2 allowed at all levels with explicit constraints:
   - MBOM: L0/L1/L2 if product_id rules respected
   - QUO: L0/L1/L2 if pricing + locking rules respected
- ✅ Outcome: Step-2 Schema Canon can be frozen cleanly

### Step D: Freeze SPEC-5 v1.0
- [ ] Freeze `NSW_DATA_DICTIONARY_v1.0.md`
- [ ] Freeze `NSW_SCHEMA_CANON_v1.0.md`
- [ ] Handover to implementation team for Phase 5 execution

### Step E: Post-Freeze (Phase 5 Execution)
- [ ] Phase-5 Step 1: Data Dictionary (use SPEC-5 as reference)
- [ ] Phase-5 Step 2: Schema Design (use SPEC-5 as reference)
- [ ] Post-Phase-5: Implementation (FastAPI/React/Docker/CI as execution plan)

**Before Freezing - Mandatory Verification:**

**🚨 FREEZE GATE:** Use `SPEC_5_FREEZE_GATE_CHECKLIST.md` compliance matrix

1. [ ] **Complete compliance matrix verification** (all items marked ✅)
2. [ ] **Patch SPEC-5 with missing governance sections:**
   - [ ] Validation Guardrails G1-G7 (explicit documentation)
   - [ ] Module Ownership Matrix (all tables mapped)
   - [ ] Naming Conventions (all standards documented)
   - [ ] IsLocked scope declaration (explicit coverage)
   - [ ] CostHead resolution order (precedence rules)
   - [ ] AI scope declaration (schema reservation vs implementation)
3. [ ] **Lock 3 design decisions:**
   - [ ] Multi-SKU linkage: `parent_line_id` + `metadata_json` (both)
   - [ ] Customer normalization: `customer_name` (text) + `customer_id` (optional FK)
   - [ ] Resolution levels: L0/L1/L2 at all levels with explicit constraints
4. [ ] **Verify schema DDL includes:**
   - [ ] All BOM tracking fields (origin_master_bom_id, instance_sequence_no, is_modified, etc.)
   - [ ] IsLocked fields (scope decided and documented)
   - [ ] CostHead system (table + FKs)
   - [ ] AI tables (ai_call_logs, etc.)
5. [ ] **Stakeholder sign-off** on freeze gate criteria

**Reference:** See `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` for detailed compliance matrix.

---

---

## ⚠️ Critical Gap Analysis: SPEC-5 vs Phase 5 Requirements

### Gap Check: Pending Upgrades Integration

**Reference:** `docs/PHASE_5/02_FREEZE_GATE/PHASE_5_PENDING_UPGRADES_INTEGRATION.md` requires all pending upgrades to be considered during Phase 5.

| Required Component | SPEC-5 Status | Phase 5 Requirement | Gap? |
|-------------------|---------------|---------------------|------|
| **BOM Tracking Fields** | ⚠️ **NEEDS VERIFICATION** | `origin_master_bom_id`, `instance_sequence_no`, `is_modified`, `modified_by`, `modified_at` in `quote_boms` | ⚠️ **VERIFY IN SPEC-5** |
| **Validation Guardrails (G1-G7)** | ⚠️ **NOT EXPLICITLY DOCUMENTED** | Must be documented as business rules in Data Dictionary | ⚠️ **GAP** |
| **CostHead System** | ✅ Mentioned as "optional but recommended" | `cost_heads` table + `cost_head_id` FK in `quote_bom_items` | ⚠️ **NEEDS VERIFICATION** |
| **AI Entities** | ✅ Mentioned (`ai_call_logs`) | `ai_call_logs` table + related AI tables | ✅ **COVERED** |
| **IsLocked Fields** | ⚠️ **NOT EXPLICITLY MENTIONED** | `is_locked` on quotation tables for deletion policy | ⚠️ **GAP** |
| **Audit Trail** | ✅ Mentioned (`audit_log` table) | Audit logging requirements | ✅ **COVERED** |
| **Module Ownership** | ⚠️ **NOT EXPLICITLY DOCUMENTED** | Must define which module owns which table | ⚠️ **GAP** |
| **Naming Conventions** | ⚠️ **NOT EXPLICITLY DOCUMENTED** | Must establish naming conventions | ⚠️ **GAP** |

**Action Required:**
1. [ ] **Verify BOM tracking fields** are in SPEC-5 schema DDL
2. [ ] **Verify CostHead table and FKs** are in SPEC-5 schema DDL  
3. [ ] **Verify IsLocked fields** are in SPEC-5 schema DDL
4. [ ] **Add Validation Guardrails (G1-G7)** to SPEC-5 business rules section
5. [ ] **Add Module Ownership** mapping to SPEC-5
6. [ ] **Add Naming Conventions** section to SPEC-5

---

## 📋 SPEC-5 v1.0 Components Summary

### Core Deliverables (Complete)

1. **UX Logic & Navigation**
   - UI Navigation structure (Masters → Templates → Quotations)
   - UI Wireframe Logic (textual descriptions)
   - Global UX principles
   - Screen-by-screen layout and actions

2. **Database Schema (DDL)**
   - Complete Postgres schema
   - All tables with columns, types, constraints
   - Foreign key relationships
   - Indexes for performance
   - Multi-tenant design (tenant_id on all tables)

3. **Seed Script**
   - Complete development fixture
   - Tenant + users + roles setup
   - CIM masters (category → subcategory → type → attributes)
   - Products (Generic L1 + Specific L2)
   - Price lists and prices
   - Master BOM template (L0/L1 items)
   - Sample quotation workspace (L2 resolved items)

4. **Local Development Setup**
   - docker-compose.yml (Postgres + NATS + FastAPI + React)
   - Auto-run DB init (schema + seed on first boot)
   - Backend + Frontend Dockerfiles
   - One-command run: `docker compose up -d --build`

5. **CI/CD Pipeline**
   - GitHub Actions workflows
   - CI on PRs (backend tests + frontend build)
   - Auto-deploy to staging on main branch
   - Manual-gated production deploy
   - Docker-based deployments (same artifacts everywhere)
   - Forward-only database migrations strategy
   - Observability hooks (/healthz, /readyz, logs, NATS monitor)

### All Components Complete ✅

**Previously Optional Components (Now Included in v1.0):**
- ✅ API contracts (OpenAPI specs per screen) - **ADDED**
- ✅ Role & permission matrix (detailed RBAC definitions) - **ADDED**
- ✅ UI design handoff (Figma-ready specifications) - **ADDED**
- ✅ API response examples (JSON for top 10 MVP endpoints) - **ADDED**

**SPEC-5 v1.0 is now complete with all components. Ready for freezing and handover.**

