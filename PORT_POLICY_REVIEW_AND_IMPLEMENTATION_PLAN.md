# Port Policy Review & Implementation Plan

## Executive Summary

**Status**: ✅ **Policy is sound and recommended for adoption**

The proposed port policy standardizes port assignments, prevents conflicts, and creates clear separation between native apps and Docker tooling. This document reviews the policy, identifies all issues, provides solutions, and outlines a safe migration path.

---

## 1. Policy Review

### 1.1 What's Good ✅

1. **Clear Separation**: Native apps (8000, 8003) vs Docker tooling (8010-8020 block)
2. **No Port Conflicts**: Each service has a dedicated, non-overlapping port
3. **Profile-Based Control**: Docker Compose profiles prevent accidental starts
4. **Batch Job Pattern**: KB Indexer correctly designed as batch-only (no port)
5. **Environment Variable Support**: Allows per-machine customization
6. **Future-Proof**: Reserved block (8010-8020) for future tooling

### 1.2 What Needs Attention ⚠️

1. **Migration Impact**: Many hardcoded references to old ports (8001, 5434, 6379, 8099)
2. **Frontend Configuration**: Vite proxy and API client need updates
3. **Documentation**: 15+ files reference old ports
4. **Test Scripts**: Automated tests reference old ports
5. **Backward Compatibility**: Need strategy for existing `.env` files

---

## 2. Current State Analysis

### 2.1 Port Mappings (Current vs Proposed)

| Service | Current | Proposed | Status |
|---------|---------|----------|--------|
| Nish (Laravel) | 8000 | 8000 | ✅ No change |
| NSW Backend | 8001 | 8003 | ⚠️ **Needs update** |
| RAG Query | 8099 | 8011 | ⚠️ **Needs update** |
| KB Indexer | N/A | N/A | ✅ Already correct |
| Host Postgres | 5432 | 5432 | ✅ No change |
| Docker Postgres | 5434 | 5433 | ⚠️ **Needs update** |
| Docker Redis | 6379 | 6380 | ⚠️ **Needs update** |

### 2.2 Files Requiring Updates

#### Critical (Runtime Impact)
- `backend/app/core/config.py` - PORT default (8001→8003), REDIS_URL (6379→6380)
- `docker-compose.yml` - Postgres (5434→5433), Redis (6379→6380), add profiles
- `docker-compose.rag.yml` - kb_query port (8099→8011), add profiles, remove restart
- `frontend/src/services/api.ts` - API base URL default (8001→8003)
- `frontend/vite.config.ts` - Proxy target (8001→8003)

#### Important (Documentation/Testing)
- `backend/RUN_TESTS.md` - psql port (5434→5433), uvicorn port (8001→8003)
- `backend/TEST_CATALOG_IMPORT.md` - Multiple port references
- `backend/test_catalog_import.sh` - curl URLs (8001→8003)
- `backend/test_catalog_import.py` - Port references
- `setup_new_build.sh` - Port references in output
- `QUICK_START.md` - Port references
- `NEW_BUILD_ARCHITECTURE.md` - Port references
- `NEW_BUILD_SETUP_COMPLETE.md` - Port references
- `backend/README.md` - Port references

#### Low Priority (Can update gradually)
- Other documentation files with port references

---

## 3. Issues & Challenges

### 3.1 Issue: Breaking Changes

**Problem**: Changing defaults will break existing setups if `.env` files aren't updated.

**Impact**: 
- Backend won't start on expected port
- Frontend won't connect to backend
- Tests will fail
- Docker containers won't be accessible on expected ports

**Solution**: 
1. Use environment variables with new defaults
2. Document migration steps clearly
3. Provide `.env.example` updates
4. Add validation/warnings in startup scripts

### 3.2 Issue: Frontend Proxy Configuration

**Problem**: Vite dev server proxy is hardcoded to `localhost:8001`.

**Impact**: Frontend won't proxy API requests correctly during development.

