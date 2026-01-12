---
Source: changes/project/migration/PROJECT_V2_IMPLEMENTATION_PLAN.md
KB_Namespace: changes
Status: WORKING
Last_Updated: 2025-12-17T02:09:20.643383
KB_Path: phase5_pack/04_RULES_LIBRARY/changes/PROJECT_V2_IMPLEMENTATION_PLAN.md
---

> Source: source_snapshot/PROJECT_V2_IMPLEMENTATION_PLAN.md
> Bifurcated into: changes/project/migration/PROJECT_V2_IMPLEMENTATION_PLAN.md
> Module: Project > Migration
> Date: 2025-12-17 (IST)

# Project V2 Implementation Plan

**Date:** December 2025  
**Goal:** Create Project V2 system with same hierarchical structure as Quotation V2 (Panel → Feeder → BOM 1 → BOM 2 → Components)

---

## 📋 Executive Summary

**Current Structure:**
```
Project → Quotation → Panel (QuotationSale) → Feeder/BOM → Components
```

**Desired Structure (V2):**
```
Project → Panel (ProjectSale) → Feeder → BOM 1 → BOM 2 → Components
```

**Key Requirement:** Old projects remain unchanged, new projects use V2 structure.

---

## 🎯 Objectives

1. ✅ Create Project V2 interface similar to Quotation V2
2. ✅ Maintain backward compatibility with existing projects
3. ✅ Enable data migration from backup to projects
4. ✅ Reuse Quotation V2 UI/UX patterns and components
5. ✅ Support same features: Master BOM, Reuse, Pricing, etc.

---

## 🏗️ Architecture Decision: Database Schema

### Option A: Reuse Existing Tables (RECOMMENDED) ⭐
**Approach:** Add `ProjectId` to existing tables, use `QuotationId = NULL` for Project V2

**Tables to Modify:**
- `quotation_sales` → Add `ProjectId` (nullable)
- `quotation_sale_boms` → Add `ProjectId` (nullable)  
- `quotation_sale_bom_items` → Add `ProjectId` (nullable)

**Pros:**
- ✅ No new tables needed
- ✅ Reuse all existing logic
- ✅ Single codebase for both Quotation and Project
- ✅ Easier data migration
- ✅ Less code duplication

**Cons:**
- ⚠️ Table names become misleading (quotation_sales for projects)
- ⚠️ Need careful NULL handling in queries

### Option B: Create New Tables
**Approach:** Create separate tables: `project_sales`, `project_sale_boms`, `project_sale_bom_items`

**Pros:**
- ✅ Clear separation
- ✅ No confusion with naming

**Cons:**
- ❌ Code duplication (need separate controllers/views)
- ❌ More maintenance overhead
- ❌ Harder to share logic

**Recommendation:** **Option A** - Reuse existing tables with `ProjectId` column.

---

## 📊 Database Schema Changes

### Migration 1: Add ProjectId to quotation_sales
```php
Schema::table('quotation_sales', function (Blueprint $table) {
    $table->integer('ProjectId')->nullable()->after('QuotationId');
    $table->index('ProjectId');
    $table->foreign('ProjectId')->references('ProjectId')->on('projects');
});
```

### Migration 2: Add ProjectId to quotation_sale_boms
```php
Schema::table('quotation_sale_boms', function (Blueprint $table) {
    $table->integer('ProjectId')->nullable()->after('QuotationId');
    $table->index('ProjectId');
    $table->foreign('ProjectId')->references('ProjectId')->on('projects');
});
```

### Migration 3: Add ProjectId to quotation_sale_bom_items
```php
Schema::table('quotation_sale_bom_items', function (Blueprint $table) {
    $table->integer('ProjectId')->nullable()->after('QuotationId');
    $table->index('ProjectId');
    $table->foreign('ProjectId')->references('ProjectId')->on('projects');
});
```

### Migration 4: Add Version Flag to Projects
```php
Schema::table('projects', function (Blueprint $table) {
    $table->tinyInteger('IsV2')->default(0)->after('Status');
    // 0 = Old project (no direct panels), 1 = V2 project (has direct panels)
});
```

---

## 🔄 Data Migration Strategy

### Phase 1: Identify Projects to Migrate
```sql
-- List all projects that need V2 migration
SELECT ProjectId, Name, ProjectNo 
FROM projects 
WHERE IsV2 = 0 
AND ProjectId IN (SELECT DISTINCT ProjectId FROM backup_quotation_sales);
```

