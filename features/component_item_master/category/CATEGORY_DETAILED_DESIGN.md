> Source: source_snapshot/CATEGORY_DETAILED_DESIGN.md
> Bifurcated into: features/component_item_master/category/CATEGORY_DETAILED_DESIGN.md
> Module: Component / Item Master > Category
> Date: 2025-12-17 (IST)

# Category Detailed Design & Architecture

**Document:** CATEGORY_DETAILED_DESIGN.md  
**Version:** 1.0  
**Date:** December 2025  
**Status:** 🔴 **STANDING INSTRUCTION - PERMANENT STANDARD**

---

## 📋 Table of Contents

1. [Category Overview](#1-category-overview)
2. [Database Structure](#2-database-structure)
3. [Model Design](#3-model-design)
4. [Controller Design](#4-controller-design)
5. [Views & UI](#5-views--ui)
6. [Relationships & Dependencies](#6-relationships--dependencies)
7. [Workflows & Operations](#7-workflows--operations)
8. [Code Examples](#8-code-examples)
9. [Troubleshooting](#9-troubleshooting)
10. [Complete Code File Mapping](#10-complete-code-file-mapping)

---

## 1. Category Overview

### 1.1 Purpose

**Category** is the top-level classification in the Item Master hierarchy. It serves as the foundation for organizing all products, components, and BOM items in the system.

**Key Roles:**
- **Top-Level Classification:** Primary organizational structure
- **Required Field:** Every product must have a CategoryId
- **Attribute Schema Driver:** Determines which attributes apply to products
- **Filtering & Search:** Primary filter for product searches
- **BOM Organization:** Groups products in Master BOMs and Production BOMs

### 1.2 Position in Hierarchy

```
Category (Required) ← YOU ARE HERE
  └── SubCategory (Optional)
        └── Item/ProductType (Optional)
              └── Generic Product (ProductType = 1)
                    └── Make (Optional)
                          └── Series (Optional)
                                └── Specific Product (ProductType = 2)
```

### 1.3 Core Characteristics

- **Required:** Every product must have a CategoryId
- **Top-Level:** No parent category (root level)
- **One-to-Many:** One category can have many subcategories, items, and products
- **Attribute Schema:** Defines which attributes apply to products in this category
- **Immutable:** Category name should not change frequently (affects all products)

---

[Rest of document continues...]

