# Port Policy Implementation - Complete ✅

**Date**: 2025-01-XX  
**Status**: ✅ **IMPLEMENTATION COMPLETE**

---

## Summary

All critical port policy changes have been successfully implemented. The system now follows a standardized, conflict-free port assignment policy with environment variable support for flexibility.

---

## Changes Implemented

### ✅ 1. Canonical PORT_POLICY.md Created
**Location**: `/PORT_POLICY.md`

- Complete port map documentation
- Docker Compose profile usage guide
- Host vs Docker networking rules
- Environment variable reference
- Acceptance test commands
- Troubleshooting guide

**Status**: ✅ Complete and ready for team reference

---

### ✅ 2. Backend Configuration Updated
**File**: `backend/app/core/config.py`

**Changes**:
- Added `import os` for environment variable support
- Changed `PORT: int = 8001` → `PORT: int = int(os.getenv("NSW_BACKEND_PORT", "8003"))`
- Changed `REDIS_URL: str = "redis://localhost:6379/0"` → `REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")`

**Impact**: 
- Backend now defaults to port 8003 (can be overridden via `NSW_BACKEND_PORT` env var)
- Redis defaults to port 6380 (can be overridden via `REDIS_URL` env var)

---

### ✅ 3. Docker Compose (Main) Updated
**File**: `docker-compose.yml`

**Changes**:
- Postgres port: `"5434:5432"` → `"${POSTGRES_HOST_PORT:-5433}:5432"`
- Redis port: `"6379:6379"` → `"${REDIS_HOST_PORT:-6380}:6379"`
- Added `profiles: ["db"]` to postgres service
- Changed redis profile from `with-redis` to `cache`

**Impact**:
- Docker Postgres now uses port 5433 (default, overridable)
- Docker Redis now uses port 6380 (default, overridable)
- Services won't auto-start (require explicit profile activation)

---

### ✅ 4. Docker Compose (RAG) Updated
**File**: `docker-compose.rag.yml`

**Changes**:
- kb_query port: `"8099:8099"` → `"${KB_QUERY_HOST_PORT:-8011}:8099"`
- Added `profiles: ["rag"]` to kb_query service
- Removed `restart: unless-stopped` (manual control)

**Impact**:
- RAG Query now uses port 8011 on host (default, overridable)
- Service won't auto-start (requires `--profile rag`)
- No automatic restart (manual control)

---

### ✅ 5. Frontend API Client Updated
**File**: `frontend/src/services/api.ts`

**Changes**:
- API base URL default: `'http://localhost:8001/api/v1'` → `'http://localhost:8003/api/v1'`

**Impact**: Frontend will connect to backend on port 8003 by default

---

### ✅ 6. Frontend Vite Config Updated
**File**: `frontend/vite.config.ts`

**Changes**:
- Proxy target: `'http://localhost:8001'` → `'http://localhost:8003'`

**Impact**: Vite dev server will proxy API requests to port 8003

---

### ✅ 7. Critical Documentation Updated
**Files**: 
- `backend/RUN_TESTS.md`
- `backend/TEST_CATALOG_IMPORT.md`

**Changes**:
- All port references updated: `8001` → `8003`
- Postgres port references: `5434` → `5433`
- All curl examples updated to use new ports

**Impact**: Documentation now matches actual port assignments

---

## Final Port Map (Canonical)

| Service | Host Port | Container Port | Notes |
|---------|-----------|----------------|-------|
| Nish (Laravel) | 8000 | N/A | Host-native |
| NSW Backend | 8003 | N/A | Host-native, env: `NSW_BACKEND_PORT` |
| RAG Query | 8011 | 8099 | Docker, env: `KB_QUERY_HOST_PORT` |
| KB Indexer | N/A | N/A | Batch job, no port |
| Host Postgres | 5432 | N/A | Local service |
| Docker Postgres | 5433 | 5432 | Optional, env: `POSTGRES_HOST_PORT` |
| Docker Redis | 6380 | 6379 | Optional, env: `REDIS_HOST_PORT` |

---

## Environment Variables

All ports can be overridden via environment variables:

```bash
# Override backend port
export NSW_BACKEND_PORT=8003

# Override RAG Query port
export KB_QUERY_HOST_PORT=8011

# Override Docker Postgres port
export POSTGRES_HOST_PORT=5433

# Override Docker Redis port
export REDIS_HOST_PORT=6380

# Override Redis URL (full URL)
export REDIS_URL=redis://localhost:6380/0
```

---

## Docker Compose Profiles

Services now use profiles to prevent auto-start:

```bash
# Start RAG Query only
docker compose -f docker-compose.rag.yml --profile rag up -d

# Run KB Indexer (batch)
docker compose -f docker-compose.rag.yml --profile index run --rm kb_indexer

# Start Docker Postgres (optional)
docker compose --profile db up -d

# Start Docker Redis (optional)
docker compose --profile cache up -d
```

---

## Acceptance Tests

Run these commands to verify implementation:

```bash
# Check NSW Backend is listening on 8003
lsof -iTCP:8003 -sTCP:LISTEN

# Check RAG Query is listening on 8011 (if started)
lsof -iTCP:8011 -sTCP:LISTEN
curl http://localhost:8011/health

# Check Docker Postgres on 5433 (if started)
lsof -iTCP:5433 -sTCP:LISTEN

# Check Docker Redis on 6380 (if started)
lsof -iTCP:6380 -sTCP:LISTEN
```

---

## Next Steps

1. **Update `.env` files** (if they exist):
   - `backend/.env`: Add `PORT=8003` (optional, defaults work)
   - `frontend/.env`: Update `VITE_API_BASE_URL=http://localhost:8003/api/v1`

2. **Test the changes**:
   - Start backend: Should run on port 8003
   - Start frontend: Should connect to backend on 8003
   - Start RAG Query: Should run on port 8011

3. **Update menu-bar scripts** (if needed):
   - Ensure "Start Apps + RAG" uses correct ports
   - Verify "Stop All" stops Docker containers

4. **Team communication**:
   - Share `PORT_POLICY.md` with team
   - Update any CI/CD configurations
   - Document any custom port overrides

---

## Rollback Plan

If issues arise, you can quickly rollback:

1. **Quick fix**: Set environment variables to old ports
2. **Code rollback**: `git checkout HEAD -- backend/app/core/config.py`
3. **Docker rollback**: `git checkout HEAD -- docker-compose*.yml`

---

## Files Modified

1. ✅ `PORT_POLICY.md` (created)
2. ✅ `backend/app/core/config.py`
3. ✅ `docker-compose.yml`
4. ✅ `docker-compose.rag.yml`
5. ✅ `frontend/src/services/api.ts`
6. ✅ `frontend/vite.config.ts`
7. ✅ `backend/RUN_TESTS.md`
8. ✅ `backend/TEST_CATALOG_IMPORT.md`

---

## Verification Checklist

- [x] PORT_POLICY.md created and complete
- [x] Backend config defaults to port 8003
- [x] Backend config defaults to Redis 6380
- [x] Docker Compose files use environment variables
- [x] Docker Compose files have profiles
- [x] Frontend API client uses port 8003
- [x] Frontend Vite proxy uses port 8003
- [x] Critical documentation updated
- [ ] Acceptance tests run successfully (pending manual verification)
- [ ] Team notified of changes (pending)

---

**Implementation Status**: ✅ **COMPLETE**  
**Ready for**: Testing and team rollout

---

**Note**: This implementation follows the canonical port policy and is ready for SSD migration. All ports are standardized and conflict-free.