### Phase 2: Migrate Data from Backup
**Assumption:** Backup data exists in separate tables or files

**Migration Script Logic:**
1. For each project in backup:
   - Create ProjectSale (Panel) records with `ProjectId` set, `QuotationId = NULL`
   - Create ProjectSaleBom (Feeder/BOM) records with `ProjectId` set, `QuotationId = NULL`
   - Create ProjectSaleBomItem (Component) records with `ProjectId` set, `QuotationId = NULL`
2. Set `IsV2 = 1` for migrated projects
3. Preserve all relationships (ParentBomId, Level, etc.)

### Phase 3: Validation
- Verify all panels migrated
- Verify all feeders/BOMs linked correctly
- Verify all components present
- Check pricing data integrity

---

## 🛠️ Implementation Plan

### Phase 1: Database & Models (Week 1)

#### 1.1 Create Migrations
- [ ] Migration: Add ProjectId to quotation_sales
- [ ] Migration: Add ProjectId to quotation_sale_boms
- [ ] Migration: Add ProjectId to quotation_sale_bom_items
- [ ] Migration: Add IsV2 flag to projects
- [ ] Run migrations on development

#### 1.2 Update Models
- [ ] Update `QuotationSale` model: Add ProjectId, relationship to Project
- [ ] Update `QuotationSaleBom` model: Add ProjectId, relationship to Project
- [ ] Update `QuotationSaleBomItem` model: Add ProjectId, relationship to Project
- [ ] Update `Project` model: Add IsV2, relationships to sales/boms/items

#### 1.3 Update Scopes
- [ ] Add scope: `whereProject($projectId)` to all three models
- [ ] Add scope: `whereQuotation($quotationId)` to maintain backward compatibility
- [ ] Add scope: `v2Projects()` to Project model

---

### Phase 2: Controller & Routes (Week 1-2)

#### 2.1 Create ProjectV2Controller
**File:** `app/Http/Controllers/ProjectV2Controller.php`

**Methods (similar to QuotationV2Controller):**
- [ ] `index($projectId)` - List panels for project
- [ ] `panel($projectId, $panelId)` - Show panel details with feeders/BOMs
- [ ] `addPanel(AddPanelRequest, $projectId)` - Add new panel
- [ ] `addFeeder(AddFeederRequest, $projectId, $panelId)` - Add feeder
- [ ] `addBom(AddBomRequest, $projectId, $parentBomId)` - Add BOM 1 or BOM 2
- [ ] `addItem(AddItemRequest, $projectId, $bomId)` - Add component
- [ ] `applyMasterBom(Request)` - Apply Master BOM to feeder/BOM
- [ ] `applyProposalBom(Request)` - Copy from another project/quotation
- [ ] `applyPanelReuse(Request)` - Reuse panel from another project
- [ ] `applyFeederReuse(Request)` - Reuse feeder from another project

#### 2.2 Create Routes
**File:** `routes/web.php`

```php
// Project V2 Routes
Route::get('project/{id}/v2', [ProjectV2Controller::class, 'index'])->name('project.v2.index');
Route::get('project/{id}/panel/{panelId}', [ProjectV2Controller::class, 'panel'])->name('project.v2.panel');
Route::post('project/{id}/panel', [ProjectV2Controller::class, 'addPanel'])->name('project.v2.addPanel');
Route::post('project/{id}/panel/{panelId}/feeder', [ProjectV2Controller::class, 'addFeeder'])->name('project.v2.addFeeder');
Route::post('project/{id}/bom/{parentBomId}/bom', [ProjectV2Controller::class, 'addBom'])->name('project.v2.addBom');
Route::post('project/{id}/bom/{bomId}/item', [ProjectV2Controller::class, 'addItem'])->name('project.v2.addItem');
Route::post('project/v2/apply-master-bom', [ProjectV2Controller::class, 'applyMasterBom'])->name('project.v2.applyMasterBom');
Route::post('project/v2/apply-proposal-bom', [ProjectV2Controller::class, 'applyProposalBom'])->name('project.v2.applyProposalBom');
Route::post('reuse/project-panel/apply', [ProjectV2Controller::class, 'applyPanelReuse'])->name('reuse.project-panel.apply');
Route::post('reuse/project-feeder/apply', [ProjectV2Controller::class, 'applyFeederReuse'])->name('reuse.project-feeder.apply');
```

