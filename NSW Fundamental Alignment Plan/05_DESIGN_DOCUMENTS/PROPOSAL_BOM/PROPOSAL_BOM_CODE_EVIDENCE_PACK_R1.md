# Code Evidence Pack — Proposal BOM (Cursor Extract)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md  
**Version:** v1.0_2025-12-19  
**Date (IST):** 2025-12-19  
**Evidence Type:** Code snippets (no DB)  
**Repo/Branch:** nish / unknown-branch (pending confirmation)

---

## Purpose

This document contains code snippets extracted from the codebase to verify implementation against Proposal BOM design specifications. Each snippet is mapped to specific gaps in the Gap Register (PB-GAP-001 through PB-GAP-004).

---

## CE-01 — Copy from Master BOM (applyMasterBom / applyFeederTemplate)
**Gap Reference:** PB-GAP-001, PB-GAP-002  
**File:** app/Http/Controllers/QuotationV2Controller.php  
**Method(s):** applyMasterBom() and applyFeederTemplate() (actual copy-from-master implementation)  
**Design Reference:** `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Copy step sets ProductId from Master BOM item (generic) in create-from-master flow

**Status:** ❌ FAIL (Specific-only not enforced; generic may persist)

**Code Evidence Findings:**
- `applyMasterBom()`: Creates QuotationSaleBomItem records with ProductId copied directly from MasterBomItem (generic products allowed). Sets MakeId=0, SeriesId=0. No forced conversion to ProductType=2.
- `applyFeederTemplate()`: Copies ProductId from template items without enforcing ProductType=2.
- `applyProposalBom()`: Copies items from another BOM without enforcing specific-only rule.
- `addItem()`: Validates product exists but does not enforce ProductType=2. MakeId/SeriesId default to 0.

**Conclusion:** The "Specific products only" rule exists in design docs, but current implementation does not enforce it consistently on key write paths. Generic products can persist as final state (Status=0) without forced conversion to specific.

**Code snippet:** (copy loops from applyMasterBom() and applyFeederTemplate() - code already verified via chat on 2025-12-19)

---

## CE-02 — Add Item to Proposal BOM (addItem)
**Gap Reference:** PB-GAP-002  
**File:** app/Http/Controllers/QuotationV2Controller.php (or relevant controller/service)  
**Method:** addItem(...)  
**Design Reference:** `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — "Specific products only" rule enforcement

**Status:** ⚠️ FINDING CONFIRMED (snippet pending insertion)

**Evidence source:** Method pasted in chat on 2025-12-19 (QuotationV2Controller::addItem)

**Code Evidence Findings:**
- `addItem()` validates that product exists but does not enforce ProductType=2 (Specific products only).
- MakeId and SeriesId are allowed to default to 0.
- Therefore it reinforces PB-GAP-002 = FAIL (Code) and also contributes to PB-GAP-001 risk (generic products can persist as final state).

**Conclusion:** The "Specific products only" rule is not enforced in the addItem() write path. Generic products can be added and persist with MakeId/SeriesId = 0, violating the design requirement.

**Action:** Paste snippet into CE-02 to convert status to ❌ VERIFIED (FAIL).

**Code snippet:**

```php
// addItem() method from QuotationV2Controller.php
// [Code snippet to be pasted here - validates product exists but does not enforce ProductType=2]
```

---

## CE-03 — Update Make/Series (updateMakeSeries / Product Resolution)
**Gap Reference:** PB-GAP-001, PB-GAP-002  
**File:** app/Http/Controllers/QuotationController.php (and related controllers)  
**Method:** changemakeseries(), MakeSeriesChange(), getItemDescription() (ad-hoc resolution logic)  
**Design Reference:** `PROPOSAL_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md` — Master Data flow: copy generic → user selects Make/Series → update to specific → price load

**Status:** ❌ VERIFIED (FAIL)

**Code Evidence Findings:**
- **No dedicated ProductResolutionService exists.** Generic → Specific conversion is implemented ad-hoc inside controller methods.
- Resolution logic appears in multiple controller methods:
  - `changemakeseries()` — handles Make/Series updates
  - `MakeSeriesChange()` — alternative Make/Series change handler
  - `getItemDescription()` — resolves GenericId + MakeId + SeriesId to specific product
- Pattern observed: `Product::where('GenericId', $ProductId)->where('MakeId', $MakeId)->where('SeriesId', $SeriesId)`
- **Enforcement is partial and UI-driven:** ProductType=2 check exists in API methods (e.g., `getItemDescription()`) but is NOT enforced as a mandatory write-path rule when saving QuotationSaleBomItem.
- **No centralized validation:** No service enforces "generic → specific conversion" as a required step before persistence.

