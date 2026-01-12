# Gate-0 Template Readiness Evidence

**Purpose:** Store Gate-0 template data readiness verification evidence for BOM-GAP-013.

**Rule:** Do not execute apply verification unless selected TEMPLATE_ID has items.

---

## Filename Format

**Format:** `TEMPLATE_<TEMPLATE_ID>_count.txt`

**Example:** `TEMPLATE_123_count.txt` (for MasterBomId=123)

---

## Required SQL Evidence

Each file must contain the output of:

```sql
SELECT COUNT(*) AS item_count FROM master_bom_items WHERE MasterBomId = <TEMPLATE_ID>;
```

**Alternative format (equivalent):**
```sql
SELECT <TEMPLATE_ID> AS template_id, COUNT(*) AS item_count
FROM master_bom_items
WHERE MasterBomId = <TEMPLATE_ID>;
```

**Requirement:** item_count must be > 0

---

## File Structure

Each `TEMPLATE_<ID>_count.txt` file should contain:

```
Template ID: <TEMPLATE_ID>
Item Count: <item_count>
Verification Date: <YYYY-MM-DD>
Verified By: <owner/module>
Status: PASS / FAIL
```

---

## Evidence Location

- **Gate-0 output:** `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/TEMPLATE_<ID>_count.txt`
- **R1 response:** inserted_count = N (must match item_count from Gate-0)
- **S1/S2 snapshots:** `docs/PHASE_4/evidence/GAP/BOM-GAP-013/`

---

**Authority:** GAP_GATEBOARD.md Section 4  
**Last Updated:** 2025-12-18