---

### Phase 3: Views (Week 2)

#### 3.1 Create Project V2 Views
**Location:** `resources/views/project/v2/`

- [ ] `index.blade.php` - List panels (reuse from quotation/v2/index.blade.php)
- [ ] `panel.blade.php` - Panel details (reuse from quotation/v2/panel.blade.php)
- [ ] `_feeder.blade.php` - Feeder partial (reuse from quotation/v2/_feeder.blade.php)
- [ ] `_bom.blade.php` - BOM partial (reuse from quotation/v2/_bom.blade.php)
- [ ] `_items_table.blade.php` - Items table (reuse from quotation/v2/_items_table.blade.php)
- [ ] `_reuse_filter_modal.blade.php` - Reuse modal (reuse from quotation/v2/_reuse_filter_modal.blade.php)

**Strategy:** Copy Quotation V2 views, replace:
- `$quotation` → `$project`
- `route('quotation.v2.*')` → `route('project.v2.*')`
- `QuotationId` → `ProjectId`

#### 3.2 Update Project Index Page
**File:** `resources/views/project/index.blade.php`

- [ ] Add "Open V2" button (similar to quotation index)
- [ ] Show V2 indicator badge for V2 projects
- [ ] Add link: `route('project.v2.index', $project->ProjectId)`

---

### Phase 4: Reuse Quotation V2 Logic (Week 2-3)

#### 4.1 Create Shared Service/Trait
**Option A: Create Trait**
```php
// app/Traits/HasV2Structure.php
trait HasV2Structure {
    // Shared methods for both Quotation and Project
    public function addPanel() { ... }
    public function addFeeder() { ... }
    public function addBom() { ... }
    public function addItem() { ... }
}
```

**Option B: Create Base Controller**
```php
// app/Http/Controllers/V2BaseController.php
abstract class V2BaseController extends Controller {
    // Shared methods
}
```

**Recommendation:** **Option B** - Base controller with protected methods.

#### 4.2 Update QuotationV2Controller
- [ ] Extract shared logic to base controller
- [ ] Keep quotation-specific logic in QuotationV2Controller
- [ ] Both controllers extend V2BaseController

#### 4.3 Update ProjectV2Controller
- [ ] Extend V2BaseController
- [ ] Override methods that need project-specific logic
- [ ] Reuse 90% of code from base controller

---

### Phase 5: Data Migration Script (Week 3)

#### 5.1 Create Migration Command
**File:** `app/Console/Commands/MigrateProjectData.php`

```php
php artisan project:migrate-data {--project-id=} {--backup-table=}
```

**Features:**
- Migrate single project or all projects
- Support multiple backup sources
- Validation and rollback capability
- Progress reporting

#### 5.2 Create Backup Import Script
**File:** `app/Console/Commands/ImportProjectBackup.php`

```php
php artisan project:import-backup {backup-file} {--project-id=}
```

---

### Phase 6: Testing & Validation (Week 3-4)

#### 6.1 Unit Tests
- [ ] Test ProjectV2Controller methods
- [ ] Test model relationships
- [ ] Test scopes and queries

#### 6.2 Integration Tests
- [ ] Test full workflow: Create project → Add panel → Add feeder → Add BOM → Add component
- [ ] Test Master BOM application
- [ ] Test reuse functionality
- [ ] Test data migration

#### 6.3 User Acceptance Testing
- [ ] Test with real project data
- [ ] Verify backward compatibility
- [ ] Test data migration from backup

---

## ⚠️ Challenges & Solutions

### Challenge 1: Table Naming Confusion
**Issue:** Using `quotation_sales` for projects is confusing.

**Solution:**
- Add clear comments in code
- Use aliases in queries: `quotation_sales AS project_sales`
- Document in README
- Consider renaming in future major version

### Challenge 2: Query Complexity
**Issue:** Need to handle both `QuotationId` and `ProjectId` in queries.

**Solution:**
- Use scopes: `whereProject($id)` or `whereQuotation($id)`
- Always filter by one or the other (never both)
- Add database constraints: `CHECK (QuotationId IS NOT NULL OR ProjectId IS NOT NULL)`

