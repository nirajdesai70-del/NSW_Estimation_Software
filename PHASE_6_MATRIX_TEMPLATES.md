# Phase 6 Matrix Templates
## Templates for All Detailed Matrices

**Date:** 2025-01-27  
**Status:** TEMPLATES  
**Purpose:** Standard templates for all Phase 6 matrices

---

## 📊 Matrix 1: Work Breakdown Matrix

### Template Structure

```markdown
| Track | Work Item ID | Work Item Name | Sub-Item ID | Sub-Item Name | Description | Status | Owner | Dependencies | Estimated Time | Actual Time | Start Date | End Date | Notes |
|-------|--------------|----------------|-------------|---------------|-------------|--------|-------|--------------|----------------|-------------|------------|----------|-------|
| A | A-001 | Quotation UI | A-001-01 | Panel Management | Create panel management UI | TODO | TBD | E-001 | 40h | - | TBD | TBD | - |
| A | A-001 | Quotation UI | A-001-02 | Feeder Management | Create feeder management UI | TODO | TBD | A-001-01 | 40h | - | TBD | TBD | - |
```

### Column Definitions

- **Track:** Track identifier (A, A-R, B, C, D0, D, E, F, G, H, I, J, K, L, M)
- **Work Item ID:** Unique identifier for work item
- **Work Item Name:** Name of work item
- **Sub-Item ID:** Unique identifier for sub-item
- **Sub-Item Name:** Name of sub-item
- **Description:** Detailed description
- **Status:** TODO | IN_PROGRESS | DONE | BLOCKED
- **Owner:** Person responsible
- **Dependencies:** IDs of dependent items
- **Estimated Time:** Estimated hours
- **Actual Time:** Actual hours spent
- **Start Date:** Actual start date
- **End Date:** Actual end date
- **Notes:** Additional notes

---

## 📊 Matrix 2: Rules Matrix

### Template Structure

```markdown
| Rule ID | Rule Category | Rule Name | Rule Description | Applies To | Priority | Status | Reference | Notes |
|---------|---------------|-----------|------------------|------------|----------|--------|-----------|-------|
| RULE-001 | Governance | Phase 6 First Rule | Phase 6 logic prevails over NEPL | All | HIGH | ACTIVE | PHASE_6_GOVERNANCE_RULES.md | - |
| RULE-002 | Business | Customer Snapshot | Always store customer_name_snapshot | Quotation | HIGH | ACTIVE | D-009 | - |
```

### Column Definitions

- **Rule ID:** Unique identifier
- **Rule Category:** Governance | Business | Technical | Validation | Workflow | Security
- **Rule Name:** Short name
- **Rule Description:** Detailed description
- **Applies To:** Where rule applies
- **Priority:** HIGH | MEDIUM | LOW
- **Status:** ACTIVE | INACTIVE | DEPRECATED
- **Reference:** Document reference
- **Notes:** Additional notes

---

## 📊 Matrix 3: Tasks & Todos Matrix

### Template Structure

```markdown
| Task ID | Track | Task Name | Description | Type | Priority | Status | Assigned To | Dependencies | Estimated Time | Actual Time | Start Date | End Date | Notes |
|---------|-------|-----------|-------------|------|----------|--------|-------------|--------------|----------------|-------------|------------|----------|-------|
| P6-SETUP-001 | E | Database Setup | Setup database from Schema Canon | SETUP | HIGH | TODO | TBD | - | 8h | - | TBD | TBD | - |
| P6-ENTRY-001 | - | Entry Gate 1 | Verify Phase 5 completion | ENTRY | HIGH | TODO | TBD | - | 2h | - | TBD | TBD | - |
```

### Column Definitions

- **Task ID:** Unique identifier
- **Track:** Track identifier (if applicable)
- **Task Name:** Short name
- **Description:** Detailed description
- **Type:** SETUP | ENTRY | UI | VAL | DB | REUSE | COST | OTHER
- **Priority:** HIGH | MEDIUM | LOW
- **Status:** TODO | IN_PROGRESS | DONE | BLOCKED | CANCELLED
- **Assigned To:** Person responsible
- **Dependencies:** Task IDs this depends on
- **Estimated Time:** Estimated hours
- **Actual Time:** Actual hours spent
- **Start Date:** Actual start date
- **End Date:** Actual end date
- **Notes:** Additional notes

---

## 📊 Matrix 4: Workflow Matrix

### Template Structure

```markdown
| Workflow ID | Workflow Name | Workflow Type | Steps | Rules | Triggers | Outcomes | Status | Diagram | Notes |
|-------------|---------------|---------------|-------|-------|----------|----------|--------|---------|-------|
| WF-001 | Quotation Creation | Quotation | 1. Create quotation<br>2. Add panels<br>3. Add feeders | RULE-001, RULE-002 | User action | Quotation created | ACTIVE | [Link] | - |
| WF-002 | Panel Creation | Panel | 1. Select quotation<br>2. Create panel<br>3. Set quantity | RULE-003 | User action | Panel created | ACTIVE | [Link] | - |
```

