# NSW Estimation Software - New Build Architecture

**Version:** 1.0  
**Date:** 2025-12-26  
**Status:** CANONICAL  
**Owner:** Phase 5 Implementation Team

## Purpose

This document defines the technical architecture for the new build of NSW Estimation Software, following a side-by-side approach with the legacy Laravel application.

---

## Target Architecture (Side-by-Side, Dev-Only)

### Legacy (Unchanged)
- **Location:** `/nish` (Laravel UI/API → MySQL via XAMPP)
- **Purpose:** Reference, old workflows, comparisons
- **Status:** Read-only reference, no modifications

### New Build (Canonical Going Forward)
- **Frontend:** React UI (port 3000)
- **Backend:** FastAPI (port 8001)
- **Database:** PostgreSQL 14+ (port 5432)
- **Status:** This becomes the future production path when ready

---

## Stepwise Implementation Plan

### 1. Dev Environment (Repeatable)

**Docker Compose** for Postgres + Redis (optional), run FastAPI locally:
- Postgres: `5432`
- FastAPI: `8001`
- React: `3000`

**Environment Files:**
- `backend/.env` - FastAPI configuration (Postgres DSN)
- `frontend/.env` - React configuration (API base URL)

**Key Rule:** Keep `.env` files separate to avoid cross-connection mistakes.

### 2. Backend Stack (Recommended Baseline)

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** + **Alembic** - ORM and migrations
- **Pydantic v2** - Data validation and schemas
- **Auth:** JWT (access + refresh) + RBAC
- **Background Jobs (later):** Redis + RQ/Celery (only if needed)

### 3. API Boundaries (Keep it Modular)

Modules aligned to domain:
- `auth/` - Login, roles, permissions
- `catalog/` - Items, attributes, SKU mapping
- `bom/` - L1 → L2 explosion, multi-SKU to multi-line-items
- `pricing/` - Catalog price import, price rules
- `quotation/` - Quotation header, line items, revisions
- `audit/` - Events + change log

### 4. React UI Integration (Clean Contract)

- Use **OpenAPI** from FastAPI as the single contract
- Generate typed client (optional) or use thin API wrapper
- UI pages map to API resources (no DB knowledge in UI)

### 5. Legacy Reference Strategy (No Live Coupling)

When you need to "check old logic":
- Run Laravel + MySQL separately
- Compare outputs manually (or via exported CSV)
- Implement new logic in FastAPI/Postgres

If you need sample data in Postgres:
- Do one-way import MySQL → Postgres into a `seed_legacy_snapshot` schema/table set (dev-only)

---

## Auth & Security (Simple and Scalable)

- **JWT access token** (short TTL) + **refresh token**
- **Roles** for workflow (can mirror 3-layer login structure later)
- **Strict CORS** allowlist for React dev/prod domains

---

## Implementation Roadmap

### Phase 1: Foundation ✅
1. ✅ Create FastAPI skeleton with health route + OpenAPI
2. ✅ Bring up Postgres 14+ dev
3. ✅ Create React UI skeleton
4. ✅ Set up Docker Compose

### Phase 2: Core Features (Next)
1. ⏳ Implement Catalog + SKU import (foundational, multi-SKU pitfalls identified)
2. ⏳ Implement BOM explosion logic (L1→L2, multi-SKU → multi-line-items)
3. ⏳ Implement quotation flow + pricing pack

### Phase 3: Advanced Features
1. ⏳ Authentication & RBAC
2. ⏳ Audit logging
3. ⏳ Background jobs (if needed)

### Phase 4: Production Readiness
1. ⏳ Testing suite
2. ⏳ Performance optimization
3. ⏳ Deployment configuration
4. ⏳ Cutover planning

---

## 5R Summary

**Results:** React + FastAPI + Postgres dev-only becomes the new canonical build, legacy Laravel/MySQL stays intact.

**Risks:** 
- Accidental cross-wiring envs
- Attempting live sync between MySQL and Postgres too early

**Rules:** 
- Separate repos or clearly separated envs
- One-way import only
- OpenAPI is the contract
- Legacy system is read-only reference

**Roadmap:** 
Skeleton → Catalog/SKU import → BOM explode → Quotation → Dashboards → cutover planning

**References:** 
- Phase-5 exploration approach
- Deterministic engine principle
- NSW Fundamentals alignment

---

## Directory Structure

```
NSW_Estimation_Software/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   └── api/v1/endpoints/
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # React frontend
│   ├── src/
│   ├── package.json
│   └── .env.example
├── docker-compose.yml      # Postgres + Redis
└── NEW_BUILD_ARCHITECTURE.md
```

---

## Quick Start

### 1. Start Database
```bash
docker-compose up -d postgres
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

### 3. Setup Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 4. Access
- API: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Frontend: http://localhost:3000

---

## Environment Variables Reference

### Backend (.env)
```env
DATABASE_URL=postgresql://nsw_user:nsw_dev_password@localhost:5432/nsw_estimation
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8001/api/v1
```

---

## Important Notes

1. **No Live Coupling:** The legacy Laravel/MySQL system is completely separate. Do not attempt to sync data between systems in production.

2. **OpenAPI Contract:** The FastAPI backend automatically generates OpenAPI documentation. Use this as the single source of truth for API contracts.

3. **Modular Design:** Each domain (auth, catalog, bom, etc.) is a separate module with clear boundaries.

4. **Reference Only:** When you need to check old logic, run the legacy system separately and compare outputs manually.

---

## Change Log

- **v1.0 (2025-12-26):** Initial architecture document created with FastAPI + React + PostgreSQL setup

---

**END OF ARCHITECTURE DOCUMENT**

