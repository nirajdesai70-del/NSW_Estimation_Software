# Track A — RETAIN Register (Global)

**Version:** 1.0  
**Status:** 🔒 ACTIVE  
**Purpose:** Central register of all RETAIN-tagged business decisions across all Phase-5 builds  
**Owner:** Development Team

---

## Purpose

This register tracks all **RETAIN** business decisions (blocking items) identified across all builds to:
- Prevent rediscovering the same decisions repeatedly
- Provide a reference for new builds
- Track implementation status across the system
- Support audit and governance

---

## RETAIN Decisions Register

| # | Business Decision | Decision Source | First Identified | Build Where Required | Implementation Status | Owner |
|---|-------------------|-----------------|------------------|---------------------|----------------------|-------|
| 1 | Idempotent import behavior | Legacy catalog import | Generic Catalog Importer | Generic Catalog Importer | ⬜ PENDING / ✅ IMPLEMENTED | [Owner] |
| 2 | WEF / effective_from date handling | Legacy pricing | Generic Catalog Importer | Generic Catalog Importer, Pricing Engine | ⬜ PENDING / ✅ IMPLEMENTED | [Owner] |
| 3 | Error logging + import batch traceability | Legacy import logs | Generic Catalog Importer | Generic Catalog Importer | ⬜ PENDING / ✅ IMPLEMENTED | [Owner] |
| 4 | Safe partial success (continue on non-fatal errors) | Legacy import behavior | Generic Catalog Importer | Generic Catalog Importer | ⬜ PENDING / ✅ IMPLEMENTED | [Owner] |
| 5 | Deterministic mapping rules (no silent overwrites) | Legacy import rules | Generic Catalog Importer | Generic Catalog Importer | ⬜ PENDING / ✅ IMPLEMENTED | [Owner] |
| 6 | Quotation numbering generation rules | Legacy quotation system | [Future build] | Quotation Core | ⬜ PENDING | [Owner] |
| 7 | Price list precedence logic | Legacy pricing rules | [Future build] | Pricing Engine | ⬜ PENDING | [Owner] |
| 8 | Locking and unlock authority | Legacy locking rules | [Future build] | Locking Module | ⬜ PENDING | [Owner] |
| 9 | Audit trail requirements | Legacy audit logs | [Future build] | Audit Module | ⬜ PENDING | [Owner] |
| 10 | Discount governance rules | Legacy discount logic | [Future build] | Pricing Engine | ⬜ PENDING | [Owner] |

---

## How to Use This Register

### When Starting a New Build

1. **Check this register first** - See if any RETAIN decisions are already identified for your build area
2. **Reference existing RETAIN items** - If a RETAIN decision applies to your build, reference it in your worksheet
3. **Add new RETAIN items** - If you discover a new RETAIN decision, add it here and mark it for your build

### When Completing a Build

1. **Update Implementation Status** - Mark RETAIN items as ✅ IMPLEMENTED when complete
2. **Update Owner** - Assign or confirm owner for tracking
3. **Cross-reference** - Link to implementation evidence (API, code, config)

### Benefits

- ✅ **Avoid rework** - Don't rediscover the same RETAIN decisions
- ✅ **Consistency** - Same RETAIN decisions applied consistently across builds
- ✅ **Tracking** - See implementation status at a glance
- ✅ **Audit** - Central reference for governance reviews

---

## RETAIN Decision Categories

### Catalog & Import (Builds: Generic Catalog Importer, etc.)
- Idempotent import behavior
- WEF / effective_from handling
- Error logging + batch traceability
- Safe partial success
- Deterministic mapping rules

### Quotation & Commercial (Builds: Quotation Core, etc.)
- Quotation numbering generation
- Panel/feeder/BOM conceptual flow
- Quotation lifecycle expectations

### Pricing (Builds: Pricing Engine, etc.)
- Price list precedence logic
- WEF date usage
- Discount governance rules
- Price source priority

### Control & Locking (Builds: Locking Module, etc.)
- When locking applies
- Who can lock/unlock
- Approval intent

### Audit & Compliance (Builds: Audit Module, etc.)
- User action auditability
- Traceability expectations
- Change tracking requirements

---

## Adding New RETAIN Items

When you identify a new RETAIN decision:

1. **Add to register** with:
   - Clear business decision description
   - Decision source (email/meeting/SOP/screen/contract)
   - First build where identified
   - Builds where it applies
   - Initial status (PENDING)
   - Owner assignment

2. **Reference in build worksheet** - Link to this register item #

3. **Update when implemented** - Change status to IMPLEMENTED and add evidence reference

---

## Maintenance

**Review Frequency:** Monthly or after major build completion  
**Update Responsibility:** Development Team Lead  
**Version Control:** Track additions via git commits

---

## Notes

- This register is **cumulative** - items remain even after implementation
- **Status tracking** helps identify cross-build dependencies
- **Owner assignment** ensures accountability
- **Decision source** supports audit and governance

---

**Last Updated:** 2026-01-03  
**Total RETAIN Items:** 10 (5 identified, 5 placeholder for future builds)

