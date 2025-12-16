> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART1_FOUNDATION.md
> Bifurcated into: features/project/_general/PROJECT_BACKEND_DESIGN_PART1_FOUNDATION.md
> Module: Project > General
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 1: Foundation & Architecture

**Document:** PROJECT_BACKEND_DESIGN_PART1_FOUNDATION.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the foundational architecture and basic structure of the Project Backend System. The Project module is a core component that links clients to quotations and organizes work by project.

---

## 🏗️ Basic Structure

### System Architecture

The Project Backend follows a **layered architecture** pattern:

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│  (Blade Views, AJAX Endpoints, API Responses)            │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│                    CONTROLLER LAYER                       │
│  (ProjectController, Request Validation)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│                    MODEL LAYER                            │
│  (Eloquent ORM Models, Relationships)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│                    DATABASE LAYER                        │
│  (MySQL Tables, Foreign Keys, Indexes)                   │
└──────────────────────────────────────────────────────────┘
```

---

## 🧩 Core Components

### 1. Project Engine

**Purpose:** Main project management engine

**Key Components:**
- **ProjectController** - Main controller handling all project operations
- **Project Model** - Eloquent ORM model for data access
- **Request Classes** - Form request validation (StoreProjectRequest, UpdateProjectRequest)

**Location:**
- Controller: `app/Http/Controllers/ProjectController.php`
- Model: `app/Models/Project.php`
- Requests: `app/Http/Requests/StoreProjectRequest.php`, `app/Http/Requests/UpdateProjectRequest.php`

---

### 2. Data Models

**Project Models:**
- `Project` - Main project entity

**Related Models:**
- `Organization` - Company/organization master
- `Client` - Customer companies
- `Quotation` - Quotations linked to project

---

## 🎯 Design Principles

### 1. Separation of Concerns

**Rule:** Each layer has a specific responsibility

- **Controllers:** Handle HTTP requests, validate input, coordinate operations
- **Models:** Data access, relationships, basic validation
- **Views:** Presentation only, no business logic

**Example:**
```php
// Controller (ProjectController)
public function store(StoreProjectRequest $request) {
    // Validation handled by StoreProjectRequest
    // Generate project number
    $projectNo = $this->generateProjectNumber();
    
    // Create project
    $project = Project::create([
        'ProjectNo' => $projectNo,
        'ClientId' => $request->ClientId,
        'Name' => $request->Name,
        // ... other fields
    ]);
    
    // Return response
    return redirect()->route('project.index')
        ->with('success', 'Project created successfully');
}
```

---

### 2. Single Responsibility Principle

**Rule:** Each class/component does one thing well

- `ProjectController` - Only handles HTTP requests for projects
- `Project` Model - Only handles project data access
- `StoreProjectRequest` - Only validates project creation
- `UpdateProjectRequest` - Only validates project updates

---

### 3. Form Request Validation

**Rule:** Use FormRequest classes for validation

**Benefits:**
- Centralized validation logic
- Reusable validation rules
- Automatic error handling
- Clean controller code

**Example:**
```php
// StoreProjectRequest
public function rules() {
    return [
        'ClientId' => 'required|integer|exists:clients,ClientId',
        'Name' => 'required|string|max:255',
        'Location' => 'nullable|string|max:255',
        // ... other rules
    ];
}
```

---

### 4. Project Numbering System

**Rule:** Auto-generate project numbers with specific format

**Format:** YYMMDD001 (Year-Month-Day + Sequential Number)

**Rules:**
- Auto-generated by default
- Unique across all projects
- Sequential within day
- Daily reset

---

### 5. Soft Delete Pattern

**Rule:** Use Status column for soft delete (if implemented)

**Implementation:**
- Use `Status` column (0 = Active, 1 = Deleted)
- Filter by `->where('Status', 0)` when loading
- Note: Current implementation uses hard delete with validation

---

### 6. Relationship Integrity

**Rule:** Maintain referential integrity

**Implementation:**
- Project must belong to Client (ClientId required)
- Project can have multiple Quotations
- Cannot delete Project if it has Quotations

---

## 🛠️ Technology Stack

### Framework
- **Laravel** - PHP framework (version 8.x+)
- **Eloquent ORM** - Database abstraction layer

### Database
- **MySQL** - Relational database (InnoDB engine)
- **Foreign Keys** - Referential integrity
- **Indexes** - Performance optimization

### Request Validation
- **FormRequest** - Laravel form request validation
- `StoreProjectRequest` - Project creation validation
- `UpdateProjectRequest` - Project update validation

---

## 📊 System Flow

### Request Flow

```
1. HTTP Request → ProjectController
2. Controller validates input (via FormRequest)
3. Controller generates project number (if needed)
4. Controller creates/updates/deletes project
5. Controller formats response (redirect/JSON)
6. Response sent to client
```

### Data Flow

```
1. User creates project → Project model
2. System generates ProjectNo (YYMMDD001)
3. Project linked to Client
4. User creates quotations → Quotation model
5. Quotations linked to Project
6. System displays project with quotations
```

---

## 🔗 Project in System Context

### Position in Hierarchy

```
Organization
  └── Client
      └── Project
          └── Quotation
              └── QuotationSale (Panel)
                  └── QuotationSaleBom (Feeder/BOM)
                      └── QuotationSaleBomItem (Component)
```

### Purpose

**Project serves as:**
- Organizational unit for client work
- Link between Client and Quotation
- Grouping mechanism for quotations
- Project tracking and management

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial foundation document | Part 1 of Project backend design series |

---

**Next:** [Part 2: Data Models & Relationships](PROJECT_BACKEND_DESIGN_PART2_DATA_MODELS.md)

