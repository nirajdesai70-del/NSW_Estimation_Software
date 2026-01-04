# KPI – Manual Cost Percentage  
## Phase 5 Enhancement – Full Conversation Record

**Project:** NSW Estimation Software  
**Phase:** Phase 5 – Enhancements  
**Owner:** Group Nish  
**Prepared by:** Niraj Desai  
**Date:** 2025-12-26  
**Status:** Logged & Traceable  

---

## Context

This document records the full design conversation and decisions related to introducing a **Manual Cost Percentage KPI** into the NSW Estimation Software as a Phase-5 enhancement.

The KPI is intended to act as an early-warning indicator for margin leakage, catalog gaps, and pricing inconsistency caused by excessive manual or override pricing.

---

## Conversation Flow

### 1. KPI Proposal

**Manual Cost %**  
= (Sum of manual-priced + override line item cost) ÷ (Total quotation cost)

Purpose:
- Detect hidden margin erosion  
- Identify catalog gaps  
- Improve predictability of quotations  
- Reduce review overhead  

---

### 2. Business Rationale

Key observations:
- Rising manual pricing correlates with missing SKUs, outdated price lists, ad-hoc discounting  
- Lower manual pricing indicates mature catalog and predictable margins  

---

### 3. Threshold Definition

| Status | Manual Cost % |
|------|----------------|
| Green | < 15% |
| Watch | 15% – 30% |
| Action | > 30% |

---

### 4. Governance Actions

- Identify categories driving manual entries  
- Create SKU tasks for recurring items  
- Enforce discount approval bands  
- Refresh vendor price lists  

---

### 5. Required Data Fields

- line_id  
- quotation_id  
- category  
- subcategory  
- sku_id (nullable)  
- price_source  
- unit_price  
- quantity  
- discount_applied  
- created_at  
- created_by  

---

### 6. SQL Logic (PostgreSQL 14+)

```sql
SELECT
  100.0 * SUM(
    CASE 
      WHEN price_source IN ('MANUAL','OVERRIDE')
      THEN unit_price * qty * (1 - COALESCE(discount_applied,0))
      ELSE 0 
    END
  ) / NULLIF(
    SUM(unit_price * qty * (1 - COALESCE(discount_applied,0))),0
  ) AS manual_cost_pct
FROM quote_lines
WHERE created_at >= now() - interval '30 days';
```

---

## 5R Summary

**Results** – Margin leakage visibility  
**Risks** – Manual overrides masking gaps  
**Rules** – Manual pricing traceability  
**Roadmap** – Phase 5 → Phase 6 AI  
**References** – NSW Estimation v1.3  

---

Prepared by Niraj Desai under Niraj Framework Evolution — All Rights Reserved
