> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART2_DATA_MODELS.md
> Bifurcated into: features/project/structure/PROJECT_BACKEND_DESIGN_PART2_DATA_MODELS.md
> Module: Project > Structure
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 2: Data Models & Relationships

**Document:** PROJECT_BACKEND_DESIGN_PART2_DATA_MODELS.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete data model structure, database schema, and all relationships for the Project module.

---

## 🗄️ Database Schema

### projects Table

**Purpose:** Store project information

**Key Columns:**
- `ProjectId` (PK) - Primary key, auto-increment
- `ProjectNo` (UNIQUE) - Unique project number (YYMMDD001 format)
- `ClientId` (FK) - Foreign key to clients (NOT NULL, required)
- `Name` - Project name (NOT NULL, required)
- `Location` - Project location (optional)
- `ClientName` - Legacy client name field (optional, for backward compatibility)
- `SpecificRequirement` - Specific project requirements (optional)
- `DocumentReference` - Document reference (optional)
- `TemperatureMax` - Maximum temperature (optional, numeric)
- `TemperatureMin` - Minimum temperature (optional, numeric)
- `Status` - Status flag (0=Active, 1=Deleted) - if soft delete implemented
- `created_at` - Created timestamp
- `updated_at` - Updated timestamp

**Indexes:**
- PRIMARY KEY (ProjectId)
- UNIQUE KEY (ProjectNo)
- INDEX (ClientId)

**Relationships:**
```sql
FOREIGN KEY (ClientId) REFERENCES clients(ClientId)
```

---

## 📊 Model Structure

### Project Model

**File:** `app/Models/Project.php`  
**Table:** `projects`  
**Primary Key:** ProjectId

**Fillable Fields:**
```php
protected $fillable = [
    'ProjectId',
    'ProjectNo',
    'ClientId',
    'Name',
    'Location',
    'ClientName',           // Legacy support
    'SpecificRequirement',
    'DocumentReference',
    'TemperatureMax',
    'TemperatureMin',
];
```

**Relationships:**
```php
// Project belongsTo Client
public function client()
{
    return $this->belongsTo(Client::class, 'ClientId', 'ClientId');
}

// Project hasMany Quotation
public function quotations()
{
    return $this->hasMany(Quotation::class, 'ProjectId', 'ProjectId');
}
```

---

## 🔗 Complete Relationship Map

### Organization → Client → Project → Quotation Flow

```
Organization (1)
    │
    └─── Client (N)
            │
            ├─── Contact (N)
            │
            ├─── Project (N)
            │       │
            │       └─── Quotation (N)
            │               │
            │               └─── QuotationSale (Panel) (N)
            │                       │
            │                       └─── QuotationSaleBom (Feeder/BOM) (N)
            │                               │
            │                               └─── QuotationSaleBomItem (Component) (N)
            │
            └─── Quotation (N) [Direct - if project not used]
```

---

### Project Relationships

**belongsTo:**
- Client (1:1) - Project belongs to one client

**hasMany:**
- Quotation (1:N) - Project can have multiple quotations

---

### Client Model (Related)

**File:** `app/Models/Client.php`  
**Table:** `clients`

**Relationships:**
```php
// Client belongsTo Organization
public function organization()
{
    return $this->belongsTo(Organization::class, 'OrganizationId', 'OrganizationId');
}

// Client hasMany Project
public function projects()
{
    return $this->hasMany(Project::class, 'ClientId', 'ClientId');
}

// Client hasMany Quotation
public function quotations()
{
    return $this->hasMany(Quotation::class, 'ClientId', 'ClientId');
}
```

---

### Organization Model (Related)

**File:** `app/Models/Organization.php`  
**Table:** `organizations`

**Relationships:**
```php
// Organization hasMany Client
public function clients()
{
    return $this->hasMany(Client::class, 'OrganizationId', 'OrganizationId');
}
```

---

### Quotation Model (Related)

**File:** `app/Models/Quotation.php`  
**Table:** `quotations`

**Relationships:**
```php
// Quotation belongsTo Project
public function project()
{
    return $this->belongsTo(Project::class, 'ProjectId', 'ProjectId');
}

// Quotation belongsTo Client
public function client()
{
    return $this->belongsTo(Client::class, 'ClientId', 'ClientId');
}
```

---

## 📊 Data Model Details

### Project Entity Attributes

**Required Fields:**
- `ClientId` - Must belong to existing client
- `Name` - Project name (required)

**Auto-Generated Fields:**
- `ProjectNo` - Auto-generated (YYMMDD001 format)

**Optional Fields:**
- `Location` - Project location
- `SpecificRequirement` - Specific requirements
- `DocumentReference` - Document reference
- `TemperatureMax` - Maximum temperature
- `TemperatureMin` - Minimum temperature
- `ClientName` - Legacy field (for backward compatibility)

---

### Project Number Format

**Format:** YYMMDD001

**Components:**
- YY - 2-digit year (e.g., 22 for 2022)
- MM - 2-digit month (e.g., 07 for July)
- DD - 2-digit day (e.g., 16)
- 001 - 3-digit sequential number (resets daily)

**Example:**
- July 16, 2022, First project: `220716001`
- July 16, 2022, Second project: `220716002`
- July 17, 2022, First project: `220717001`

---

## 🔍 Relationship Details

### Project → Client Relationship

**Type:** Many-to-One (N:1)

**Implementation:**
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

**Business Rules:**
- Project MUST belong to a client
- ClientId is required (NOT NULL)
- Cannot create project without client

---

### Project → Quotation Relationship

**Type:** One-to-Many (1:N)

**Implementation:**
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
- Project can have multiple quotations
- Quotation belongs to one project
- Cannot delete project if it has quotations

---

### Client → Project Relationship

**Type:** One-to-Many (1:N)

**Implementation:**
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
- Client can have multiple projects
- Each project belongs to one client

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial data models document | Part 2 of Project backend design series |

---

**Previous:** [Part 1: Foundation & Architecture](PROJECT_BACKEND_DESIGN_PART1_FOUNDATION.md)  
**Next:** [Part 3: Project Structure & Hierarchy](PROJECT_BACKEND_DESIGN_PART3_STRUCTURE.md)

