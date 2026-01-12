---
Source: features/project/structure/PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T02:09:17.749017
KB_Path: phase5_pack/04_RULES_LIBRARY/features/PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md
---

> Source: source_snapshot/PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md
> Bifurcated into: features/project/structure/PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md
> Module: Project > Structure
> Date: 2025-12-17 (IST)

# Project Backend Design - Part 4: Project Numbering System

**Document:** PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the project numbering system, including format, generation algorithm, uniqueness rules, and sequential numbering logic.

---

## 🔢 Project Number Format

### Format Pattern

**Pattern:** YYMMDD###

**Components:**
- **YY** - 2-digit year (e.g., 22 for 2022, 25 for 2025)
- **MM** - 2-digit month (01-12)
- **DD** - 2-digit day (01-31)
- **###** - 3-digit sequential number (001-999)

**Example:**
```
220716001 = July 16, 2022, Project #1
220716002 = July 16, 2022, Project #2
220717001 = July 17, 2022, Project #1 (resets daily)
```

---

## 🧮 Number Generation Algorithm

### Step-by-Step Algorithm

**Step 1: Get Current Date**
```php
$date = date('ymd'); // Returns: 220716 (for July 16, 2022)
```

**Step 2: Query Existing Projects for Today**
```php
$v_StartNo1 = DB::select(
    "SELECT CONCAT(?, LPAD(CAST(MAX(RIGHT(ProjectNo, 3)) + 1 AS CHAR), 3, '0')) AS MaxNumber 
     FROM projects 
     WHERE ProjectNo LIKE ?",
    [$date, $date.'%']
);
```

**Step 3: Determine Next Number**
```php
$ProjectNo = $v_StartNo1[0]->MaxNumber != null 
    ? $v_StartNo1[0]->MaxNumber 
    : $date.'001';
```

**Complete Function:**
```php
protected function generateProjectNumber()
{
    $date = date('ymd');
    
    $result = DB::select(
        "SELECT CONCAT(?, LPAD(CAST(MAX(RIGHT(ProjectNo, 3)) + 1 AS CHAR), 3, '0')) AS MaxNumber 
         FROM projects 
         WHERE ProjectNo LIKE ?",
        [$date, $date.'%']
    );
    
    return $result[0]->MaxNumber ?? $date.'001';
}
```

---

## 📐 Algorithm Details

### SQL Query Breakdown

**Query Purpose:** Find the highest sequential number for today and increment it

**Query Components:**
1. `CONCAT(?, ...)` - Concatenate date prefix with sequential number
2. `LPAD(CAST(MAX(RIGHT(ProjectNo, 3)) + 1 AS CHAR), 3, '0')` - Get max number, add 1, pad to 3 digits
3. `WHERE ProjectNo LIKE ?` - Filter by today's date prefix
4. `$date.'%'` - Pattern match (e.g., "220716%")

**Example Execution:**
```
Date: 220716
Existing Projects:
  - 220716001
  - 220716002
  - 220716003

Query finds MAX(RIGHT(ProjectNo, 3)) = 003
Adds 1 = 004
LPAD to 3 digits = 004
CONCAT with date = 220716004

Result: 220716004
```

---

## 🔒 Uniqueness Rules

### Rule 1: Unique Constraint

**Database Constraint:**
- `ProjectNo` has UNIQUE constraint
- Prevents duplicate project numbers
- Database enforces uniqueness

**Implementation:**
```sql
UNIQUE KEY (ProjectNo)
```

---

### Rule 2: Daily Reset

**Rule:** Sequential number resets each day

**Example:**
```
July 16, 2022:
  - First project: 220716001
  - Second project: 220716002
  - Third project: 220716003

July 17, 2022:
  - First project: 220717001 (resets to 001)
  - Second project: 220717002
```

**Why:** Date prefix changes, so sequential number can reset

---

### Rule 3: Sequential Within Day

**Rule:** Numbers increment sequentially within same day

**Example:**
```
Same day (220716):
  220716001
  220716002
  220716003
  (cannot skip numbers)
```

---

### Rule 4: Manual Override

**Rule:** User can manually enter project number

**Implementation:**
- If user provides `ProjectNo` in request, use it
- System validates uniqueness
- If not provided, auto-generate