**Conclusion:** No centralized product resolution service exists. Generic → Specific conversion is implemented ad-hoc inside controller methods and is not enforced as a mandatory write-path rule. Therefore, generic persistence is not just possible — it is structurally allowed. This confirms PB-GAP-001 and PB-GAP-002: generic products can persist as final state without forced conversion to specific.

**Code snippet:**

```php
// Resolution pattern found in controller methods (scattered, not centralized):
// Product::where('GenericId', $ProductId)
//     ->where('MakeId', $MakeId)
//     ->where('SeriesId', $SeriesId)
//     ->where('ProductType', 2) // Only in API methods, not write paths
//     ->first();
```

---

## CE-04 — Quantity Chain (QuotationQuantityService::calculate)
**Gap Reference:** PB-GAP-003  
**File:** app/Services/QuotationQuantityService.php  
**Method:** calculate(...)  
**Design Reference:** `PROPOSAL_BOM_BACKEND_DESIGN_PART9_LOGIC.md` — Quantity chain logic walks up to Level 0 (feeder) for roll-up calculations

**Paste snippet:** (feeder discovery + bomQtyChain multiplication + effQty)

**Status:** ✅ VERIFIED (Code pasted into chat on 2025-12-19)
**Finding:** QuantityService treats Level 1 with no parent as feeder-equivalent (legacy). Feeder discovery treats Level 0 as feeder, OR Level 1 with no parent as feeder ("legacy data"). Quantity chain multiplication excludes the feeder itself and multiplies only higher-level BOM qtys (Level ≥ 1, excluding feeder).

**Code behavior:**
- Feeder discovery: `Level == 0` OR (`Level == 1` AND `ParentBomId == NULL`) treated as feeder
- Quantity chain: Excludes feeder itself, multiplies only higher-level BOM quantities
- Result: "Level-1 under Panel" is supported only as legacy feeder-equivalent, not as normal BOM1-under-panel case

**Code snippet:**

**Note:** `fallbackToPanelOnly()` exists and is referenced for "no BOM relationship" cases; not pasted here (optional).

```php
public function calculate(QuotationSaleBomItem $item): array
{
    $itemId = $item->QuotationSaleBomItemId;

    // Check per-item cache (not instance-level)
    if (isset($this->effectiveQtyCache[$itemId])) {
        return $this->effectiveQtyCache[$itemId];
    }

    $itemQty = (float) ($item->Qty ?? 0);
    if ($itemQty <= 0) {
        return $this->effectiveQtyCache[$itemId] = $this->emptyResult();
    }

    // Load BOM relationship if not already loaded
    $bom = $item->bom;
    if (!$bom && $item->QuotationSaleBomId) {
        $bom = $item->bom()->first();
    }

    if (!$bom) {
        return $this->effectiveQtyCache[$itemId] = $this->fallbackToPanelOnly($item, $itemQty);
    }

    // Walk up chain to collect BOM qtys (Level >= 1) and find feeder (Level 0 or 1)
    // Note: Some legacy data has Level=1 for feeders, so we handle both
    $bomQtyChain = [];
    $currentBom  = $bom;
    $feeder      = null;
    $feederQty   = 1.0;

    // First, try to find feeder by walking up the chain
    $tempBom = $bom;
    while ($tempBom) {
        // Feeder is Level 0, or Level 1 if it has no parent (legacy data)
        if ($tempBom->Level !== null) {
            if ((int)$tempBom->Level === 0) {
                $feeder = $tempBom;
                break;
            } elseif ((int)$tempBom->Level === 1 && !$tempBom->parentBom) {
                // Legacy: Level 1 with no parent might be a feeder
                $feeder = $tempBom;
                break;
            }
        }
        $tempBom = $tempBom->parentBom;
    }

    // If no feeder found, check if current BOM itself is a feeder
    if (!$feeder && $bom->Level !== null) {
        if ((int)$bom->Level === 0 || ((int)$bom->Level === 1 && !$bom->parentBom)) {
            $feeder = $bom;
        }
    }

    // Now walk up to collect BOM quantities (Level >= 1, but not the feeder)
    while ($currentBom) {
        if ($currentBom->Level !== null && (int)$currentBom->Level >= 1) {
            // Only add to chain if it's not the feeder
            if ($currentBom !== $feeder) {
                $bomQty = (float) ($currentBom->Qty ?? 1);
                if ($bomQty <= 0) {
                    return $this->effectiveQtyCache[$itemId] = $this->emptyResult();
                }
                $bomQtyChain[] = $bomQty;
            }
        }
        $currentBom = $currentBom->parentBom;
    }

    // Get feeder quantity
    if ($feeder) {
        $feederQty = (float) ($feeder->Qty ?? 1);
        if ($feederQty <= 0) {
            return $this->effectiveQtyCache[$itemId] = $this->emptyResult();
        }
    }

    // Load panel relationship if not already loaded
    $panel = $item->quotationSale;
    if (!$panel && $item->QuotationSaleId) {
        $panel = $item->quotationSale()->first();
    }
    $panelQty = (float) ($panel->Qty ?? 1);
    if ($panelQty <= 0) {
        return $this->effectiveQtyCache[$itemId] = $this->emptyResult();
    }

    $bomQtyProduct = empty($bomQtyChain) ? 1.0 : array_product($bomQtyChain);
    $perPanelQty   = $feederQty * $bomQtyProduct * $itemQty;
    $totalQty      = $panelQty * $perPanelQty;

    return $this->effectiveQtyCache[$itemId] = [
        'component_qty'           => $itemQty,
        'bom_qty_chain'           => $bomQtyChain,
        'bom_qty_product'         => $bomQtyProduct,
        'feeder_qty'              => $feederQty,
        'panel_qty'               => $panelQty,
        'effective_qty_per_panel' => $perPanelQty,
        'effective_qty_total'     => $totalQty,
        // Legacy aliases
        'base_qty'                => $itemQty,
        'per_panel_qty'           => $perPanelQty,
        'total_qty'               => $totalQty,
        'breakdown' => [
            'PanelQty'  => $panelQty,
            'FeederQty' => $feederQty,
            'BomQty'    => $bomQtyProduct,
            'ItemQty'   => $itemQty,
        ],
    ];
}
```

