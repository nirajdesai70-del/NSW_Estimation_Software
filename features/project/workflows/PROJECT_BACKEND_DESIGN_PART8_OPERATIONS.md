> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART8_OPERATIONS.md
> Bifurcated into: features/project/workflows/PROJECT_BACKEND_DESIGN_PART8_OPERATIONS.md
> Module: Project > Workflows
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 8: Operation Level Details

**Document:** PROJECT_BACKEND_DESIGN_PART8_OPERATIONS.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document provides detailed operation-level workflows for all major operations in the Project module.

---

## 🔄 Operation 1: Create Project

### Step-by-Step Operation Flow

**Step 1: Validate Input**
```php
// StoreProjectRequest validates:
// - ClientId: required|integer|exists:clients,ClientId
// - Name: required|string|max:255
// - Location: nullable|string|max:255
// - Other optional fields
```

**Step 2: Generate Project Number**
```php
$date = date('ymd'); // e.g., 220716

$result = DB::select(
    "SELECT CONCAT(?, LPAD(CAST(MAX(RIGHT(ProjectNo, 3)) + 1 AS CHAR), 3, '0')) AS MaxNumber 
     FROM projects 
     WHERE ProjectNo LIKE ?",
    [$date, $date.'%']
);

$ProjectNo = $result[0]->MaxNumber ?? $date.'001';
```

**Step 3: Prepare Project Data**
```php
$project = [
    'ProjectNo' => $ProjectNo,
    'ClientId' => $request->ClientId,
    'Name' => $request->Name,
    'Location' => $request->Location ?? '',
    'ClientName' => $request->ClientName ?? '', // Legacy
    'DocumentReference' => $request->DocumentReference ?? '',
    'SpecificRequirement' => $request->SpecificRequirement ?? '',
    'TemperatureMax' => $request->TemperatureMax ?? 0,
    'TemperatureMin' => $request->TemperatureMin ?? 0,
];
```

**Step 4: Create Project Record**
```php
$newProject = Project::create($project);
```

**Step 5: Handle Response**
```php
// AJAX request
if ($request->ajax() || $request->wantsJson()) {
    return response()->json([
        'ProjectId' => $newProject->ProjectId,
        'Name' => $newProject->Name,
    ]);
}

// Regular request
return redirect()->route('project.index')
    ->with('success', __('project added successfully.'));
```

---

## 🔄 Operation 2: Update Project

### Step-by-Step Operation Flow

**Step 1: Validate Input**
```php
// UpdateProjectRequest validates:
// - ClientId: required|integer|exists:clients,ClientId
// - Name: required|string|max:255
// - Other fields (same as creation)
```

**Step 2: Update Project Record**
```php
Project::where('ProjectId', $ProjectId)->update([
    'ClientId' => $request->ClientId,
    'Name' => $request->Name,
    'Location' => $request->Location,
    'ClientName' => $request->ClientName ?? '', // Legacy
    'SpecificRequirement' => $request->SpecificRequirement,
    'DocumentReference' => $request->DocumentReference,
    'TemperatureMax' => $request->TemperatureMax ?? 0,
    'TemperatureMin' => $request->TemperatureMin ?? 0
]);
```

**Step 3: Return Response**
```php
return redirect()->route('project.index')
    ->with('success', __('Project updated successfully.'));
```

---

## 🔄 Operation 3: Delete Project

### Step-by-Step Operation Flow

**Step 1: Check for Dependent Records**
```php
$quotations = Quotation::where('ProjectId', $ProjectId)->first();
```

**Step 2: Validate Deletion**
```php
if ($quotations) {
    // Cannot delete - has quotations
    return [
        'message' => 'There are many Quotations linked to this Project.',
        'success' => 'error'
    ];
}
```

**Step 3: Delete Project**
```php
Project::where('ProjectId', $ProjectId)->delete();
```

**Step 4: Return Response**
```php
return [
    'message' => 'Project deleted successfully.',
    'success' => 'success'
];
```

---

## 🔄 Operation 4: List Projects

### Step-by-Step Operation Flow

**Step 1: Get Pagination Parameter**
```php
$perPage = $request->get('per_page', 25);
```

**Step 2: Load Projects with Client**
```php
$project = Project::with('client')
    ->orderBy('Name')
    ->paginate($perPage)
    ->appends($request->query());
```

**Step 3: Define Table Columns**
```php
$columns = [
    ['key' => 'Name', 'label' => 'Project Name', 'sortable' => true],
    ['key' => 'client_name', 'label' => 'Client', 'render' => function($p) {
        return e(optional($p->client)->ClientName ?? $p->ClientName ?? '-');
    }],
    ['key' => 'Location', 'label' => 'Location', 'sortable' => false],
    ['key' => 'TemperatureMax', 'label' => 'Temp Max', 'sortable' => false],
    ['key' => 'TemperatureMin', 'label' => 'Temp Min', 'sortable' => false],
];
```

**Step 4: Define Action Buttons**
```php
$actions = [
    ['type' => 'edit', 'route' => 'project.edit', 'param' => 'ProjectId'],
    ['type' => 'delete', 'route' => 'project.destroy', 'param' => 'ProjectId'],
];
```

**Step 5: Return View**
```php
return view('project.index', compact('project', 'columns', 'actions'));
```

---

## 🔄 Operation 5: View Project Details

### Step-by-Step Operation Flow

**Step 1: Load Project**
```php
$project = Project::where('ProjectId', $projectId)->firstOrFail();
```

**Step 2: Load Clients for Dropdown**
```php
$client = Client::pluck('ClientName', 'ClientId')->toArray();
```

**Step 3: Load Quotations with Pagination**
```php
$quotations = Quotation::where('ProjectId', $project->ProjectId)
    ->where('Status', 0)
    ->with('client') // Eager load to prevent N+1
    ->orderBy('QuotationNo', 'DESC')
    ->paginate(10); // 10 per page for performance
```

**Step 4: Attach Quotations to Project**
```php
$project->setRelation('quotations', $quotations);
```

**Step 5: Return View**
```php
return view('project.edit', compact('project', 'quotations', 'client'));
```

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial operations document | Part 8 of Project backend design series |

---

**Previous:** [Part 7: Master Data Integration](PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md)  
**Next:** [Part 9: Logic Level Details](PROJECT_BACKEND_DESIGN_PART9_LOGIC.md)

