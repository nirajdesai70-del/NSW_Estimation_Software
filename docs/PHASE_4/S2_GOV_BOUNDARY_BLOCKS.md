# S2 GOV-002 — Module Boundary Blocks

**Task ID:** NSW-P4-S2-GOV-002  
**Gate:** G3  
**Risk:** HIGH  
**Status:** ACTIVE  
**Rule:** Planning-only. No behavior change.

---

## 1️⃣ Purpose

Lock **who may call whom** during Phase-4 to prevent:
- Silent coupling
- PROTECTED scope leakage
- Accidental QUO-V2 contamination

These blocks are **enforced from S2 onward**.

---

## 2️⃣ Global Enforcement Rules

- ❌ **No module may call another module's PROTECTED services/models directly**
- ❌ **No cross-module DB access**
- ✅ **Only documented HTTP routes or contracts are allowed**
- ❌ **No new COMPAT endpoints without decision log + retirement plan**

---

## 3️⃣ Module Boundary Blocks (Authoritative)

---

### 🔒 SHARED

**Allowed:**
- Expose read-only contracts:
  - CatalogLookupContract
  - ReuseSearchContract
- Adapter access to CIM data (read-only)

**Forbidden:**
- Direct DB reads/writes
- Direct calls to QUO services
- Business logic mutation

---

### 🔒 CIM (Component / Item Master)

**Allowed:**
- Catalog CRUD
- Import/export (CIM scope)
- Serve catalog data via SHARED contracts

**Forbidden:**
- Calling QUO services/models
- Calling Costing / Quantity logic
- Reading Settings table directly

**Integration:**
- Must consume:
  - CatalogLookupContract
  - PdfContainSettingsContract (if needed)

---

### 🔒 MASTER

**Allowed:**
- Organization / Vendor reference CRUD
- PDF container management
- Read-only reference exposure

**Forbidden:**
- Business logic execution
- Costing / quantity logic
- Direct access to CIM internals

---

### 🔒 EMP (Employee / Role)

**Allowed:**
- Role/user reference lookups
- Auth middleware usage

**Forbidden:**
- Owning pricing logic
- Shadow role caches
- Writing cross-module state

---

### 🔒 MBOM (Master BOM)

**Allowed:**
- Master BOM template CRUD
- Expose read/apply contracts

**Forbidden:**
- Writing quotation data directly
- Calling QUO costing services
- Direct catalog DB access

**Integration:**
- Must consume:
  - CatalogLookupContract
  - QUO apply endpoints (wrapper-only)

---

### 🔒 FEED (Feeder Library)

**Allowed:**
- Feeder template CRUD
- Expose apply contract

**Forbidden:**
- Writing quotation structures directly
- Direct catalog DB access

**Integration:**
- Must use:
  - CatalogLookupContract
  - QUO apply endpoints (wrapper-only)

---

### 🔒 PBOM (Proposal BOM)

**Allowed:**
- Proposal BOM reuse/search
- Apply via QUO wrapper

**Forbidden:**
- Writing quotation BOM trees directly
- Costing/quantity logic

---

### 🔒 QUO (Legacy + V2)

**Allowed:**
- Own quotation lifecycle
- Own costing and quantity logic
- Expose apply endpoints

**Forbidden:**
- Being called directly by other modules' services
- Any modification without G4 for PROTECTED areas

**Special Rule:**
- V2 core = **WRAPPER ONLY**
- No direct reuse of CostingService or QuantityService

---

## 4️⃣ Enforcement Rule

Any cross-module call **not listed above is INVALID**.

Violations require:
- Decision Log entry
- Explicit gate approval
- Retirement plan

---

## 5️⃣ Evidence

**Authority References:**
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- Execution Context: `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`
- Exception Mapping: `docs/PHASE_4/S2_GOV_EXCEPTION_TASK_MAPPING.md`
- Execution Checklist: `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md`

---

## 6️⃣ Exit Criteria (G3)

- ✅ All module blocks documented
- ✅ No ambiguity in allowed/forbidden calls
- ✅ Referenced by MBOM/FEED/PBOM isolation docs

---

**Task Status:** ✅ Complete  
**Next Task:** NSW-P4-S2-MBOM-001 (MBOM interface contract)