---

## Verification Status (To be filled after code review)

| Code Evidence | PB-GAP | Status | Notes |
|---|---|---|---|
| CE-01 | PB-GAP-001, PB-GAP-002 | ❌ VERIFIED (FAIL) | Specific-only not enforced; generic may persist. Copy flows (applyMasterBom/applyFeederTemplate) do not force ProductType=2. |
| CE-02 | PB-GAP-002 | ⚠️ FINDING CONFIRMED | Finding confirmed: No ProductType=2 enforcement; MakeId/SeriesId default to 0. Snippet pending insertion to convert to VERIFIED (FAIL). Not required for closure (PB-GAP-002 already FAIL via CE-01 + CE-03). |
| CE-03 | PB-GAP-001, PB-GAP-002 | ❌ VERIFIED (FAIL) | No centralized ProductResolutionService exists; conversion logic is ad-hoc in controllers; enforcement is partial and UI-driven. Generic persistence is structurally allowed. |
| CE-04 | PB-GAP-003 | ✅ VERIFIED | Code supports legacy feeder (Level 1 with no parent). Spec contradiction needs correction. |

---

## DB Verification Pack — COMPLETED

**Owner:** DB/Backend engineer  
**Status:** ✅ VERIFIED (PASS) — Proposal BOM cleared for freeze on DB axis

**Results:**

### DB-Check B1 — Active items with ProductType=1 (CRITICAL)
**Query:** Active Proposal BOM items (Status=0) where ProductType=1 (Generic)  
**Result:** ✅ 0 rows (no active ProductType=1 items)  
**Conclusion:** No generic items exist in Proposal BOM data today.

### DB-Check B2 — ProductType=2 missing MakeId/SeriesId (CRITICAL)
**Query:** Active Proposal BOM items (Status=0) where ProductType=2 (Specific) but MakeId=0 OR SeriesId=0  
**Result:** ✅ 0 rows (no ProductType=2 items missing MakeId/SeriesId)  
**Conclusion:** No missing Make/Series in Proposal BOM today.

**Final Status:** Proposal BOM is cleared for freeze on DB axis. Code Evidence still shows enforcement gaps (CE-01/CE-03 FAIL), but not causing Proposal BOM DB violations today. Code enforcement improvements remain recommended but are non-blocking for Proposal BOM freeze.

---

## Change Log

| Version | Date (IST) | Change |
|---|---|---|
| v1.0_2025-12-19 | 2025-12-19 | Created Code Evidence Pack template for Round-1 verification |

