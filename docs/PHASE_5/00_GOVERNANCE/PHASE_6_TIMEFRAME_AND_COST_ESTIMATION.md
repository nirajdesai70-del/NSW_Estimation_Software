# Phase-6 Timeframe & Cost Estimation

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ESTIMATION DOCUMENT  
**Reference:** Phase-6 Execution Plan v1.4

---

## 🗓️ Timeframe Summary

### Overall Duration
- **Base Timeline:** 10-12 weeks
- **Recommended Buffer:** +1 week
- **Total Estimated Duration:** **11-13 weeks** (2.5-3 months)

### Timeline Breakdown by Phase

| Phase | Duration | Weeks | Key Activities |
|-------|----------|-------|----------------|
| **Week 0** | 1 week | Entry Gate & Setup | Entry gate verification, structure setup, module boundaries |
| **Weeks 1-6** | 6 weeks | Core Development | Parallel tracks: UI, Catalog, Costing Engine, DB Implementation |
| **Weeks 7-8** | 2 weeks | UI Completion & Ops | Costing UI, Operational readiness, Legacy parity gate |
| **Weeks 9-10** | 2 weeks | Integration & Stabilisation | End-to-end integration, bug fixes, UX polish |
| **Weeks 11-12** | 2 weeks | Closure | Exit criteria verification, documentation, handover |

### Critical Path Dependencies

1. **Week 0:** Entry gate must pass (blocks all work)
2. **Weeks 0-1:** Database implementation (blocks UI work)
3. **Weeks 3-6:** Costing engine foundations (D0 Gate) (blocks costing UI)
4. **Week 8.5:** Legacy parity gate (blocks integration)
5. **Weeks 9-10:** Integration testing (blocks closure)

---

## 👥 Team Composition Assumptions

### Recommended Team Structure

| Role | Count | Allocation | Notes |
|------|-------|------------|-------|
| **Senior Full-Stack Developer** | 2 | 100% | Lead UI + Backend development |
| **Mid-Level Full-Stack Developer** | 2 | 100% | UI + Backend support |
| **Backend/Engine Developer** | 1 | 100% | Costing engine, QCD/QCA, calculations |
| **Database/DevOps Engineer** | 1 | 50% | DB migrations, schema parity, seed scripts |
| **UI/UX Designer** | 1 | 50% | UI design, UX flows, design system |
| **QA Engineer** | 1 | 75% | Testing, validation, gate verification |
| **Product Owner** | 1 | 25% | Requirements, prioritization, gate approvals |
| **Tech Lead/Architect** | 1 | 25% | Architecture review, technical decisions |

### Total Team Size
- **Full-time equivalent (FTE):** ~7.5 FTE
- **Peak team size:** 9 people (part-time allocations)

---

## 💰 Cost Estimation Framework

### Assumptions
- **Working days per week:** 5 days
- **Hours per day:** 8 hours
- **Total working days (12 weeks):** 60 days
- **Total working days (13 weeks with buffer):** 65 days

### Effort Estimation by Track

| Track | Tasks | Estimated Effort (Days) | Notes |
|-------|-------|-------------------------|-------|
| **Track A: Productisation** | 33 | 35-40 days | UI development, complex workflows |
| **Track A-R: Reuse & Legacy Parity** | 7 | 8-10 days | Parallel with Track A |
| **Track B: Catalog Tooling** | 16 | 18-22 days | Import UI, validation, governance |
| **Track C: Operational Readiness** | 12 | 12-15 days | RBAC, approvals, audit |
| **Track D0: Costing Engine** | 14 | 20-25 days | Engine development, QCD/QCA |
| **Track D: Costing & Reporting** | 20 | 25-30 days | UI, dashboards, Excel export |
| **Track E: Canon Implementation** | ~29 | 30-35 days | DB, guardrails, API, multi-SKU |
| **Integration & Stabilisation** | 12 | 15-18 days | Testing, bug fixes, polish |
| **Closure** | 5 | 5-7 days | Documentation, handover |
| **Legacy Parity Gate** | 6 | 3-4 days | Verification |
| **Week 0 Setup** | 8 | 5-7 days | Entry gate, structure setup |
| **TOTAL** | **~133** | **~176-213 days** | With parallelization: ~60-65 working days |

### Cost Estimation (Sample Rates)

**Note:** Replace with actual team rates for accurate estimation.

| Role | Rate (USD/hour) | Hours (12 weeks) | Cost (USD) |
|------|-----------------|------------------|------------|
| Senior Full-Stack Developer (2 × 100%) | $80 | 960 | $76,800 |
| Mid-Level Full-Stack Developer (2 × 100%) | $60 | 960 | $57,600 |
| Backend/Engine Developer (1 × 100%) | $75 | 480 | $36,000 |
| Database/DevOps Engineer (1 × 50%) | $70 | 240 | $16,800 |
| UI/UX Designer (1 × 50%) | $65 | 240 | $15,600 |
| QA Engineer (1 × 75%) | $55 | 360 | $19,800 |
| Product Owner (1 × 25%) | $90 | 120 | $10,800 |
| Tech Lead/Architect (1 × 25%) | $100 | 120 | $12,000 |
| **TOTAL** | | **3,480 hours** | **$245,000** |

### Cost Ranges

| Scenario | Duration | Total Cost (USD) | Notes |
|----------|----------|------------------|-------|
| **Optimistic** | 11 weeks | $220,000 - $240,000 | Minimal delays, efficient execution |
| **Realistic** | 12 weeks | $240,000 - $260,000 | Expected timeline with normal issues |
| **Pessimistic** | 13 weeks | $260,000 - $280,000 | With buffer, some delays, scope adjustments |

