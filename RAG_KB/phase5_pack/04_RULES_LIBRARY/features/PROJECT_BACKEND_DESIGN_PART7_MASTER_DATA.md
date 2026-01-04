---
Source: features/project/_general/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T02:13:10.739036
KB_Path: phase5_pack/04_RULES_LIBRARY/features/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md
---

> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md
> Bifurcated into: features/master/organization/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md
> Module: Master > Organization
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 7: Master Data Integration

**Document:** PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes how the Project module integrates with master data: Organization, Client, and Quotation.

---

## 🏢 Organization → Client → Project Flow

### Organization Connection

**Table:** `organizations`  
**Model:** `Organization`  
**Purpose:** Company/organization master

**Connection to Project:**
```
Organization (1) ──→ (N) Client ──→ (N) Project
```

**Usage:**
- Organization groups multiple clients
- Clients belong to organization
- Projects belong to clients
- Indirect connection: Project → Client → Organization

**Code:**
```php
$project = Project::with('client.organization')->find($projectId);
$organizationName = $project->client->organization->Name;
```

---

### Client Connection

**Table:** `clients`  
**Model:** `Client`  
**Purpose:** Customer companies

**Connection to Project:**
```
Client (1) ──→ (N) Project
```

**Direct Relationship:**
```php
// In Project model
public function client()
{
    return $this->belongsTo(Client::class, 'ClientId', 'ClientId');
}

// Usage
$project = Project::with('client')->find($projectId);
$clientName = $project->client->ClientName;
```

**Required:**
- Project MUST belong to a client
- ClientId is required (NOT NULL)
- Cannot create project without client

**Business Rules:**
- One project belongs to one client
- One client can have multiple projects
- Client must exist before creating project

---

### Quotation Connection

**Table:** `quotations`  
**Model:** `Quotation`  
**Purpose:** Quotations linked to projects

**Connection to Project:**
```
Project (1) ──→ (N) Quotation
```

**Direct Relationship:**
```php
// In Project model
public function quotations()
{
    return $this->hasMany(Quotation::class, 'ProjectId', 'ProjectId');
}

// Usage
$project = Project::with('quotations')->find($projectId);
$quotations = $project->quotations; // Collection of quotations
```

**Business Rules:**
- One project can have multiple quotations
- One quotation belongs to one project
- Cannot delete project if it has quotations

---

## 🔗 Complete Integration Map

### Organization to Project Flow

```
Organization
    │
    └─── Client
            │
            ├─── Contact
            │
            ├─── Project ← CURRENT LEVEL
            │       │
            │       └─── Quotation
            │               │
            │               └─── QuotationSale (Panel)
            │                       │
            │                       └─── QuotationSaleBom (Feeder/BOM)
            │                               │
            │                               └─── QuotationSaleBomItem (Component)
            │
            └─── Quotation (Direct - if project not used)
```

---

## 📊 Data Flow Examples

### Example 1: Creating Project from Client

**Step 1: User Selects Client**
```php
$client = Client::find($clientId);
```

**Step 2: System Creates Project**
```php
$project = new Project();
$project->ClientId = $clientId;
$project->Name = $request->Name;
$project->ProjectNo = $this->generateProjectNumber();
$project->save();
```

**Step 3: Project Linked to Client**
```php
// Relationship automatically established
$client->projects; // Includes new project
```

---

### Example 2: Loading Project with All Relationships

**Step 1: Load Project with Client**
```php
$project = Project::with('client')->find($projectId);
```

**Step 2: Load Project with Quotations**
```php
$project = Project::with('quotations')->find($projectId);
```

**Step 3: Load Project with All Relationships**
```php
$project = Project::with([
    'client',
    'client.organization',
    'quotations',
    'quotations.client'
])->find($projectId);
```

---

### Example 3: Project to Organization Access

**Step 1: Load Project**
```php
$project = Project::find($projectId);
```

**Step 2: Access Organization via Client**
```php
$organization = $project->client->organization;
$organizationName = $organization->Name;
```

**Or with Eager Loading:**
```php
$project = Project::with('client.organization')->find($projectId);
$organizationName = $project->client->organization->Name;
```

---

## 🔄 Integration Points

### Point 1: Project Creation

**Requires:**
- Client must exist
- ClientId must be valid

**Creates:**
- Project record
- Project number (auto-generated)
- Link to client

---

### Point 2: Quotation Creation

**Requires:**
- Project must exist
- ProjectId must be valid

**Creates:**
- Quotation record
- Link to project
- Link to client (via project)

---

### Point 3: Project Deletion

**Checks:**
- Project has quotations?
- If yes → Prevent deletion
- If no → Allow deletion

**Impact:**
- Deletes project record
- Breaks link to client (if project deleted)
- Breaks link to quotations (if project deleted)

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial master data integration document | Part 7 of Project backend design series |

---

**Previous:** [Part 6: Backend Services & Controllers](PROJECT_BACKEND_DESIGN_PART6_SERVICES.md)  
**Next:** [Part 8: Operation Level Details](PROJECT_BACKEND_DESIGN_PART8_OPERATIONS.md)

