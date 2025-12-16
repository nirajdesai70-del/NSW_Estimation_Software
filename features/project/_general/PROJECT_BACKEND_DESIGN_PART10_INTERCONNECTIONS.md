> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md
> Bifurcated into: features/project/_general/PROJECT_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md
> Module: Project > General
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 10: Interconnections & Data Flow

**Document:** PROJECT_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete interconnection map and data flow between Project and all other components: Organization, Client, Quotation, and related modules.

---

## 🗺️ Complete Relationship Map

### Organization → Client → Project → Quotation Flow

```
Organization (1)
    │
    └─── Client (N)
            │
            ├─── Contact (N)
            │
            ├─── Project (N) ← CURRENT LEVEL
            │       │
            │       └─── Quotation (N)
            │               │
            │               ├─── QuotationMakeSeries (N)
            │               │
            │               └─── QuotationSale / Panel (N)
            │                       │
            │                       └─── QuotationSaleBom / Feeder/BOM (N)
            │                               │
            │                               └─── QuotationSaleBomItem / Component (N)
            │
            └─── Quotation (N) [Direct - if project not used]
```

---

## 🔗 Interconnection Details

### Project ↔ Client

**Type:** Many-to-One (N:1)

**Project to Client:**
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

**Client to Project:**
```php
// In Client model
public function projects()
{
    return $this->hasMany(Project::class, 'ClientId', 'ClientId');
}

// Usage
$client = Client::with('projects')->find($clientId);
$projects = $client->projects; // Collection of projects
```

**Business Rules:**
- Project MUST belong to a client
- ClientId is required (NOT NULL)
- One project belongs to one client
- One client can have multiple projects

---

### Project ↔ Quotation

**Type:** One-to-Many (1:N)

**Project to Quotation:**
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

**Quotation to Project:**
```php
// In Quotation model
public function project()
{
    return $this->belongsTo(Project::class, 'ProjectId', 'ProjectId');
}

// Usage
$quotation = Quotation::with('project')->find($quotationId);
$projectName = $quotation->project->Name;
```

**Business Rules:**
- Project can have multiple quotations
- Quotation belongs to one project
- Cannot delete project if it has quotations

---

### Project ↔ Organization (Indirect)

**Type:** Indirect (via Client)

**Access Path:**
```
Project → Client → Organization
```

**Code:**
```php
$project = Project::with('client.organization')->find($projectId);
$organizationName = $project->client->organization->Name;
```

**Business Rules:**
- Project belongs to client
- Client belongs to organization
- Project indirectly linked to organization

---

## 🔄 Data Flow Diagrams

### Flow 1: Creating Project

```
Step 1: User selects Client
    ↓
Step 2: System validates ClientId exists
    ↓
Step 3: System generates ProjectNo (YYMMDD001)
    ↓
Step 4: System creates Project
    Project.ClientId = selected Client
    Project.ProjectNo = generated number
    ↓
Step 5: Project created and linked to Client
    ↓
Step 6: System redirects to project list
```

---

### Flow 2: Creating Quotation from Project

```
Step 1: User selects Project
    ↓
Step 2: System loads Project with Client
    ↓
Step 3: System creates Quotation
    Quotation.ProjectId = selected Project
    Quotation.ClientId = Project.ClientId (from project)
    ↓
Step 4: Quotation linked to Project
    ↓
Step 5: System displays quotation
```

---

### Flow 3: Viewing Project with Quotations

```
Step 1: User opens Project edit page
    ↓
Step 2: System loads Project
    ↓
Step 3: System loads Quotations for Project (paginated)
    Quotation WHERE ProjectId = project.ProjectId
    ↓
Step 4: System eager loads Client for each Quotation
    ↓
Step 5: System displays Project with Quotations list
```

---

### Flow 4: Deleting Project

```
Step 1: User clicks Delete Project
    ↓
Step 2: System checks for Quotations
    Quotation WHERE ProjectId = ProjectId
    ↓
Step 3: IF quotations found
    ↓
    RETURN error: "Cannot delete - has quotations"
    ↓
Step 4: ELSE (no quotations)
    ↓
    DELETE Project
    ↓
Step 5: RETURN success
```

---

## 📊 Complete Data Flow Summary

### Creation Flow

```
Organization → Client → Project → Quotation
```

### Access Flow

```
Project → Client → Organization
Project → Quotations → QuotationSale → QuotationSaleBom → QuotationSaleBomItem
```

### Deletion Flow

```
Project → Check Quotations → IF exists: Prevent deletion
Project → Check Quotations → IF not exists: Allow deletion
```

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial interconnections document | Part 10 of Project backend design series |

---

**Previous:** [Part 9: Logic Level Details](PROJECT_BACKEND_DESIGN_PART9_LOGIC.md)  
**Next:** [Part 11: Codebase Reference](PROJECT_BACKEND_DESIGN_PART11_CODEBASE.md)

