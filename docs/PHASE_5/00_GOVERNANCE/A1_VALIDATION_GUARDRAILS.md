# A1 — Canonical Validation Guardrails (Phase-5)

**Status:** 🟡 IN PROGRESS  
**Freeze Impact:** 🔴 BLOCKING (Category A)  
**Scope:** Applies to NSW Estimation Software – Phase-5 and later  
**Purpose:** Define non-negotiable system invariants enforced across schema, logic, and APIs.

---

## A1.0 Guardrail Governance Rules

- Guardrails are system invariants, not business preferences
- Violations must be:
  - Blocked, normalized, or explicitly flagged
- Each guardrail must specify:
  1. Intent
  2. Rule
  3. Enforcement Layer(s)
  4. Implementation Reference
  5. Failure Mode
- Guardrails apply regardless of UI, API, or import path

---

## G1 — Master BOM must NOT reference ProductId

### Intent

Prevent premature binding of conceptual BOMs to physical products.

### Rule

- Master BOMs must never reference a concrete product_id.
- Product binding is only allowed at Production BOM or downstream execution stages.

### Enforcement

- **Schema:** product_id column must be NULL for Master BOM rows
- **Validator:** Reject any write where:

```
bom_type = MASTER AND product_id IS NOT NULL
```

### Implementation Reference

- **Module:** MBOM
- **Validator:** mbom_validators.py (planned / existing)
- **Data Dictionary:** BOM entity semantics

### Failure Mode

- Hard reject (HTTP 400 / validation error)
- Error message:

```
Master BOM cannot reference ProductId
```

---

## G2 — Production BOM must reference ProductId

### Intent

Ensure execution-ready BOMs are fully resolved and traceable.

### Rule

- Production BOM rows must reference a valid product_id.
- A Production BOM without ProductId is considered incomplete and invalid.

### Enforcement

- **Schema:** product_id NOT NULL when bom_type = PRODUCTION
- **Validator:** Reject save or transition if:

```
bom_type = PRODUCTION AND product_id IS NULL
```

### Implementation Reference

- **Module:** MBOM
- **Transition logic:** Master → Production promotion flow
- **Data Dictionary:** BOM lifecycle rules

### Failure Mode

- Hard reject
- Error message:

```
Production BOM requires ProductId
```

---

## G3 — IsPriceMissing normalizes all monetary outputs

### Intent

Avoid partial or misleading totals when pricing data is incomplete.

### Rule

If any required price input is missing:
- All derived monetary values must be normalized to 0
- is_price_missing = TRUE must be set

### Enforcement

- **Computation Layer:** Pricing / Estimation Engine
- **Output Rule:**

```
amount = 0
tax = 0
total = 0
```

### Implementation Reference

- **Module:** PricingResolver, DiscountEngine
- **Flag:** is_price_missing

### Failure Mode

- Soft normalize + flag
- No exception; computation continues safely

---

## G4 — RateSource consistency is mandatory

### Intent

Guarantee traceability of how a rate was derived.

### Rule

Each line must have exactly one effective rate source:
- PRICELIST
- MANUAL

Mixed or undefined sources are invalid.

### Enforcement

- **Resolver:** PricingResolver
- **Snapshot:** rate_source persisted with rate

### Implementation Reference

- **File:** pricing_resolver.py
- **Enum:** RateSource

### Failure Mode

- Hard reject if ambiguous
- Audit warning if overridden

---

## G5 — UNRESOLVED normalizes dependent values

### Intent

Prevent propagation of undefined states.

### Rule

If a line is marked UNRESOLVED:
- All dependent computed fields must normalize to safe defaults

### Enforcement

- **Computation Layer**
- **Flag propagation**

### Failure Mode

- Soft normalize + flag

---

## G6 — FIXED_NO_DISCOUNT forces discount = 0

### Intent

Protect contractual or locked pricing.

### Rule

When a line is marked FIXED_NO_DISCOUNT:
- No discount rule (LINE / CATEGORY / SITE) may apply

### Enforcement

- **DiscountResolver**
- **Override precedence**

### Failure Mode

- Discount ignored
- Flag emitted: DISCOUNT_BLOCKED_BY_POLICY

---

## G7 — All discounts are percentage-based

### Intent

Ensure consistency, auditability, and math safety.

### Rule

- Discounts must be expressed only as percentage (0–100)
- Absolute discounts are forbidden

### Enforcement

- **Schema:** DECIMAL(5,2)
- **Validator:** Reject non-percentage input

### Failure Mode

- Hard reject

---

## G8 — L1-SKU reuse is allowed and expected

### Intent

Support estimation reuse and catalog efficiency.

### Rule

- Same SKU may appear across:
  - Multiple quotations
  - Multiple BOMs
- No uniqueness constraint at SKU usage level

### Enforcement

- **Schema:** No unique constraint on SKU usage
- **Design:** Explicitly allowed

### Failure Mode

- None (this is a permissive guardrail)

---

## A1 Status Tracker

| Guardrail | Status |
|-----------|--------|
| G1 | ✅ DONE |
| G2 | ✅ DONE |
| G3 | ⏳ TODO |
| G4 | ⏳ TODO |
| G5 | ⏳ TODO |
| G6 | ⏳ TODO |
| G7 | ⏳ TODO |
| G8 | ⏳ TODO |

---

## Next Action (Recommended)

Tomorrow / next block:
- Finalize G3 + G4 (they directly reference existing code)
- Then G6 (ties to DiscountResolver you already built)

If you want, I can:
- Finish G3 + G4 immediately, or
- Convert this into a Data Dictionary–ready appendix format, or
- Map each guardrail to exact file + line references (for auditors).

Just say the word.

