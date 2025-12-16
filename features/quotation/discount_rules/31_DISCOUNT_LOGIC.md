> Source: source_snapshot/docs/02_DATABASE/31_DISCOUNT_LOGIC.md
> Bifurcated into: features/quotation/discount_rules/31_DISCOUNT_LOGIC.md
> Module: Quotation > Discount Rules
> Date: 2025-12-17 (IST)

# Discount Logic & Application

**Document:** 31_DISCOUNT_LOGIC.md  
**Version:** 1.0

---

## Discount Levels

### Item-Level Discount
```
Applied to individual BOM items
Discount field in quotation_sale_bom_items table
```

**Formula:**
```
NetRate = Rate × (1 - Discount/100)
```

**Example:**
```
Rate: ₹10,000
Discount: 5%
NetRate = 10,000 × 0.95 = ₹9,500
```

---

### Quotation-Level Discount
```
Applied to entire quotation
Discount field in quotations table
```

**Formula:**
```
Subtotal = Sum of all sales
DiscountAmount = Subtotal × (Discount/100)
Total = Subtotal - DiscountAmount
```

**Example:**
```
Subtotal: ₹2,50,000
Discount: 5%
DiscountAmount = 2,50,000 × 0.05 = ₹12,500
Total = 2,50,000 - 12,500 = ₹2,37,500
```

---

## Multiple Discounts

**Cascading:**
1. Item discount applied first (NetRate)
2. Amounts calculated
3. Quotation discount applied to subtotal

**Not Compounding:**
```
Item discount does NOT compound with quotation discount
They are independent
```

---

**End of Document 31 - Discount Logic**

[← Back](30_NUMBERING_SYSTEM.md) | [Next: Admin Guide →](32_ADMIN_GUIDE.md)

