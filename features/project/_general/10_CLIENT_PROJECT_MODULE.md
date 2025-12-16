> Source: source_snapshot/docs/03_MODULES/10_CLIENT_PROJECT_MODULE.md
> Bifurcated into: features/project/_general/10_CLIENT_PROJECT_MODULE.md
> Module: Project > General
> Date: 2025-12-17 (IST)

# Client & Project Module

**Document:** 10_CLIENT_PROJECT_MODULE.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Module Overview

**Purpose:** Manage clients, contacts, and projects

**Controllers:** 3 (ClientController, ContactController, ProjectController)  
**Models:** 4 (Client, Contact, Project, Organization)  
**Database Tables:** 4

---

## Module Structure

```
RELATIONSHIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Organization (1) ──→ (N) Client
Client (1) ──→ (N) Contact
Client (1) ──→ (N) Project
Project (1) ──→ (N) Quotation
```

---

## Clients

### Client Table Schema

```sql
ClientId         INT PRIMARY KEY
OrganizationId   INT FK → organizations
ClientName       VARCHAR(255) NOT NULL
Email            VARCHAR(255)
Mobile           VARCHAR(20)
Address          TEXT
CountryId        INT FK → countries
StateId          INT FK → states
CityName         VARCHAR(100)
PinCode          VARCHAR(20)
GSTNo            VARCHAR(50)
PANNo            VARCHAR(50)
TANNo            VARCHAR(50)
AddharNo         VARCHAR(50)
Website          VARCHAR(255)
Status           TINYINT DEFAULT 0
created_at       TIMESTAMP
updated_at       TIMESTAMP
```

### Client Controller Methods

**ClientController.php** (151 lines)

- index() - List clients
- create() - Show create form
- store() - Save client
- edit($id) - Show edit form
- update($id) - Update client
- destroy($id) - Soft delete
- getState($id) - AJAX get states by country

### Client Business Rules

**Required:**
- ClientName

**Validation:**
- Email must be valid format
- Mobile must be numeric
- GST format validation (optional)
- PAN format validation (optional)

**Relationships:**
- Can have multiple contacts
- Can have multiple projects
- Can have multiple quotations

---

## Contacts

### Contact Table Schema

```sql
ContactId       INT PRIMARY KEY
ClientId        INT FK → clients NOT NULL
ContactName     VARCHAR(255) NOT NULL
Email           VARCHAR(255)
Mobile          VARCHAR(20)
Phone           VARCHAR(20)
Designation     VARCHAR(100)
Status          TINYINT DEFAULT 0
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### Contact Controller

**ContactController.php** (97 lines)

Standard CRUD operations

### Contact Business Rules

**Required:**
- ClientId (must belong to client)
- ContactName

**Purpose:**
- Contact persons for client
- Used in quotations (who receives quote)
- Can have multiple per client

---

## Projects

### Project Table Schema

```sql
ProjectId       INT PRIMARY KEY
ClientId        INT FK → clients NOT NULL
ProjectNo       VARCHAR(20) UNIQUE NOT NULL
Name            VARCHAR(255) NOT NULL
Location        VARCHAR(255)
Status          TINYINT DEFAULT 0
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### Project Number Generation

**Format:** YYMMDD###

**Same algorithm as quotations:**
```php
$date = date('ymd');
$maxNo = DB::select(
    "SELECT MAX(RIGHT(ProjectNo, 3)) as max 
     FROM projects 
     WHERE ProjectNo LIKE ?",
    [$date.'%']
)[0]->max;

$sequential = $maxNo ? ($maxNo + 1) : 1;
$ProjectNo = $date . str_pad($sequential, 3, '0', STR_PAD_LEFT);
```

### Project Business Rules

**Required:**
- ClientId
- Name

**Auto-generated:**
- ProjectNo

**Purpose:**
- Track client projects
- Link quotations to projects
- Organize work by project

---

## Organizations

### Organization Table Schema

```sql
OrganizationId  INT PRIMARY KEY
Name            VARCHAR(255) NOT NULL
Address         TEXT
Contact         VARCHAR(20)
Email           VARCHAR(255)
Status          TINYINT DEFAULT 0
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

**Purpose:** Group clients by parent organization

**Example:**
```
Organization: TATA Group
├── Client: TATA Motors
├── Client: TATA Steel
└── Client: TATA Power
```

---

## Workflows

### Create Client Workflow

```
1. Navigate to Clients → Create Client
2. Fill form:
   - Organization (optional)
   - Client Name *
   - Email, Mobile
   - Address
   - Country, State, City
   - GST, PAN numbers
3. Save
4. Add contacts for client
5. Create projects for client
```

### Create Project Workflow

```
1. Navigate to Projects → Create Project
2. Select Client *
3. Enter Project Name *
4. Enter Location
5. Project Number auto-generated
6. Save
7. Create quotations for project
```

---

## Summary

**Purpose:** Foundation for quotation system  
**Hierarchy:** Organization → Client → Contact/Project → Quotation  
**Key Feature:** Auto-generated project numbers  
**Best Practice:** Set up clients/projects before creating quotations

---

**End of Document 10 - Client/Project Module**

[← Back: BOM Module](09_BOM_MODULE.md) | [Next: Pricing Module →](11_PRICING_MODULE.md)

