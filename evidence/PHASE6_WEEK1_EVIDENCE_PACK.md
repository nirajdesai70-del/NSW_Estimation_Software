# Phase-6 — Week-1 Evidence Pack

**Project:** NSW Estimation Software  
**Phase:** Phase-6  
**Week:** Week-1  
**Prepared By:** (fill)  
**Date:** (fill)  
**Status:** ✅ COMPLETE (Schema Canon Setup)

---

## 1) Locked Invariants (Do Not Break)

- Copy-never-link
- QCD/QCA separation (Cost summary reads QCA only)
- No costing breakup in quotation view (summary-only)
- Fabrication remains summary-only
- Schema canon frozen (Phase-6)
- All changes are additive + read-only

---

## 2) Week-1 Deliverables Summary

### Schema Canon Setup
- ✅ Database setup from Schema Canon
- ✅ Schema canon drift detection
- ✅ Canon validation setup

### Key Achievements
- Schema canon frozen for Phase 6
- Database foundation established
- Drift detection mechanism in place

---

## 3) Commands Executed (Copy/Paste)

### Schema Canon Setup
```bash
# Database setup from Schema Canon
# [Commands to be filled]

# Schema drift check
./scripts/check_schema_drift.sh
```

---

## 4) Output Evidence (paste latest run output)

```
[Output to be filled]
```

---

## 5) Schema Canon Validation

### Database Tables Verified
- ✅ `quote_bom_items` - tenant_id NOT NULL
- ✅ `quote_boms` - tenant_id NOT NULL
- ✅ `quote_panels` - tenant_id NOT NULL

### Indexes Verified
- ✅ `quote_cost_adders_pkey`
- ✅ `uq_qca_panel_costhead`

---

## 6) Notes / Deviations

- Schema canon frozen for Phase 6
- All future changes must be additive and read-only

---

## 7) Commit Hash Placeholders

- Week-1 Day-1: (fill)
- Week-1 Day-2: (fill)
- Week-1 Day-3: (fill)
- Week-1 Day-4: (fill)

---

**Status:** ✅ COMPLETE  
**Next Week:** Week-2 (TBD)
