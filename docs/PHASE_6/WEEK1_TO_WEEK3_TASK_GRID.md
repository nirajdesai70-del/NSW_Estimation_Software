# Week-1 to Week-3 Task Grid (Track-wise)

**Date:** 2026-01-XX  
**Status:** 📋 Planning  
**Objective:** Track-wise task grid with acceptance criteria for Weeks 1-3

---

## Week-1 (Stabilize + Wire Real Data)

### Track A — Core Quotation UI

**A1.1** — Replace placeholder quotation list with GET /quotations (or stub endpoint returning DB rows).  
**AC:** UI list shows IDs 2/3/4 from DB; no hardcoded list.

**A1.2** — Quotation detail uses GET /quotations/{id}.  
**AC:** Quote_no/customer/status match DB.

**A1.3** — Panel list uses GET /quotations/{id}/panels.  
**AC:** Panel names reflect DB (including "PANEL-1 (EDITED)" for qid=4).

**A1.4** — Feeder list uses GET /quotations/{id}/panels/{panelId}/feeders (level=0 boms).  
**AC:** Only level=0 displayed.

**A1.5** — BOM items uses GET /quotations/{id}/boms/{bomId}/items.  
**AC:** Items count matches DB.

---

### Track E — Canon Enforcement

**E1.1** — Startup check logs resolved DATABASE_URL and rejects SQLite.  
**AC:** On startup, logs show postgresql+psycopg://…; if sqlite detected, app refuses to boot in Phase-6 mode.

**E1.2** — Add a "Canon drift check" script (schema diff against snapshot).  
**AC:** One command outputs PASS/FAIL; no auto-migrations.

---

### Track C — Ops Readiness (Lite)

**C1.1** — Add "request_id" propagation to all logs (already middleware exists).  
**AC:** every request has request_id in logs.

---

## Week-2 (Reuse Parity + Editable Copy UX)

### Track A-R — Reuse & Legacy Parity

**AR2.1** — Add UI actions: Copy quotation / Copy panel / Copy feeder / Copy BOM.  
**AC:** returns new IDs; navigates to copied entity.

**AR2.2** — Reuse invariants test pack (manual checklist + 3 automated API tests).  
**AC:** proves: no shared IDs + tracking fields correct + edit preserved.

**AR2.3** — Tracking fields visible (read-only debug widget in dev).  
**AC:** shows instance_sequence_no, is_modified, origin_master_bom_id.

---

### Track A — UX Minimum

**A2.1** — Loading/error states for all 5 screens.  
**AC:** no blank screens; errors show request_id.

---

## Week-3 (Costing Foundations Start + Catalog Tooling Activation)

### Track D0 — QCD/QCA Foundations

**D0.3.1** — Implement upsert_cost_adder (ON CONFLICT) with validator.  
**AC:** Can add/update cost head for a panel; uniqueness preserved.

**D0.3.2** — Read-only "quotation cost head summary API" (no UI).  
**AC:** returns one line per cost head per panel (as per rule doc).

**D0.3.3** — Fabrication special rule stub: FAB → MATERIAL bucket mapping in summary output.  
**AC:** JSON output shows fabrication rolled into MATERIAL for quotation view.

---

### Track B — Catalog Tooling

**B3.1** — Define "pilot category" import path (even one make/series).  
**AC:** one SKU and one price record flows into system; BOM line can resolve to SKU later.

---

**Status:** Planning complete — proceed to Week-1 execution checklist.