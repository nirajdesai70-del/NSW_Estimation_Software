> Source: source_snapshot/COSTING_DASHBOARD_PROJECT_BRIEF.md
> Bifurcated into: features/project/reports/COSTING_DASHBOARD_PROJECT_BRIEF.md
> Module: Project > Reports
> Date: 2025-12-17 (IST)

# Costing Dashboard Project - One-Page Brief

**Date:** December 2025  
**Status:** ✅ Ready to Share  
**Purpose:** Single-page project brief for all stakeholders

---

## 🎯 What We're Building

A structured costing engine and dashboard on top of NEPL V2 quotation system that:

- ✅ Replaces manual Excel costing sheets with automated engine
- ✅ Provides Costing Pack per quotation (snapshot, panel summary, pivots)
- ✅ Provides global dashboard for margins, hit rates, cost drivers
- ✅ Feeds Excel exports and future AI helpers

**Goal:** Single, reliable source of truth for all costing calculations and analysis.

---

## 📊 What Each Team Needs to Provide

### **Finance Team:**
- Costing calculation formulas (BOM, Feeder, Panel costs)
- Discount policy rules (how discounts are applied)
- CostHead categories and CostBucket mappings
- Price sanity thresholds
- **Clarification needed:** CLIENT SUPPLIED items treatment, rounding rules

### **Engineering Team:**
- Quantity multiplication rules (EffectiveQty formulas)
- BOM logic and panel design rules
- Component selection rules
- IEC 61439 basic rules (voltage, kW, short-circuit)
- Golden Rulebook content

### **DevOps / DB Admin:**
- Database read access (development/staging)
- Sample quotation data (5-10 anonymized quotations)
- Performance targets (specific load time numbers)
- **Clarification needed:** Specific performance numbers

### **Sales / Management:**
- Target margin rules
- Substitution matrix rules (economy vs premium paths)
- Dashboard access control requirements
- **Clarification needed:** Who can access what dashboards?

### **QA / Support:**
- Test scenarios (typical and edge cases)
- Real-world quotation examples
- Edge case identification

---

## 🔗 How This Fits Together

**Week 1-2:** Foundation
- DB access, costing formulas, quantity rules
- Build core costing engine

**Week 3:** Refinement
- CostHead system, export columns
- Golden Rulebook, historical data

**Week 4+:** Dashboards & AI
- UI design, performance optimization
- Global dashboard, AI integration

---

## 💡 Why We Need These Inputs

All inputs ensure we build a single, consistent costing engine that:

- ✅ Matches real NEPL business rules
- ✅ Shows correct KPIs in dashboards
- ✅ Satisfies Finance, Sales, Engineering, and Management requirements
- ✅ Replaces manual Excel with automated, trustworthy system

**Without these inputs, we risk building a tool that doesn't match reality and nobody trusts.**

---

## 📞 Contact

**Project Lead:** [Your Name]  
**Questions?** Contact project lead for clarification on any input requirements.

---

**Status:** ✅ Ready to Share with Stakeholders  
**Next Step:** Send to all stakeholders, get clarifications on counter questions
