> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART5_RULES.md
> Bifurcated into: features/project/status_approvals/PROJECT_BACKEND_DESIGN_PART5_RULES.md
> Module: Project > Status/Approvals
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 5: Business Rules & Validation

**Document:** PROJECT_BACKEND_DESIGN_PART5_RULES.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes all business rules, validation rules, and constraints for the Project module.

---

## ✅ Validation Rules

### Project Creation Rules (StoreProjectRequest)

**File:** `app/Http/Requests/StoreProjectRequest.php`

**Validation Rules:**
```php
[
    'ClientId'            => 'required|integer|exists:clients,ClientId',
    'Name'                 => 'required|string|max:255',
    'Location'             => 'nullable|string|max:255',
    'ClientName'           => 'nullable|string|max:255', // Legacy support
    'DocumentReference'    => 'nullable|string|max:255',
    'SpecificRequirement'  => 'nullable|string|max:1000',
    'TemperatureMax'       => 'nullable|numeric|min:-100|max:100',
    'TemperatureMin'       => 'nullable|numeric|min:-100|max:100',
]
```

**Required Fields:**
- `ClientId` - Must exist in clients table
- `Name` - Project name (required)

**Optional Fields:**
- All other fields are optional

---

### Project Update Rules (UpdateProjectRequest)

**File:** `app/Http/Requests/UpdateProjectRequest.php`

**Validation Rules:**
```php
[
    'ClientId'            => 'required|integer|exists:clients,ClientId',
    'Name'                 => 'required|string|max:255',
    'Location'             => 'nullable|string|max:255',
    'ClientName'           => 'nullable|string|max:255', // Legacy support
    'DocumentReference'    => 'nullable|string|max:255',
    'SpecificRequirement'  => 'nullable|string|max:1000',
    'TemperatureMax'       => 'nullable|numeric|min:-100|max:100',
    'TemperatureMin'       => 'nullable|numeric|min:-100|max:100',
]
```

**Note:** Same rules as creation (StoreProjectRequest)

---

## 🔒 Business Rules

### Rule 1: Client Required

**Rule:** Project MUST belong to a client

**Implementation:**
- `ClientId` is required (NOT NULL in database)
- Validation: `'ClientId' => 'required|integer|exists:clients,ClientId'`
- Cannot create project without client

**Enforcement:**
- Database constraint: NOT NULL
- FormRequest validation: required
- Controller validation: checks existence

---

### Rule 2: Project Name Required

**Rule:** Project name is mandatory

**Implementation:**
- `Name` is required (NOT NULL in database)
- Validation: `'Name' => 'required|string|max:255'`
- Must be descriptive and meaningful

---

### Rule 3: Project Number Uniqueness

**Rule:** Project number must be unique

**Implementation:**
- Database constraint: UNIQUE KEY on `ProjectNo`
- Auto-generated if not provided
- Manual entry validated for uniqueness

**Enforcement:**
- Database UNIQUE constraint
- Application-level validation (if manual entry)

---

### Rule 4: Cannot Delete Project with Quotations

**Rule:** Project cannot be deleted if it has quotations

**Implementation:**
```php
public function destroy($ProjectId)
{
    $quotations = Quotation::where('ProjectId', $ProjectId)->first();
    if ($quotations) {
        return [
            'message' => 'There are many Quotations linked to this Project.',
            'success' => 'error'
        ];
    }
    
    Project::where('ProjectId', $ProjectId)->delete();
    return [
        'message' => 'Project deleted successfully.',
        'success' => 'success'
    ];
}
```

**Business Logic:**
- Check if project has any quotations
- If yes, prevent deletion
- If no, allow deletion

---

### Rule 5: Temperature Range Validation

**Rule:** Temperature values must be within valid range

**Implementation:**
- `TemperatureMax`: nullable, numeric, min -100, max 100
- `TemperatureMin`: nullable, numeric, min -100, max 100
- Both optional (default 0 if not provided)

**Validation:**
```php
'TemperatureMax' => 'nullable|numeric|min:-100|max:100',
'TemperatureMin' => 'nullable|numeric|min:-100|max:100',
```

---

### Rule 6: String Length Limits

**Rule:** String fields have maximum length limits

**Implementation:**
- `Name`: max 255 characters
- `Location`: max 255 characters
- `ClientName`: max 255 characters (legacy)
- `DocumentReference`: max 255 characters
- `SpecificRequirement`: max 1000 characters

**Validation:**
```php
'Name' => 'required|string|max:255',
'Location' => 'nullable|string|max:255',
'SpecificRequirement' => 'nullable|string|max:1000',
```

---

## 🚫 Constraints

### Database Constraints

**Primary Key:**
- `ProjectId` - PRIMARY KEY, auto-increment

**Unique Constraint:**
- `ProjectNo` - UNIQUE KEY

**Foreign Key:**
- `ClientId` - FOREIGN KEY to `clients.ClientId`, NOT NULL

**Indexes:**
- PRIMARY KEY (ProjectId)
- UNIQUE KEY (ProjectNo)
- INDEX (ClientId)

---

### Application Constraints

**Referential Integrity:**
- Project must belong to existing client
- Cannot delete client if it has projects (enforced at client level)
- Cannot delete project if it has quotations (enforced at project level)

**Data Integrity:**
- ProjectNo must be unique
- ClientId must reference valid client
- Name must be provided

---

## 📝 Validation Messages

### Custom Error Messages

**StoreProjectRequest:**
```php
public function messages()
{
    return [
        'ClientId.required' => 'Client is required for a project.',
        'ClientId.exists' => 'Selected client does not exist.',
        'Name.required' => 'Project name is required.',
        'Name.max' => 'Project name cannot exceed 255 characters.',
    ];
}
```

**UpdateProjectRequest:**
```php
public function messages()
{
    return [
        'ClientId.required' => 'Client is required.',
        'ClientId.exists' => 'Selected client does not exist.',
        'ClientId.integer' => 'Client ID must be a valid number.',
        'Name.required' => 'Project name is required.',
        'Name.max' => 'Project name cannot exceed 255 characters.',
        'Location.max' => 'Location cannot exceed 255 characters.',
    ];
}
```

---

## 🔍 Deletion Rules

### Deletion Validation

**Rule:** Check for dependent records before deletion

**Implementation:**
```php
public function destroy($ProjectId)
{
    // Check if project has quotations
    $quotations = Quotation::where('ProjectId', $ProjectId)->first();
    
    if ($quotations) {
        // Cannot delete - has quotations
        return [
            'message' => 'There are many Quotations linked to this Project.',
            'success' => 'error'
        ];
    }
    
    // Safe to delete
    Project::where('ProjectId', $ProjectId)->delete();
    return [
        'message' => 'Project deleted successfully.',
        'success' => 'success'
    ];
}
```

**Business Logic:**
1. Check if project has quotations
2. If yes → Return error, prevent deletion
3. If no → Delete project, return success

**Note:** Current implementation uses hard delete. Consider implementing soft delete (Status column) for audit trail.

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial business rules document | Part 5 of Project backend design series |

---

**Previous:** [Part 4: Project Numbering System](PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md)  
**Next:** [Part 6: Backend Services & Controllers](PROJECT_BACKEND_DESIGN_PART6_SERVICES.md)

