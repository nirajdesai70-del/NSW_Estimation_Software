# Phase 5 Glossary

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT  
**Owner:** Phase 5 Senate  

## Purpose
Standard vocabulary and terminology for Phase 5 work. All terms must be used consistently across all Phase 5 documents.

## Source of Truth
- **Canonical:** This is the authoritative glossary for Phase 5

## Core Terms

### Phase Structure
- **Phase 5:** Analysis-only phase that freezes canonical data definitions and schema design
- **Step 1:** Freeze NSW Canonical Data Dictionary
- **Step 2:** Define NSW Canonical Schema (Design Only)
- **Post-Phase 5:** Implementation work (backend, frontend, deployment)

### Data Dictionary Terms
- **Entity:** A business concept (Category, Product, BOM, etc.)
- **Semantic:** Business meaning of an entity or field
- **Relationship:** How entities connect (one-to-many, many-to-many)
- **Business Rule:** Constraint or rule that governs entity behavior

### Schema Terms
- **Table:** Database table structure
- **Column:** Field within a table
- **Constraint:** Database-level rule (PK, FK, Unique, Check)
- **FK:** Foreign Key relationship

### Resolution Levels
- **L0:** Unresolved placeholder (no ProductId)
- **L1:** Partially resolved (ProductId may exist but not fully specified)
- **L2:** Fully resolved (ProductId exists and is complete)

### BOM Terms
- **Master BOM:** Template BOM (L0/L1 only, no ProductId)
- **Quote BOM:** Instance BOM (can have ProductId, L0/L1/L2)
- **Copy-never-link:** Quote BOMs are always copies, never references
- **Feeder:** Synonym for BOM Group

### Module Ownership
- **AUTH:** Authentication & Authorization module
- **CIM:** Component/Item Master module
- **MBOM:** Master BOM module
- **QUO:** Quotation module
- **PRICING:** Pricing module
- **AUDIT:** Audit & History module
- **AI:** AI/ML module

### Freeze Terms
- **FROZEN:** Document is locked and cannot be changed without governance approval
- **DRAFT:** Document is work-in-progress
- **REFERENCE:** Document is informational only, not canonical

## Change Log
- v1.0: Created initial glossary

