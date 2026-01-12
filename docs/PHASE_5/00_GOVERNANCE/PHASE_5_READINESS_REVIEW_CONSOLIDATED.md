# Phase-5 Readiness Review — Consolidated Status

**Date:** 2025-01-27  
**Status:** Pre-Freeze Verification  
**Context:** TfNSW Estimation Software Framework — Canonical Estimation Platform Build

---

## 🎯 Phase-5 Definition (Locked)

**Context:** NSW = Transport for NSW (TfNSW) Estimation Software Framework

**Phase 5 = Canonical Estimation Platform Build (New Truth Layer)**

- **Strategic rebuild phase** establishing clean, authoritative estimation system
- **Encodes TfNSW-compliant estimation logic** in software
- **Removes legacy contamination** and ambiguity
- **Serves as future baseline** for change estimates, lifecycle validation, governance reviews

**Primary Objective:** **D. Change / variation estimation for live systems**
- New scope
- Design changes
- Make/series substitutions
- Add-ons / exclusions
- Repricing under governance

**Secondary Objective:** **B. Whole-of-life cost validation (derived)**
- Comparison against earlier estimates
- Drift analysis
- Baseline vs current delta

**Out of Scope for Phase 5:**
- ❌ Pure operations forecasting
- ❌ Benefits realisation analytics
- ❌ General BI/analytics

---

## ✅ Confirmed & Locked Items (Do Not Change)

### Core Semantics (TfNSW-Aligned)

✅ **Master BOM: L0/L1 only, ProductId = NULL**
- Templates contain generic placeholders only
- No resolved products in Master BOM
- **Locked** — No backtracking

✅ **Copy-Never-Link Rule**
- Applying Master BOM creates independent instances
- Changes to Master BOM don't affect existing quotations
- **Locked** — Core governance rule

✅ **Full Editability + History**
- All line items remain editable after copy
- History snapshots retained
- **Locked** — Audit requirement

✅ **Multi-SKU Explosion (First-Class)**
- Single user intent can expand to multiple purchasable SKUs
- ACB + UV/OV add-ons supported
- Expansion results in multiple line items
- **Locked** — Business requirement

✅ **Resolution Levels: L0/L1/L2 at All Levels**
- Master BOM items: L0/L1/L2 supported (with product_id rules)
- Quotation BOM items: L0/L1/L2 supported (with pricing + locking rules)
- BOM hierarchy (parent/child) is orthogonal to resolution levels
- **Locked** — Architecture decision

✅ **Feeder = BOM Group**
- No separate "feeder" entity
- Feeder is just a BOM group
- Panel-level items represented as default BOM group (e.g., "PANEL_ITEMS")
- **Locked** — Normalized design

✅ **Multi-Tenant Design**
- Tenant isolation (data + auth boundary)
- Tenant → Customer → Quotation hierarchy
- RBAC: admin, estimator, reviewer/approver, viewer
- **Locked** — Security requirement

✅ **Master Data Governance**
- No-auto-create masters rule
- Import approval queue
- Canonical resolver rules
- **Locked** — Data quality requirement

### Technical Stack (NS Ware Services)

✅ **FastAPI + Postgres + NATS JetStream + React**
- Modular monolith, microservice-ready later
- Docker-based deployment
- CI/CD pipeline (GitHub Actions)
- **Locked** — Technical foundation

### New Build Approach

✅ **Phase 5 = New DB + New Masters + New Logic**
- No legacy dependency
- No migration required
- Clean canonical definitions
- **Locked** — Strategic decision

---

## 🔒 Explicit Do-Not-Touch Rules

1. **Never resolve ProductId in Master BOM items** (G1 Guardrail)
2. **Always copy, never link** Master BOM to quotations
3. **Always retain history** on all edits
4. **Never auto-create masters** from imports
5. **Always enforce tenant isolation** on all queries
6. **Never allow destructive schema changes** (forward-only migrations)
7. **Always validate guardrails G1-G7** (business rules enforcement)

---

## 🟡 Open Items (MUST Resolve Before Coding)

### Critical (Freeze Gate Requirements)

🟡 **1. Validation Guardrails G1-G7 Documentation**
- **Status:** Must be explicitly documented in Data Dictionary
- **Action:** Add "Canonical Validation Guardrails" section
- **Location:** Data Dictionary Step 1
- **Blocking:** Yes — cannot freeze without this

🟡 **2. Module Ownership Matrix**
- **Status:** Must map all tables to owner modules
- **Action:** Create ownership matrix (Auth / CIM / MBOM / QUO / PRICING / AUDIT / AI)
- **Location:** Data Dictionary Step 1
- **Blocking:** Yes — contractor handoff requirement

🟡 **3. Naming Conventions**
- **Status:** Must document all naming standards
- **Action:** Create naming conventions section (tables, columns, FKs, enums, timestamps, IDs)
- **Location:** Data Dictionary Step 1
- **Blocking:** Yes — contractor handoff requirement