### Column Definitions

- **Workflow ID:** Unique identifier
- **Workflow Name:** Short name
- **Workflow Type:** Quotation | Panel | Feeder | BOM | Item | Reuse | Costing | Approval | Import | Export
- **Steps:** Numbered list of steps
- **Rules:** Rule IDs that apply
- **Triggers:** What triggers workflow
- **Outcomes:** Expected outcomes
- **Status:** ACTIVE | INACTIVE | DEPRECATED
- **Diagram:** Link to workflow diagram
- **Notes:** Additional notes

---

## 📊 Matrix 5: Sequence & Dependencies Matrix

### Template Structure

```markdown
| Item ID | Item Name | Item Type | Predecessors | Successors | Sequence Number | Critical Path | Parallel Possible | Blocking | Notes |
|---------|-----------|-----------|--------------|------------|-----------------|---------------|-------------------|----------|-------|
| A-001 | Quotation UI | Work Item | E-001 | A-002 | 10 | YES | NO | NO | - |
| A-002 | Panel Management | Work Item | A-001 | A-003 | 11 | YES | NO | NO | - |
```

### Column Definitions

- **Item ID:** Unique identifier
- **Item Name:** Short name
- **Item Type:** TRACK | WORK_ITEM | TASK | WORKFLOW_STEP | GATE
- **Predecessors:** IDs of items that must complete first
- **Successors:** IDs of items that come after
- **Sequence Number:** Order in sequence
- **Critical Path:** YES | NO
- **Parallel Possible:** YES | NO
- **Blocking:** YES | NO (blocks other items)
- **Notes:** Additional notes

---

## 📊 Matrix 6: Gap Analysis Matrix

### Template Structure

```markdown
| Gap ID | Gap Category | Gap Description | Severity | Impact | Current State | Required State | Gap Closure Plan | Owner | Target Date | Status |
|--------|--------------|-----------------|----------|--------|---------------|----------------|------------------|-------|-------------|--------|
| GAP-001 | Scope | Missing Organization Management | HIGH | Cannot create organizations | Not implemented | Full CRUD for organizations | Track F implementation | TBD | TBD | OPEN |
| GAP-002 | Task | Missing Auto-Naming Service | MEDIUM | Manual naming required | Not implemented | Auto-naming service | Add to Track F or Track A | TBD | TBD | OPEN |
```

### Column Definitions

- **Gap ID:** Unique identifier
- **Gap Category:** Scope | Task | Rule | Workflow | Documentation | Technical | Integration
- **Gap Description:** Detailed description
- **Severity:** HIGH | MEDIUM | LOW
- **Impact:** Description of impact
- **Current State:** What exists now
- **Required State:** What is needed
- **Gap Closure Plan:** How to close gap
- **Owner:** Person responsible
- **Target Date:** Target closure date
- **Status:** OPEN | IN_PROGRESS | CLOSED | DEFERRED

---

## 📊 Matrix 7: Master Matrix

### Template Structure

```markdown
| ID | Type | Name | Work Breakdown | Rules | Tasks | Workflows | Sequence | Gaps | Status |
|----|------|------|----------------|-------|-------|-----------|----------|------|--------|
| A-001 | Work Item | Quotation UI | A-001 | RULE-001, RULE-002 | P6-UI-001, P6-UI-002 | WF-001 | 10 | GAP-001 | IN_PROGRESS |
```

### Column Definitions

- **ID:** Unique identifier
- **Type:** TRACK | WORK_ITEM | TASK | WORKFLOW | RULE | GAP
- **Name:** Short name
- **Work Breakdown:** Related work breakdown IDs
- **Rules:** Related rule IDs
- **Tasks:** Related task IDs
- **Workflows:** Related workflow IDs
- **Sequence:** Sequence number
- **Gaps:** Related gap IDs
- **Status:** Overall status

---

## 🎯 Usage Guidelines

### Matrix Population Order

1. **Start with Gap Analysis Matrix** (Priority 1)
   - Identify all gaps first
   - This informs all other matrices

2. **Create Work Breakdown Matrix**
   - Break down all work
   - Identify all work items

3. **Create Rules Matrix**
   - Document all rules
   - Link to work items

4. **Create Tasks & Todos Matrix**
   - List all tasks
   - Link to work items

5. **Create Workflow Matrix**
   - Define all workflows
   - Link to tasks and rules

6. **Create Sequence & Dependencies Matrix**
   - Map execution order
   - Identify dependencies

7. **Create Master Matrix**
   - Link all matrices together
   - Provide unified view

---

### Matrix Maintenance

- **Update Frequency:** Weekly
- **Owner:** Phase 6 Team
- **Validation:** Cross-matrix validation required
- **Version Control:** Git tracked

---

**Status:** TEMPLATES READY  
**Next Action:** Begin populating matrices starting with Gap Analysis
