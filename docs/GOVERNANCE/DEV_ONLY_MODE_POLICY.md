# Dev-Only Mode Policy

**Version:** 1.0  
**Date:** 2025-12-26  
**Status:** CANONICAL — MANDATORY  
**Owner:** Phase 5 Implementation Team

---

## Purpose

This policy prevents accidental coupling, schema drift, and production risks during the new build development phase. It establishes clear boundaries between the legacy system and the new build.

---

## Core Rules (Non-Negotiable)

### 1. PostgreSQL is Dev-Only

**Rule:** PostgreSQL database is **development-only**. It is NOT production-ready and must NOT be used for production data.

**Implications:**
- All data in Postgres is considered temporary/experimental
- No production data should be stored in Postgres during development
- Database can be reset/dropped without data loss concerns
- Migrations are experimental and can be rewritten

**Enforcement:**
- Environment variables clearly mark `ENVIRONMENT=development`
- Database connection strings use dev credentials only
- No production database URLs in codebase

---

### 2. Legacy MySQL is Reference-Only

**Rule:** The legacy Laravel/MySQL system (`/nish`) is **read-only reference**. It is used ONLY for:
- Understanding existing logic
- Comparing outputs
- Manual verification
- One-way data import (seed snapshots only)

**Implications:**
- **NO live sync** between MySQL and Postgres
- **NO bidirectional data flow**
- **NO runtime queries** to MySQL from FastAPI
- Legacy system runs separately, independently

**Enforcement:**
- Legacy MySQL connection settings are marked as `LEGACY_*` in config
- No active database connections to MySQL from FastAPI code
- All legacy references are documented as "reference only"

---

### 3. No Live Sync

**Rule:** There is **NO live synchronization** between legacy MySQL and new Postgres databases.

**Implications:**
- Changes in MySQL do NOT automatically appear in Postgres
- Changes in Postgres do NOT affect MySQL
- Systems operate completely independently
- Manual comparison via exported CSV/JSON is acceptable

**Enforcement:**
- No background jobs syncing data
- No triggers or replication
- No shared connection pools
- Clear separation in code and documentation

---

### 4. Imports are One-Way Seed Snapshots Only

**Rule:** Data imports from MySQL to Postgres are **one-way, manual, seed snapshots** for development purposes only.

**Implications:**
- Imports are **not automatic**
- Imports are **not continuous**
- Imports create **snapshot data** in a separate schema/table set (e.g., `seed_legacy_snapshot`)
- Imports are **dev-only** and can be discarded
- Imported data is **not production data**

**Enforcement:**
- Import scripts are clearly marked as "one-way seed"
- Imported data goes into `seed_legacy_snapshot` schema or clearly marked tables
- No production import paths
- Import scripts require explicit manual execution

---

### 5. No AI/NL→SQL in Runtime Paths

**Rule:** **No AI/Natural Language to SQL conversion** in any runtime code paths.

**Implications:**
- No LLM-generated SQL queries in production code
- No dynamic SQL generation from natural language
- All SQL must be explicit, reviewed, and tested
- Database queries use ORM (SQLAlchemy) or explicit SQL strings

**Enforcement:**
- Code reviews check for AI-generated SQL
- All database queries are statically analyzable
- No runtime SQL generation from user input without validation

---

## Architecture Boundaries

### Clear Separation

```
┌─────────────────────────────────────┐
│  Legacy System (Reference Only)     │
│  /nish (Laravel + XAMPP/MySQL)      │
│  - Read-only reference              │
│  - Manual comparison only           │
│  - One-way import source            │
└─────────────────────────────────────┘
              │
              │ (one-way import only)
              ▼
┌─────────────────────────────────────┐
│  New Build (Canonical)              │
│  FastAPI + React + PostgreSQL        │
│  - Dev-only Postgres                │
│  - Independent operation             │
│  - Future production path            │
└─────────────────────────────────────┘
```

### Data Flow Rules

**Allowed:**
- ✅ Manual CSV/JSON export from MySQL → import to Postgres (dev seed)
- ✅ Manual comparison of outputs
- ✅ Reading legacy code for reference
- ✅ One-way snapshot imports to `seed_legacy_snapshot` schema

**Forbidden:**
- ❌ Live sync between MySQL and Postgres
- ❌ Bidirectional data flow
- ❌ Runtime queries to MySQL from FastAPI
- ❌ Automatic data replication
- ❌ Production data in Postgres during dev phase

---

## Environment Configuration

### Backend (.env)

```env
# New Build Database (Dev-Only)
DATABASE_URL=postgresql+psycopg://nsw_user:nsw_dev_password@localhost:5432/nsw_estimation
ENVIRONMENT=development

# Legacy Reference (Read-Only, Not Connected)
LEGACY_MYSQL_HOST=localhost
LEGACY_MYSQL_PORT=3306
LEGACY_MYSQL_DB=nish
LEGACY_MYSQL_USER=root
LEGACY_MYSQL_PASSWORD=
# NOTE: These are for reference/documentation only, NOT for live connections
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8001/api/v1
VITE_ENVIRONMENT=development
```

---

## Violation Consequences

**If any rule is violated:**
1. Immediate code review required
2. Violation must be documented
3. Corrective action must be taken
4. Policy must be re-read by team

**Common Violations to Watch For:**
- Adding MySQL connection code to FastAPI
- Creating sync jobs between systems
- Using Postgres for production data
- AI-generated SQL in runtime paths
- Bidirectional data imports

---

## Policy Review

This policy must be reviewed:
- Before any database integration work
- Before any import script creation
- When adding new team members
- When production deployment is planned

---

## Change Log

- **v1.0 (2025-12-26):** Initial policy created to prevent accidental coupling and schema drift

---

**END OF DEV-ONLY MODE POLICY**