**Solution**: Update `vite.config.ts` proxy target to `8003`.

### 3.3 Issue: Docker Compose Profiles Missing

**Problem**: Current `docker-compose.yml` has no profiles, so services start automatically.

**Impact**: 
- Port conflicts if services already running
- Can't selectively start services
- Violates "no auto-start" principle

**Solution**: Add profiles to all services in both compose files.

### 3.4 Issue: Redis Default Mismatch

**Problem**: `config.py` defaults to `6379` but Docker Redis will be on `6380`.

**Impact**: If Redis is used, connection will fail unless explicitly configured.

**Solution**: Update default to `6380` or make it environment-driven.

### 3.5 Issue: Documentation Inconsistency

**Problem**: Many docs reference old ports, creating confusion.

**Impact**: Developers follow wrong instructions, waste time debugging.

**Solution**: Update critical docs first, others gradually.

---

## 4. Solutions & Adoption Strategy

### 4.1 Recommended Approach: Phased Migration

**Phase 1: Core Configuration (Critical)**
- Update `config.py` defaults
- Update `docker-compose.yml` with profiles and new ports
- Update `docker-compose.rag.yml` with correct port and profiles
- Update frontend API configuration

**Phase 2: Documentation (Important)**
- Update quick start guides
- Update test documentation
- Update architecture docs

**Phase 3: Scripts & Automation (Nice to have)**
- Update test scripts
- Update setup scripts
- Add port validation

### 4.2 Backward Compatibility Strategy

**Option A: Environment Variable Override (Recommended)**
```python
# config.py
PORT: int = int(os.getenv("PORT", "8003"))
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")
```

**Option B: Migration Script**
Create a script that:
1. Checks current `.env` files
2. Warns about port changes
3. Offers to update automatically

**Recommendation**: Use Option A (env vars) - simpler, more flexible.

### 4.3 Docker Compose Profile Strategy

**Profiles to Add:**

```yaml
# docker-compose.yml
postgres:
  profiles: ["db"]
redis:
  profiles: ["cache"]

# docker-compose.rag.yml  
kb_query:
  profiles: ["rag"]
kb_indexer:
  profiles: ["index"]
```

**Usage:**
```bash
# Start only DB
docker compose --profile db up -d

# Start RAG tooling
docker compose -f docker-compose.rag.yml --profile rag up -d

# Run indexer
docker compose -f docker-compose.rag.yml --profile index run --rm kb_indexer
```

---

## 5. Implementation Plan

### 5.1 Step-by-Step Execution

#### Step 1: Update Core Configuration Files
1. ✅ Update `backend/app/core/config.py`
   - Change `PORT: int = 8001` → `PORT: int = 8003`
   - Change `REDIS_URL: str = "redis://localhost:6379/0"` → `REDIS_URL: str = "redis://localhost:6380/0"`

2. ✅ Update `docker-compose.yml`
   - Change postgres port: `"5434:5432"` → `"${POSTGRES_HOST_PORT:-5433}:5432"`
   - Change redis port: `"6379:6379"` → `"${REDIS_HOST_PORT:-6380}:6379"`
   - Add `profiles: ["db"]` to postgres
   - Change redis profile from `with-redis` to `cache`

3. ✅ Update `docker-compose.rag.yml`
   - Change kb_query port: `"8099:8099"` → `"${KB_QUERY_HOST_PORT:-8011}:8099"`
   - Add `profiles: ["rag"]` to kb_query
   - Remove `restart: unless-stopped` (manual control)
   - Ensure kb_indexer has `profiles: ["index"]`

4. ✅ Update `frontend/src/services/api.ts`
   - Change default: `'http://localhost:8001/api/v1'` → `'http://localhost:8003/api/v1'`

5. ✅ Update `frontend/vite.config.ts`
   - Change proxy target: `'http://localhost:8001'` → `'http://localhost:8003'`

