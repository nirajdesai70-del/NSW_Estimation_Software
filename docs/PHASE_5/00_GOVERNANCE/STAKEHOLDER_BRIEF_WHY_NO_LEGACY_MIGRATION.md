# NSW Data Strategy — Why Legacy Data Was Not Migrated

**Date:** 2025-12-18  
**Audience:** Management, stakeholders, auditors, implementation partners  
**Decision Status:** Approved / Frozen  
**Related Docs:** 
- `docs/PHASE_5/00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md`
- `docs/PHASE_5/00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md`
- `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md`

---

## The Core Issue

Legacy data contains inconsistent and unreliable meaning due to historical item creation practices:

- **Categories/subcategories/items/products were often created on-the-fly** during imports and runtime operations
- **Same business meaning exists under multiple names/IDs** (e.g., "Panel" vs "Panels" vs "Electrical Panel")
- **Imports and edits produced duplicate masters and semantic drift** over time
- **Some relationships rely on defaults like 0 instead of valid references** (data quality issues)

This makes legacy data **unsafe to treat as canonical truth**.

---

## Why Migrating Legacy Data Would Harm NSW

If we migrate legacy data as-is, we **permanently embed legacy mistakes** into NSW:

- The new system inherits wrong categorization rules
- Clean reporting and costing become unreliable
- Cleanup becomes endless and higher-cost than building clean masters
- Future automation (ML, analytics, standard catalogs) becomes brittle

**In short: migration would compromise the product.**

---

## What We Are Doing Instead

NSW will be built on a **clean canonical master structure**:

### Master Data Creation Rules

- **Master data is created only via controlled admin/UI pathways** (no runtime auto-creation)
- **Imports must reference existing approved masters** (no "create if missing")
- **Unknown masters go to a review/approval queue** (no silent creation)
- **Schema enforces referential integrity and uniqueness** (no FK=0, no duplicates)

### Legacy Archive

Legacy remains available as a **read-only archive** for reference. Historical data can be consulted, but does not contaminate NSW canonical structure.

---

## Business Impact

### Benefits

- **NSW master data becomes trusted and consistent** - No semantic drift, no duplicates
- **Faster long-term operations** - Less rework, fewer support issues
- **Better quality costing, BOM integrity, and future integrations** - Clean data enables reliable automation
- **Audit-ready traceability** - Every master creation and import decision is logged and reviewable

### Trade-off

- **Initial data onboarding requires admin approval steps** for unknown masters

This is **intentional to protect correctness**. The approval queue ensures semantic quality from day one.

---

## If Legacy Continuity Is Needed Later

Legacy migration can still happen as a **separate governed project**, after NSW canonical schema is frozen:

1. **Extract legacy schema** + assess quality
2. **Decide scope** (none/partial/active-only)
3. **Use staging + transformation rules** (never direct import)
4. **Import only what passes validation**

But it will **not block NSW go-live**.

---

## Final Statement

**We did not migrate legacy data because it would pollute NSW canonical meaning.**

NSW is being built as a **clean product with enforceable rules**, not as a patch on top of legacy semantics.

This decision:
- Protects NSW from historical data quality issues
- Enables reliable automation and reporting
- Provides audit-ready governance
- Allows optional legacy migration later (if needed) via controlled, validated pathways

---

## Questions & Answers

**Q: Won't this slow down initial data entry?**  
A: Yes, intentionally. The approval queue ensures semantic correctness. Once masters are established, imports proceed quickly.

**Q: What if we need historical quotations?**  
A: Legacy database remains read-only for reference. Historical data can be consulted without contaminating NSW.

**Q: Can we migrate legacy data later?**  
A: Yes, as a separate governed project. After NSW schema is frozen, we can assess legacy quality and import only validated data via staging pipeline.

**Q: How do we prevent the same mistakes in NSW?**  
A: Database constraints, code review rules, and governance policies prevent runtime auto-creation. See `NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md` for full rules.

---

**Document Status:** Approved / Frozen  
**Last Updated:** 2025-12-18  
**Owner:** Phase 5 Governance Team