### Challenge 3: Data Migration Complexity
**Issue:** Backup data structure may differ, relationships need to be preserved.

**Solution:**
- Create comprehensive mapping script
- Validate relationships after migration
- Support incremental migration (migrate one project at a time)
- Create rollback mechanism

### Challenge 4: Backward Compatibility
**Issue:** Existing code expects `QuotationId` to always be set.

**Solution:**
- Update all queries to handle NULL `QuotationId`
- Use scopes consistently
- Add validation: "Either QuotationId or ProjectId must be set"
- Test all existing quotation functionality

### Challenge 5: UI Consistency
**Issue:** Need to maintain same UI/UX for both Quotation and Project V2.

**Solution:**
- Reuse Blade components
- Use shared JavaScript functions
- Create view partials that accept context (quotation vs project)
- Use route helpers to generate correct URLs

---

## 📝 Implementation Checklist

### Database
- [ ] Create migrations for ProjectId columns
- [ ] Add IsV2 flag to projects
- [ ] Add foreign key constraints
- [ ] Add indexes for performance
- [ ] Add check constraints (QuotationId OR ProjectId must be set)

### Models
- [ ] Update QuotationSale model
- [ ] Update QuotationSaleBom model
- [ ] Update QuotationSaleBomItem model
- [ ] Update Project model
- [ ] Add relationships
- [ ] Add scopes

### Controllers
- [ ] Create V2BaseController
- [ ] Create ProjectV2Controller
- [ ] Refactor QuotationV2Controller to use base
- [ ] Add validation
- [ ] Add error handling

### Routes
- [ ] Add Project V2 routes
- [ ] Update route names
- [ ] Add middleware

### Views
- [ ] Create project/v2 directory
- [ ] Copy and adapt Quotation V2 views
- [ ] Update route helpers
- [ ] Update variable names
- [ ] Add V2 indicator in project index

### JavaScript
- [ ] Update AJAX URLs for project context
- [ ] Reuse existing functions
- [ ] Add project-specific handlers if needed

### Data Migration
- [ ] Create migration command
- [ ] Create backup import script
- [ ] Test migration on sample data
- [ ] Document migration process

### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] User acceptance testing
- [ ] Performance testing

### Documentation
- [ ] Update API documentation
- [ ] Create user guide
- [ ] Document migration process
- [ ] Update README

---

## 🚀 Rollout Strategy

### Phase 1: Development (Weeks 1-2)
- Implement database changes
- Create controllers and routes
- Create views

### Phase 2: Testing (Week 3)
- Internal testing
- Fix bugs
- Performance optimization

### Phase 3: Migration (Week 4)
- Migrate test projects
- Validate data
- User training

### Phase 4: Production (Week 5)
- Deploy to production
- Migrate production projects
- Monitor and support

---

## 📊 Estimated Effort

| Phase | Tasks | Estimated Hours |
|-------|-------|----------------|
| Database & Models | 15 tasks | 20 hours |
| Controllers & Routes | 10 tasks | 16 hours |
| Views | 8 tasks | 12 hours |
| Shared Logic | 5 tasks | 8 hours |
| Data Migration | 4 tasks | 12 hours |
| Testing | 8 tasks | 16 hours |
| Documentation | 4 tasks | 8 hours |
| **Total** | **54 tasks** | **92 hours (~2.5 weeks)** |

---

## ✅ Success Criteria

1. ✅ New projects can use V2 structure
2. ✅ Old projects remain unchanged
3. ✅ Data migration successful from backup
4. ✅ UI/UX matches Quotation V2
5. ✅ All features work (Master BOM, Reuse, Pricing)
6. ✅ Performance acceptable
7. ✅ No breaking changes to existing functionality

---

## 🔄 Next Steps

1. **Review this plan** with team
2. **Approve database schema** changes
3. **Identify backup data source** and structure
4. **Create development branch** for Project V2
5. **Start with Phase 1** (Database & Models)

---

## 📞 Questions to Resolve

1. **Backup Data Format:** What format is the backup data in? (SQL dump, CSV, separate tables?)
2. **Migration Scope:** Migrate all projects or selected ones?
3. **Timeline:** What's the target completion date?
4. **Testing:** Who will perform UAT?
5. **Rollback Plan:** What if migration fails?

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Status:** Draft - Pending Approval