#### Step 2: Update Critical Documentation
1. ✅ Update `backend/RUN_TESTS.md`
   - Change psql port: `-p 5434` → `-p 5433`
   - Change uvicorn port: `--port 8001` → `--port 8003`
   - Update curl URLs: `8001` → `8003`

2. ✅ Update `backend/TEST_CATALOG_IMPORT.md`
   - Update all port references

3. ✅ Update `QUICK_START.md`
   - Update port references

#### Step 3: Create Port Policy Documentation
1. ✅ Create `PORT_POLICY.md` in project root
   - Document all port assignments
   - Document profile usage
   - Document migration notes

#### Step 4: Update Environment Examples
1. ✅ Update `.env.example` files (if they exist)
   - Update DATABASE_URL if it references port
   - Add PORT=8003
   - Add REDIS_URL=redis://localhost:6380/0

---

## 6. Risk Assessment

### 6.1 Low Risk ✅
- Updating docker-compose files (no running services affected until restart)
- Adding profiles (backward compatible)
- Updating documentation

### 6.2 Medium Risk ⚠️
- Changing config.py defaults (requires .env update or restart)
- Updating frontend config (requires rebuild)

### 6.3 Mitigation Strategies
1. **Test in isolation first**: Update one service at a time
2. **Keep old ports temporarily**: Use env vars to allow rollback
3. **Clear migration guide**: Document what needs updating
4. **Validation**: Add startup checks for port conflicts

---

## 7. Testing Checklist

After implementation, verify:

- [ ] Backend starts on port 8003
- [ ] Frontend connects to backend on 8003
- [ ] RAG Query starts on port 8011
- [ ] Docker Postgres accessible on 5433 (if profile started)
- [ ] Docker Redis accessible on 6380 (if profile started)
- [ ] KB Indexer runs without port (batch job)
- [ ] Profiles work correctly (services don't auto-start)
- [ ] Existing `.env` files still work (with overrides)
- [ ] Documentation matches actual ports

---

## 8. Rollback Plan

If issues arise:

1. **Quick Rollback**: Set environment variables to old ports
   ```bash
   PORT=8001 docker compose ...
   ```

2. **Code Rollback**: Revert config.py changes
   ```bash
   git checkout HEAD -- backend/app/core/config.py
   ```

3. **Docker Rollback**: Revert compose files
   ```bash
   git checkout HEAD -- docker-compose*.yml
   ```

---

## 9. Post-Implementation

### 9.1 Communication
- Update team documentation
- Announce port changes
- Update any CI/CD configurations

### 9.2 Monitoring
- Watch for port conflict errors
- Monitor startup logs
- Check for connection failures

### 9.3 Future Improvements
- Add port validation script
- Add health check endpoints
- Consider port conflict detection

---

## 10. Final Recommendation

**✅ PROCEED WITH IMPLEMENTATION**

The policy is well-designed and addresses real port conflict issues. The migration is manageable with the phased approach outlined above.

**Priority Order:**
1. **Critical**: Core config files (config.py, compose files, frontend)
2. **Important**: Test documentation and quick start guides
3. **Nice to have**: Other documentation updates

**Timeline Estimate:**
- Phase 1 (Critical): 30 minutes
- Phase 2 (Important): 30 minutes
- Phase 3 (Nice to have): 1 hour (can be done gradually)

**Total**: ~2 hours for complete migration, or 1 hour for critical updates only.

---

## Appendix: File Change Summary

### Files to Modify (Critical)
1. `backend/app/core/config.py`
2. `docker-compose.yml`
3. `docker-compose.rag.yml`
4. `frontend/src/services/api.ts`
5. `frontend/vite.config.ts`

### Files to Modify (Important)
6. `backend/RUN_TESTS.md`
7. `backend/TEST_CATALOG_IMPORT.md`
8. `backend/test_catalog_import.sh`
9. `QUICK_START.md`

### Files to Create
10. `PORT_POLICY.md` (new documentation)

---

**Ready for execution?** Review this plan and confirm if you want to proceed with the implementation.

