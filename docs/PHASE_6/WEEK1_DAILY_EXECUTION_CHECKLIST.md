# Week-1 Daily Execution Checklist

**Date:** 2026-01-XX  
**Status:** 📋 Execution Ready  
**Objective:** Day-by-day, track-wise execution with clear acceptance criteria

**Scope:** Replace UI placeholders with real data, stabilize reuse, enforce canon  
**Rule:** No new features. No schema changes. No costing UI.

---

## 🟢 DAY-1 — Backend Read APIs (Truth First)

### 🎯 Objective

Expose read-only APIs so UI can stop guessing and start reflecting DB truth.

---

### Track A — Core Read APIs

**A1.1** — GET /quotations

**Action:**
- Implement list quotations (tenant-scoped)
- Fields: id, quote_no, customer_name, status, created_at

**Acceptance:**
- Returns IDs 2 / 3 / 4 (existing data)
- Order deterministic (created_at DESC or id ASC)

**Must NOT:**
- Add filters beyond tenant
- Add pagination yet

---

**A1.2** — GET /quotations/{id}

**Action:**
- Fetch single quotation (tenant-safe)

**Acceptance:**
- quote_no, customer_name, status match DB
- 404 if wrong tenant or id

**Must NOT:**
- Compute pricing
- Join cost adders

---

### Track E — Canon Enforcement

**E1.1** — SQLite Guard (Startup Check)

**Action:**
- On startup, log resolved DATABASE_URL
- If URL starts with sqlite, raise RuntimeError

**Acceptance:**
- App refuses to start on SQLite

**Why:**
- Prevent silent regression (what we just debugged)

---

### Day-1 Exit Gate

✅ UI placeholders can now be replaced with /quotations  
❌ No write APIs touched

---

## 🟢 DAY-2 — Panel & Feeder Read APIs

### 🎯 Objective

Complete the Quotation → Panel → Feeder read chain.

---

### Track A — Structure APIs

**A2.1** — GET /quotations/{id}/panels

**Action:**
- Return panels for quotation

**Acceptance:**
- For qid=4 → returns panel "PANEL-1 (EDITED)"

**Must NOT:**
- Allow updates
- Join BOM items

---

**A2.2** — GET /quotations/{id}/panels/{panelId}/feeders

**Action:**
- Return level=0 BOMs only

**Acceptance:**
- Only feeders returned
- No child BOMs included

**Canon Rule:**
- Feeder = quote_boms.level = 0

---

### Track A — UI Wiring

**A2.3** — Replace placeholder panels/feeders

**Action:**
- Remove hardcoded arrays in:
  - QuotationDetail.tsx
  - PanelFeeders.tsx

**Acceptance:**
- UI reflects DB edits (edited panel name shows)

---

### Day-2 Exit Gate

✅ Quotation → Panel → Feeder path is fully DB-driven  
❌ No BOM items yet

---

## 🟡 DAY-3 — BOM Item Read + Reuse Hooks

### 🎯 Objective

Finish read path and prepare reuse UI actions (no new copy logic).

---

### Track A — BOM APIs

**A3.1** — GET /quotations/{id}/boms/{bomId}/items

**Action:**
- Fetch BOM items (tenant-safe)

**Acceptance:**
- Items count = 2 (matches DB)
- Fields: product_id/make/category, qty, rate, amount

**Must NOT:**
- Modify pricing
- Add cost heads

---

### Track A-R — Reuse UI Hooks

**AR3.1** — UI buttons (no new backend)

**Action:**
- Add buttons:
  - Copy Quotation
  - Copy Panel
  - Copy Feeder

**Acceptance:**
- Buttons call existing APIs
- Redirects to new IDs

---

### Day-3 Exit Gate

✅ Full read path live  
✅ Reuse actions visible  
❌ No edits yet

---

## 🟡 DAY-4 — Reuse Parity Verification (UI-Driven)

### 🎯 Objective

Ensure reuse behaves identically via UI, not just curl.

---

### Track A-R — Reuse Validation

**AR4.1** — Copy quotation via UI

**Action:**
- Copy quotation ID 4

**Acceptance:**
- New quotation opens
- Panels/BOMs/items exist
- Editable (rename panel)

---

**AR4.2** — Edit after copy

**Action:**
- Rename panel in copied quotation

**Acceptance:**
- Source quotation unchanged
- Copied quotation updated

---

### Track E — Invariant Check

**E4.1** — Invariants (manual DB check)

**Verify:**
- No shared IDs between source & copy
- instance_sequence_no=1
- is_modified=false

---

### Day-4 Exit Gate

✅ UI reuse = API reuse  
✅ Editability preserved

---

## 🔴 DAY-5 — Stabilisation & Week-1 Sign-off

### 🎯 Objective

Freeze Week-1 and prepare for controlled expansion.

---

### Track C — Ops & Hygiene

**C5.1** — Error handling & loading states

**Action:**
- Add loading + error UI to all pages

**Acceptance:**
- No blank screens
- Errors show request_id

---

### Track E — Canon Drift Check

**E5.2** — Schema drift script

**Action:**
- Script: compare live DB schema vs snapshot

**Acceptance:**
- Outputs PASS
- No auto-fix

---

### Week-1 Closure Criteria

- ✅ UI fully DB-driven
- ✅ Reuse parity proven via UI
- ✅ No canon drift
- ✅ No costing leakage

---

## 🧭 Week-1 Output Artifacts

By end of Week-1 you must have:

- Working UI (no placeholders)
- Stable read APIs
- Reuse verified via UI
- Canon guardrails active

---

## 5R — Week-1 Snapshot

**Results:** UI now reflects truth  
**Risks:** UI–API mismatch (mitigated by strict ACs)  
**Rules:** Read-only first, reuse next  
**Roadmap:** Week-2 = controlled enhancements  
**References:** Week-0 gates + Canon lock

---

**Week-1 Execution Ready** ✅