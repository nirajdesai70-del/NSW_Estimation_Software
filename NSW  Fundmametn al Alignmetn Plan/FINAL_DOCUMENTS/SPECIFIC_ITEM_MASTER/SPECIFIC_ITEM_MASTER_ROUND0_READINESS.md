# Specific Item Master — Round-0 Readiness Checklist

**Purpose:**  
Ensure Specific Item Master review starts only after Generic Item Master is frozen.

---

## Pre-Conditions (ALL REQUIRED)

| Check | Required | Status |
|-----|---------|--------|
| Generic Item Master Round-2 APPROVED | YES | ☐ |
| ProductResolutionService enforces L2 rules | YES | ☐ |
| ProductArchiveService active | YES | ☐ |
| Phase-8 SKU Governance frozen | YES | ☐ |
| EX-SUBCAT-001 acknowledged | YES | ☐ |

If any item unchecked → **Specific Item Master review MUST NOT START**

---

## Scope Confirmation

Specific Item Master review will cover:
- ProductType=2 only
- L2 identity (Make + SKU + SkuType)
- Phase-8 SKU governance
- Pricing + quotation usage
- Archival behavior

Generic Item Master is **out of scope**.

---

## Authorization to Start Round-1

When all above are ✔:

> **Specific Item Master — Round-1 is authorized to begin.**

---

## Gap Revalidation (Phase-3)

**Purpose:** Re-classify any gaps/findings with L0-L1-L2 layer context after Phase-3 Rule Compliance Review.

| Finding ID | Original Classification | Layer Label | Re-classification | Reason | Status |
|------------|------------------------|-------------|-------------------|--------|--------|
| SI-GAP-001 | Dependency (MB-GAP-002) | Cross-Layer | ✅ Close | Specific Item Master plan registered; dependency satisfied (tracked in Master BOM Gap Register) | CLOSED |

**Re-classification Legend:**
- ✅ **Close:** Gap was terminology-caused or dependency resolved
- 🔁 **Reword:** Gap needs layer context added to description
- ❌ **Keep:** True violation remains, not terminology-related

**Layer Label Legend:**
- **L0:** Generic Item Master (Functional Family)
- **L1:** Master BOM (Technical Variant, Make-agnostic)
- **L2:** Specific Item Master (Catalog Item with Make+Series+SKU) — **operates at L2 layer**
- **Proposal-Resolution:** L1 → L2 resolution process
- **Cross-Layer:** Affects multiple layers

**Notes:**
- SI-GAP-001: Specific Item Master plan dependency (MB-GAP-002) was resolved. Specific Item Master operates at L2 layer and is plan-recorded (detailed design complete).
- Specific Item Master Round-0 Readiness is a checklist, not a gap register. Gaps related to Specific Item Master are tracked in Master BOM Gap Register (MB-GAP-002).

**Phase-3 Status:** No gaps in this document (readiness checklist only). Specific Item Master operates at L2 layer.

---

## Change Log

| Version | Date (IST) | Change |
|--------|------------|--------|
| v1.0 | 2025-12-18 | Initial readiness gate |
| v1.1 | 2025-12-19 | Phase-3: Added Gap Revalidation section; confirmed L2 layer operation |

---

**END OF DOCUMENT**