### Additional Cost Considerations

1. **Infrastructure Costs:**
   - Development/staging environments: $500-1,000/month
   - Testing tools/licenses: $200-500/month
   - **Total (3 months):** $2,100 - $4,500

2. **Third-Party Tools:**
   - Design tools (Figma, etc.): $100-200/month
   - Project management tools: $100-200/month
   - **Total (3 months):** $600 - $1,200

3. **Contingency (10-15%):**
   - For unexpected issues, scope adjustments
   - **Amount:** $24,000 - $40,000

### Total Cost Estimate

| Component | Cost Range (USD) |
|-----------|------------------|
| **Development Team** | $240,000 - $280,000 |
| **Infrastructure** | $2,100 - $4,500 |
| **Third-Party Tools** | $600 - $1,200 |
| **Contingency (12%)** | $29,000 - $34,000 |
| **TOTAL ESTIMATE** | **$272,000 - $320,000** |

---

## 📊 Effort Distribution

### By Work Type

| Work Type | % of Total Effort | Days |
|-----------|-------------------|------|
| **UI Development** | 35% | 21-23 days |
| **Backend/Engine** | 30% | 18-20 days |
| **Database/Implementation** | 15% | 9-10 days |
| **Testing & QA** | 12% | 7-8 days |
| **Documentation & Closure** | 8% | 5-6 days |

### By Track Priority

| Priority | Track | Effort (Days) | Critical Path |
|----------|-------|---------------|---------------|
| **P0 (Critical)** | Track E (DB) | 30-35 | Yes - Blocks UI |
| **P0 (Critical)** | Track D0 (Engine) | 20-25 | Yes - Blocks Costing UI |
| **P1 (High)** | Track A (UI) | 35-40 | Yes - Core functionality |
| **P1 (High)** | Track D (Costing UI) | 25-30 | Yes - After D0 Gate |
| **P2 (Medium)** | Track A-R (Reuse) | 8-10 | No - Parallel |
| **P2 (Medium)** | Track B (Catalog) | 18-22 | No - Parallel |
| **P2 (Medium)** | Track C (Ops) | 12-15 | No - Parallel |

---

## ⚠️ Risk Factors Affecting Timeline & Cost

### High-Impact Risks

| Risk | Impact on Timeline | Impact on Cost | Mitigation |
|------|-------------------|----------------|------------|
| **Database migration complexity** | +1-2 weeks | +$20,000-40,000 | Early DB work, thorough testing |
| **Costing engine performance issues** | +1 week | +$20,000-30,000 | Performance testing in D0 Gate |
| **Legacy parity gaps discovered** | +1 week | +$20,000-30,000 | Early legacy review, checklist |
| **Integration issues** | +1 week | +$20,000-30,000 | Early integration testing |
| **Scope creep** | +1-2 weeks | +$20,000-40,000 | Strict gate controls, change management |

### Medium-Impact Risks

| Risk | Impact on Timeline | Impact on Cost | Mitigation |
|------|-------------------|----------------|------------|
| **Team availability** | +0.5-1 week | +$10,000-20,000 | Buffer in timeline, cross-training |
| **Third-party dependencies** | +0.5 week | +$10,000-15,000 | Early dependency identification |
| **Learning curve** | +0.5 week | +$10,000-15,000 | Knowledge sharing, documentation |

---

## 📅 Milestone-Based Payment Schedule (Optional)

If using milestone-based payments:

| Milestone | Deliverable | % Complete | Payment (USD) |
|-----------|-------------|------------|---------------|
| **M1: Week 0** | Entry Gate Passed | 5% | $13,600 - $16,000 |
| **M2: Week 3** | DB Implementation Complete | 20% | $54,400 - $64,000 |
| **M3: Week 6** | D0 Gate Passed (Engine Ready) | 35% | $95,200 - $112,000 |
| **M4: Week 8** | Core UI Complete | 50% | $136,000 - $160,000 |
| **M5: Week 10** | Integration Complete | 75% | $204,000 - $240,000 |
| **M6: Week 12** | Phase-6 Closure | 100% | $272,000 - $320,000 |

---

## ✅ Recommendations

### Timeline Optimization
1. **Start DB work immediately** (Week 0) - Critical path
2. **Parallel execution** - Maximize track parallelism
3. **Early integration testing** - Start Week 8, not Week 9
4. **Buffer allocation** - Use +1 week buffer for unexpected issues

### Cost Optimization
1. **Fixed-price contract** - Lock scope, manage changes strictly
2. **Milestone-based payments** - Align payments with deliverables
3. **Resource optimization** - Use part-time specialists (DB, UX) efficiently
4. **Early risk mitigation** - Invest in early testing to avoid late-stage fixes

### Risk Mitigation
1. **Weekly progress reviews** - Catch delays early
2. **Gate enforcement** - Don't proceed without gate signoff
3. **Scope freeze** - Minimize scope changes after Week 0
4. **Contingency reserve** - Maintain 12-15% contingency

---

## 📝 Notes

- **Rates are sample values** - Replace with actual team rates
- **Effort estimates** - Based on task complexity and historical data
- **Timeline assumes** - Full team availability, minimal blockers
- **Cost includes** - Development, testing, documentation, basic infrastructure
- **Cost excludes** - Production infrastructure, ongoing maintenance, Phase-7 work

---

**Document Status:** ✅ ESTIMATION COMPLETE  
**Last Updated:** 2025-01-27  
**Next Review:** Before Phase-6 kickoff, update with actual team rates
