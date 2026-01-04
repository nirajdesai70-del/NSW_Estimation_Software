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
| 7 | Price list precedence logic | Legacy pricing rules | Phase 5 Task 5.1 | Pricing Engine | ✅ IMPLEMENTED | Phase 5 Team |
| 8 | Locking and unlock authority | Legacy locking rules | [Future build] | Locking Module | ⬜ PENDING | [Owner] |
| 9 | Audit trail requirements | Legacy audit logs | Phase 5 Task 5.1 | Audit Module | ✅ IMPLEMENTED | Phase 5 Team |
| 10 | Discount governance rules | Legacy discount logic | Phase 5 Task 5.1 | Pricing Engine | ✅ IMPLEMENTED | Phase 5 Team |
| 11 | Manual override requires authorization | Legacy pricing rules | Phase 5 Task 5.1 | Pricing Engine | ✅ IMPLEMENTED | Phase 5 Team |
| 12 | Tax calculation with CGST/SGST/IGST split | Legacy tax rules | Phase 5 Task 5.1 | Tax Engine | ✅ IMPLEMENTED | Phase 5 Team |
| 13 | Preview before apply (safe calculation) | Legacy quotation workflow | Phase 5 Task 5.1 | Quotation API | ✅ IMPLEMENTED | Phase 5 Team |
| 14 | Role-based permissions for recalculation | Legacy approval workflow | Phase 5 Task 5.1 | Quotation API | ✅ IMPLEMENTED | Phase 5 Team |

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
- Price list precedence logic ✅ (Phase 5)
- WEF date usage
- Discount governance rules ✅ (Phase 5)
- Price source priority ✅ (Phase 5)
- Manual override authorization ✅ (Phase 5)

### Control & Locking (Builds: Locking Module, etc.)
- When locking applies
- Who can lock/unlock
- Approval intent

### Audit & Compliance (Builds: Audit Module, etc.)
- User action auditability ✅ (Phase 5)
- Traceability expectations ✅ (Phase 5)
- Change tracking requirements ✅ (Phase 5)

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

**Last Updated:** 2026-01-27  
**Total RETAIN Items:** 14 (9 identified and implemented, 5 placeholder for future builds)  
**Phase 5 RETAIN Items:** 6 items implemented (items #7, #9, #10, #11, #12, #13, #14)

