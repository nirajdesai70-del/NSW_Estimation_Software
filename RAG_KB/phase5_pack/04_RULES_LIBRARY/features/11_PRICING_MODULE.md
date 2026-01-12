---
Source: features/component_item_master/price_list/11_PRICING_MODULE.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T01:11:05.122330
KB_Path: phase5_pack/04_RULES_LIBRARY/features/11_PRICING_MODULE.md
---

> Source: source_snapshot/docs/03_MODULES/11_PRICING_MODULE.md
> Bifurcated into: features/component_item_master/price_list/11_PRICING_MODULE.md
> Module: Component / Item Master > Price List
> Date: 2025-12-17 (IST)

# Pricing Module

**Document:** 11_PRICING_MODULE.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## Module Overview

**Purpose:** Manage product pricing with effective dates

**Controller:** PriceController (141 lines)  
**Model:** Price  
**Table:** prices

---

## Database Schema

```sql
prices
├── PriceId         INT PRIMARY KEY
├── ProductId       INT FK → products NOT NULL
├── Rate            DECIMAL(10,2) NOT NULL
├── EffectiveDate   DATE NOT NULL
├── Status          TINYINT DEFAULT 0
├── created_at      TIMESTAMP
└── updated_at      TIMESTAMP

INDEX idx_product_price ON prices(ProductId, EffectiveDate)
```

---

## Price Selection Logic

**Algorithm:**
```php
$currentDate = date('Y-m-d');
$price = Price::where('ProductId', $productId)
    ->where('EffectiveDate', '<=', $currentDate)
    ->where('Status', 0)
    ->orderBy('EffectiveDate', 'DESC')
    ->first();

return $price ? $price->Rate : 0;
```

**Selects most recent price where effective date is today or earlier**

---

## Price History

**Example:**
```
Product: SIV-S8-100A

Prices:
2022-01-01  ₹40,000  (Old price)
2022-04-01  ₹42,000  (Q1 increase)
2022-07-01  ₹45,000  (Q3 increase) ← Current
2022-10-01  ₹47,000  (Future increase)

On July 16, 2022:
- System uses ₹45,000 (Jul 1 price)
- Oct 1 price ignored (future)
```

---

## Price Management

**Operations:**
- Create new price (adds to history)
- Edit price (updates existing)
- Soft delete (Status=1)
- Import prices from Excel
- Export prices to Excel

**Business Rules:**
- Multiple prices per product allowed
- Effective date controls activation
- Price history preserved
- Future prices supported

---

**End of Document 11 - Pricing Module**

[← Back](10_CLIENT_PROJECT_MODULE.md) | [Next: User Management →](12_USER_MANAGEMENT.md)