**Code:**
```php
if ($request->has('ProjectNo') && !empty($request->ProjectNo)) {
    // Validate uniqueness
    $exists = Project::where('ProjectNo', $request->ProjectNo)->exists();
    if ($exists) {
        return redirect()->back()
            ->with('error', 'Project number already exists');
    }
    $projectNo = $request->ProjectNo;
} else {
    $projectNo = $this->generateProjectNumber();
}
```

---

## 🔄 Number Generation Flow

### Complete Flow

```
START: Generate Project Number
│
├─→ Step 1: Check if Manual Number Provided
│   │
│   ├─→ IF ProjectNo provided in request
│   │   │
│   │   ├─→ Validate uniqueness
│   │   │   │
│   │   │   ├─→ IF exists
│   │   │   │   └─→ RETURN error (number already exists)
│   │   │   │
│   │   │   └─→ ELSE
│   │   │       └─→ USE provided number
│   │   │
│   │   └─→ END IF
│   │
│   └─→ ELSE
│       └─→ CONTINUE to Step 2
│
├─→ Step 2: Get Current Date
│   │
│   └─→ date = date('ymd') // e.g., 220716
│
├─→ Step 3: Query Database
│   │
│   ├─→ Find MAX sequential number for today
│   │
│   └─→ Query: SELECT MAX(RIGHT(ProjectNo, 3)) FROM projects WHERE ProjectNo LIKE '220716%'
│
├─→ Step 4: Calculate Next Number
│   │
│   ├─→ IF max number found
│   │   └─→ nextNumber = maxNumber + 1
│   │
│   └─→ ELSE
│       └─→ nextNumber = 1
│
├─→ Step 5: Format Number
│   │
│   ├─→ Pad to 3 digits: LPAD(nextNumber, 3, '0')
│   │
│   └─→ Concatenate: date + paddedNumber
│
└─→ END: RETURN ProjectNo
```

---

## 📊 Examples

### Example 1: First Project of Day

**Date:** July 16, 2022  
**Existing Projects:** None for today

**Calculation:**
```
date = 220716
maxNumber = NULL (no projects today)
nextNumber = 1
paddedNumber = 001
ProjectNo = 220716001
```

---

### Example 2: Subsequent Project Same Day

**Date:** July 16, 2022  
**Existing Projects:** 220716001, 220716002, 220716003

**Calculation:**
```
date = 220716
maxNumber = 003
nextNumber = 003 + 1 = 4
paddedNumber = 004
ProjectNo = 220716004
```

---

### Example 3: First Project Next Day

**Date:** July 17, 2022  
**Existing Projects:** 220716001, 220716002 (from previous day)

**Calculation:**
```
date = 220717 (different date)
maxNumber = NULL (no projects for 220717)
nextNumber = 1
paddedNumber = 001
ProjectNo = 220717001 (resets to 001)
```

---

## 🔍 Edge Cases

### Case 1: Maximum Sequential Number (999)

**Scenario:** 999 projects created in one day

**Handling:**
- System can handle up to 999 projects per day
- If 1000th project attempted, number would be 2207161000 (4 digits)
- **Recommendation:** Add validation to prevent > 999 per day, or extend format

---

### Case 2: Concurrent Creation

**Scenario:** Multiple users create projects simultaneously

**Handling:**
- Database UNIQUE constraint prevents duplicates
- If two users get same number, second insert fails
- Application should retry with next number

**Recommendation:**
```php
$maxRetries = 3;
$retry = 0;
while ($retry < $maxRetries) {
    try {
        $projectNo = $this->generateProjectNumber();
        $project = Project::create(['ProjectNo' => $projectNo, ...]);
        break; // Success
    } catch (\Illuminate\Database\QueryException $e) {
        if ($e->getCode() == 23000) { // Duplicate entry
            $retry++;
            continue;
        }
        throw $e;
    }
}
```

---

### Case 3: Manual Number Conflict

**Scenario:** User provides project number that already exists

**Handling:**
- Validation checks uniqueness
- Returns error if exists
- User must provide different number or let system generate

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial numbering document | Part 4 of Project backend design series |

---

**Previous:** [Part 3: Project Structure & Hierarchy](PROJECT_BACKEND_DESIGN_PART3_STRUCTURE.md)  
**Next:** [Part 5: Business Rules & Validation](PROJECT_BACKEND_DESIGN_PART5_RULES.md)

