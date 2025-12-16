> Source: source_snapshot/docs/03_MODULES/09_BOM_MODULE.md
> Bifurcated into: features/master_bom/_general/09_BOM_MODULE.md
> Module: Master BOM > General (Overview)
> Date: 2025-12-17 (IST)

# BOM Module - Complete Reference

**Document:** 09_BOM_MODULE.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Module Overview

**Purpose:** Bill of Materials management - define product assemblies

**Controllers:** 1 (MasterBomController)  
**Models:** 2 (MasterBom, MasterBomItem)  
**Views:** 3  
**Routes:** 7 RESTful + custom  
**Database Tables:** 2

---

## Complete Module Structure

**Master BOM (Template):**
```
master_boms (1) ──→ (N) master_bom_items ──→ (1) products
```

**Quotation BOM (Instance):**
```
quotation_sale_boms (1) ──→ (N) quotation_sale_bom_items ──→ (1) products
```

---

## Controller Methods

**MasterBomController.php** (283 lines)

| Method | Route | Purpose |
|--------|-------|---------|
| index() | GET /masterbom | List all master BOMs |
| create() | GET /masterbom/create | Show create form |
| store() | POST /masterbom | Save new master BOM |
| edit($id) | GET /masterbom/{id}/edit | Show edit form with items |
| update($id) | PUT /masterbom/{id} | Update BOM and items |
| destroy($id) | DELETE /masterbom/{id} | Soft delete BOM |

---

## Database Tables

### master_boms
```sql
MasterBomId    INT PRIMARY KEY
Name           VARCHAR(255) NOT NULL UNIQUE
Status         TINYINT DEFAULT 0
created_at     TIMESTAMP
updated_at     TIMESTAMP
```

### master_bom_items
```sql
MasterBomItemId  INT PRIMARY KEY
MasterBomId      INT FK → master_boms
ProductId        INT FK → products (Generic only!)
Quantity         DECIMAL(10,2) DEFAULT 1.00
Status           TINYINT DEFAULT 0
created_at       TIMESTAMP
updated_at       TIMESTAMP
```

---

## BOM Creation Process

**See Document 19_BOM_CREATION_FLOW.md for complete details**

---

## Summary

**Purpose:** Define reusable product assemblies  
**Benefit:** 75% time savings in quotation creation  
**Usage:** Template-based BOM insertion

---

**End of Document 09 - BOM Module**

[← Back: Product Module](08_PRODUCT_MODULE.md) | [Next: Client/Project Module →](10_CLIENT_PROJECT_MODULE.md)

