> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART3_STRUCTURE.md
> Bifurcated into: features/project/structure/PROJECT_BACKEND_DESIGN_PART3_STRUCTURE.md
> Module: Project > Structure
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 3: Project Structure & Hierarchy

**Document:** PROJECT_BACKEND_DESIGN_PART3_STRUCTURE.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete structure of the Project entity, its attributes, fields, and its position in the system hierarchy.

---

## 🏗️ Project Entity Structure

### Project Entity

**Table:** `projects`  
**Model:** `Project`  
**Purpose:** Organizational unit for client work, links clients to quotations

**Key Attributes:**
- `ProjectId` - Primary key
- `ProjectNo` - Unique project number (YYMMDD001)
- `ClientId` - Foreign key to clients (required)
- `Name` - Project name (required)
- `Location` - Project location (optional)
- `SpecificRequirement` - Specific requirements (optional)
- `DocumentReference` - Document reference (optional)
- `TemperatureMax` - Maximum temperature (optional)
- `TemperatureMin` - Minimum temperature (optional)
- `ClientName` - Legacy client name (optional, for backward compatibility)

---

## 📊 Field Details

### Required Fields

**ClientId:**
- Type: Integer (Foreign Key)
- Required: Yes (NOT NULL)
- References: `clients.ClientId`
- Purpose: Links project to client
- Validation: Must exist in clients table

**Name:**
- Type: String (VARCHAR 255)
- Required: Yes (NOT NULL)
- Purpose: Project name/identifier
- Validation: Required, max 255 characters

---

### Auto-Generated Fields

**ProjectNo:**
- Type: String (VARCHAR 20)
- Required: Yes (UNIQUE, NOT NULL)
- Auto-generated: Yes (unless manually provided)
- Format: YYMMDD001
- Purpose: Unique project identifier
- Validation: Must be unique

---

### Optional Fields

**Location:**
- Type: String (VARCHAR 255)
- Required: No (nullable)
- Purpose: Project location/address
- Validation: Max 255 characters

**SpecificRequirement:**
- Type: Text (VARCHAR 1000)
- Required: No (nullable)
- Purpose: Specific project requirements
- Validation: Max 1000 characters

**DocumentReference:**
- Type: String (VARCHAR 255)
- Required: No (nullable)
- Purpose: Document reference number
- Validation: Max 255 characters

**TemperatureMax:**
- Type: Numeric (DECIMAL)
- Required: No (nullable, default 0)
- Purpose: Maximum operating temperature
- Validation: Numeric, min -100, max 100

**TemperatureMin:**
- Type: Numeric (DECIMAL)
- Required: No (nullable, default 0)
- Purpose: Minimum operating temperature
- Validation: Numeric, min -100, max 100

**ClientName:**
- Type: String (VARCHAR 255)
- Required: No (nullable)
- Purpose: Legacy client name field (for backward compatibility)
- Note: Client name should come from Client relationship, not this field

---

## 🏢 Project Hierarchy in System

### Position in System

```
Organization (Top Level)
    │
    └─── Client (Customer Level)
            │
            ├─── Contact (Contact Persons)
            │
            └─── Project (Project Level) ← CURRENT LEVEL
                    │
                    └─── Quotation (Quotation Level)
                            │
                            └─── QuotationSale / Panel
                                    │
                                    └─── QuotationSaleBom / Feeder/BOM
                                            │
                                            └─── QuotationSaleBomItem / Component
```

---

### Project Role

**Project serves as:**
1. **Organizational Unit** - Groups quotations by project
2. **Client Work Tracking** - Tracks work for specific client projects
3. **Quotation Link** - Links quotations to client projects
4. **Project Management** - Enables project-based reporting and management

---

## 📋 Project Attributes Summary

### Core Attributes

| Attribute | Type | Required | Purpose |
|-----------|------|----------|---------|
| ProjectId | INT (PK) | Yes | Primary key |
| ProjectNo | VARCHAR(20) | Yes | Unique identifier |
| ClientId | INT (FK) | Yes | Client reference |
| Name | VARCHAR(255) | Yes | Project name |

### Optional Attributes

| Attribute | Type | Required | Purpose |
|-----------|------|----------|---------|
| Location | VARCHAR(255) | No | Project location |
| SpecificRequirement | VARCHAR(1000) | No | Requirements |
| DocumentReference | VARCHAR(255) | No | Document ref |
| TemperatureMax | DECIMAL | No | Max temperature |
| TemperatureMin | DECIMAL | No | Min temperature |
| ClientName | VARCHAR(255) | No | Legacy field |

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial structure document | Part 3 of Project backend design series |

---

**Previous:** [Part 2: Data Models & Relationships](PROJECT_BACKEND_DESIGN_PART2_DATA_MODELS.md)  
**Next:** [Part 4: Project Numbering System](PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md)