🟡 **4. BOM Tracking Fields Verification**
- **Status:** Must verify schema includes: origin_master_bom_id, instance_sequence_no, is_modified, modified_by, modified_at
- **Action:** Verify in SPEC-5 schema DDL
- **Location:** Schema Design Step 2
- **Blocking:** Yes — governance requirement

🟡 **5. IsLocked Scope Declaration**
- **Status:** Must explicitly declare IsLocked coverage
- **Decision Required:** Line-item only OR all quotation levels?
- **Action:** Document decision in Data Dictionary
- **Location:** Data Dictionary Step 1
- **Blocking:** Yes — prevents contractor confusion

🟡 **6. CostHead Resolution Order**
- **Status:** Must document precedence rules
- **Action:** Document: item override → product default → system default
- **Location:** Data Dictionary Step 1
- **Blocking:** Yes — business rule requirement

🟡 **7. AI Scope Declaration**
- **Status:** Must label AI tables as schema reservation vs implementation
- **Action:** Declare: Phase-5 = schema reservation, Post-Phase-5 = implementation
- **Location:** Data Dictionary Step 1
- **Blocking:** Yes — scope clarity

### Design Decisions (Lock Before Schema Freeze)

🟡 **8. Multi-SKU Linkage Strategy**
- **Recommendation:** Use both `parent_line_id` (grouping) + `metadata_json` (flexibility)
- **Status:** Decision needed
- **Blocking:** Yes — affects schema DDL

🟡 **9. Customer Normalization**
- **Recommendation:** `customer_name` (text, snapshot) + `customer_id` (optional FK, nullable)
- **Status:** Decision needed (per business standard discussion)
- **Blocking:** Yes — affects schema DDL

🟡 **10. Resolution Level Constraints**
- **Recommendation:** L0/L1/L2 at all levels with explicit rules:
  - MBOM: L0/L1/L2 if product_id rules respected
  - QUO: L0/L1/L2 if pricing + locking rules respected
- **Status:** Decision needed
- **Blocking:** Yes — affects schema DDL

---

## ❌ Out-of-Scope Items for Phase 5

### Implementation Work (Post-Phase-5)

❌ **Code implementation** (FastAPI, React, workers)
❌ **Database creation** (actual DB setup)
❌ **UI implementation** (React components)
❌ **Runtime testing** (functional testing)
❌ **Performance testing**
❌ **Deployment** (local, staging, production)

### Legacy Work (Separate Project)

❌ **Legacy DB schema extraction**
❌ **Legacy data quality assessment**
❌ **Legacy → NSW mapping matrices**
❌ **Data migration scripts**
❌ **Legacy data import**

### Analytics & Reporting (Post-Phase-5)

❌ **Operations forecasting** (pure ops)
❌ **Benefits realisation analytics**
❌ **General BI/analytics**
❌ **Advanced reporting**

---

## 📋 Freeze Gate Checklist

**SPEC-5 v1.0 CANNOT be frozen until ALL items below are ✅ Complete:**

- [ ] ✅ Validation Guardrails G1-G7 explicitly documented
- [ ] ✅ Module Ownership Matrix complete (all tables mapped)
- [ ] ✅ Naming Conventions documented (all standards)
- [ ] ✅ BOM tracking fields verified in schema DDL
- [ ] ✅ IsLocked scope explicitly declared
- [ ] ✅ CostHead resolution order documented
- [ ] ✅ AI scope explicitly declared
- [ ] ✅ Multi-SKU linkage strategy locked (parent_line_id + metadata_json)
- [ ] ✅ Customer normalization approach locked (customer_name + optional customer_id)
- [ ] ✅ Resolution level constraints locked (L0/L1/L2 rules explicit)

**Reference:** See `SPEC_5_FREEZE_GATE_CHECKLIST.md` for detailed compliance matrix.

---

## ✅ Phase-5 Execution Readiness

### Ready to Start: Phase-5 Step 1 (Data Dictionary)

**What can begin immediately:**
- ✅ Entity definitions
- ✅ Relationship semantics
- ✅ Business rules documentation
- ✅ Naming conventions establishment
- ✅ Module ownership mapping

### Gated: Phase-5 Step 2 (Schema Design)

**What requires Step 1 completion:**
- Schema DDL finalization
- Constraint definitions
- ER diagram creation
- Table inventory generation

### Blocked: SPEC-5 v1.0 Freeze

**What requires freeze gate completion:**
- Freezing Data Dictionary v1.0
- Freezing Schema Canon v1.0
- Contractor handoff

---

## 🎯 Next Actions

1. **Immediate:** Complete freeze gate checklist (all 10 items)
2. **Parallel:** Begin Phase-5 Step 1 (Data Dictionary) — can proceed while verification completes
3. **After Freeze Gate:** Freeze SPEC-5 v1.0 and proceed to Step 2
4. **Post-Freeze:** Handover to implementation team for Post-Phase-5 milestones

---

**Document Status:** ✅ Ready for Approval  
**Approval Required:** Architecture, Execution Team, Stakeholders  
**Next Step:** Complete freeze gate checklist → Freeze SPEC-5 v1.0

