# System of Engagement (SoE) Consumption Guide — Motor Control Equipment

**Status:** 🟢 BINDING (Living Document)  
**Depends On:** `SOR_CONTRACT__MOTOR_CONTROL_EQUIPMENT.md`  
**Last Updated:** 2026-01-03

---

## 📋 Document Purpose

Defines how UI, estimation, quotation, and dashboards may consume Motor Control Equipment data.

**Governance Model:** Rules are required, but when they become roadblocks, we review carefully and adopt what's useful.

**Review Trigger:** When real UI/estimation requirements cannot be met within current constraints.

---

## 1. Purpose

**Applies uniformly to:**
- LC1D, LC1E
- Capacitor duty contactors
- K-class contactors
- MPCB, MCCB, ACB
- All accessories

**Defines:**
- What UI can read
- What UI can do
- What UI must NOT do

---

## 2. Read-Only Contract

### SoE MAY:
- ✅ Read
- ✅ Filter
- ✅ Display
- ✅ Constrain choices

### SoE MAY NOT:
- ❌ Create catalog data
- ❌ Modify catalog data
- ❌ Infer rules
- ❌ Override prices
- ❌ Encode OEM logic

**Exception Process:** If a UI requirement needs to create/modify data, document and escalate to Phase-6 rules engine or catalog pipeline update.

---

## 3. Allowed Data Sources (Universal)

| Purpose | Sheet |
|---------|-------|
| Configuration options | `NSW_L1_CONFIG_LINES` |
| Attributes (KVU) | `L1_ATTRIBUTES_KVU` |
| SKU identity | `NSW_L2_PRODUCTS` |
| Variants | `NSW_PRODUCT_VARIANTS` |
| Prices | `NSW_PRICE_MATRIX` |

**Exception Process:** If UI needs additional data sources, document requirement and review for SoR contract update.

---

## 4. UI Behaviour Rules

### A. Structural Filters
- Use SC_Lx only
- No business meaning
- No inference

**Exception:** If UI needs to filter by duty/rating, use L1/KVU attributes, not SC_Lx.

### B. Configuration Selection
- Use L1 lines only
- Labels from `GenericDescriptor`
- Group via `L1_Group_Id`

**Exception:** If UI needs custom grouping, document requirement and review.

### C. Duty & Rating Display
- Read from KVU attributes
- Display only
- No recomputation

**Exception:** If UI needs computed ratings, document requirement and escalate to Phase-6 rules engine.

### D. Capability Handling
- Read only from `capability_codes`
- Disable unavailable capabilities
- Never infer from structure or name

**Exception:** If UI needs inferred capabilities, document requirement and review for SoR contract update.

### E. Accessories
- Display as optional FEATURE lines
- No automatic compatibility enforcement
- No hidden inclusion

**Exception:** If UI needs compatibility enforcement, escalate to Phase-6 rules engine.

### F. Pricing
- Read only from `NSW_PRICE_MATRIX`
- No UI pricing logic
- Currency & WEF respected

**Exception:** If UI needs pricing calculations, document requirement and escalate to Phase-6 rules engine.

---

## 5. Mandatory Validation Checklist

**Before UI approval:**

- [ ] **Data Discipline:** Read-only confirmed, no mutation
- [ ] **Structural Discipline:** SC_Lx used only structurally, no duty/ratings in SC_Lx
- [ ] **Duty Discipline:** Duty from L1 / KVU only, no name-based inference
- [ ] **Capability Discipline:** `capability_codes` only, no inference
- [ ] **Pricing Discipline:** Price from matrix only, no overrides
- [ ] **Layer Discipline:** L1 for configuration, L2 for identity+price
- [ ] **No BOM / Dependency Logic:** Phase-5 catalog is pure (no engineering rules)

**Exception Process:** If a validation item cannot be met, document the requirement and review for contract update or Phase-6 escalation.

---

## 6. Escalation Rule

**If UI requires:**
- Protection coordination
- Interlocking rules
- Accessory compatibility enforcement
- BOM explosion
- Dependency logic
- Engineering QC

**👉 Escalate to Phase-6 Rules Engine**  
**👉 Do NOT patch Phase-5 catalog or UI**

**Exception Process:** If Phase-6 is not available and requirement is critical, document and review for Phase-5 contract update.

---

## 7. Review & Correction Mechanism

**When a UI requirement cannot be met:**

1. **Document the requirement** (what UI needs, why current contract blocks it)
2. **Review carefully** with:
   - SoR contract
   - Business requirement
   - Technical feasibility
3. **Propose solution:**
   - Contract update (if SoR needs change)
   - Phase-6 escalation (if rules engine needed)
   - UI workaround (if acceptable)
4. **Update this guide** with resolution
5. **Commit change** with clear rationale

**Principle:** Rules are required, but when they block progress, we review and adopt what's useful.

---

## 8. Final Binding Statement

**SoE consumes. SoR decides. This applies to all Motor Control Equipment.**

**Exception:** When real requirements arise, we review and correct, then update this guide.

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-01-03 | Initial guide created | Phase-5 LC1E execution complete |
| 2026-01-03 | Moved to shared governance folder | Prevent divergence across series |

---

**Next Review:** When UI requirements arise that cannot be met within current constraints.

