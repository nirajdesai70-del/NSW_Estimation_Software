# PORT_POLICY.md (CANONICAL)

**Purpose**: Prevent port conflicts and enforce a single, deterministic local dev standard across:
- Nish (Laravel)
- NSW Estimation Backend (FastAPI)
- Docker tooling (RAG/Catalog)
- Optional Docker DB/cache

**Status**: ✅ **LOCKED** - This is the single source of truth for port assignments.

---

## Canonical Port Map (LOCKED)

### Host-native Apps
- **Nish (Laravel)**: `8000`
- **NSW Backend API (FastAPI)**: `8003`
- **Host Postgres**: `5432` (local service, not Docker)

### Docker Tooling Reserved Block (8010–8020)
- **RAG Query API (Docker)**: `8011` → container `8099`
- **Catalog API (Docker, optional)**: `8013` → container `8013`
- **KB Indexer (Docker)**: **no port** (batch job only)

### Optional Docker Infrastructure
- **Docker Postgres (optional)**: `5433` → container `5432`
- **Docker Redis (optional)**: `6380` → container `6379`

---

## Key Rules

1. **Port 8003 is reserved for NSW Backend only. Docker must never bind 8003.**
2. **Port 8000 is reserved for Nish (Laravel) only.**
3. **Port 5432 on host is reserved for local Postgres. Docker Postgres uses 5433.**
4. **Docker tooling uses reserved block 8010-8020 to avoid conflicts.**

---

## Docker Compose Profiles (LOCKED)

Profiles prevent auto-start and allow selective service management:

- `rag` → kb_query (RAG Query API)
- `index` → kb_indexer (batch job, no port)
- `db` → postgres (optional Docker Postgres)
- `cache` → redis (optional Docker Redis)
- `catalog` → catalog_api (optional, if/when added)

**Usage:**
```bash
# Start RAG Query only
docker compose -f docker-compose.rag.yml --profile rag up -d

# Run KB Indexer (batch job)
docker compose -f docker-compose.rag.yml --profile index run --rm kb_indexer

# Start Docker Postgres (optional)
docker compose --profile db up -d

# Start Docker Redis (optional)
docker compose --profile cache up -d
```

---

## Host vs Docker Networking (RULE)

### When Nish/NSW run on host (current mode)
Services running on host connect to Docker services via `localhost`:

- `RAG_QUERY_SERVICE_URL=http://localhost:8011`
- `DATABASE_URL=postgresql://nsw_user:password@localhost:5432/nsw_estimation` (host Postgres)
- `REDIS_URL=redis://localhost:6380/0` (if using Docker Redis)

### If NSW backend ever runs inside Docker network
Services running inside Docker connect via service names:

- `RAG_QUERY_SERVICE_URL=http://kb_query:8099`
- `DATABASE_URL=postgresql://nsw_user:password@postgres:5432/nsw_estimation`
- `REDIS_URL=redis://redis:6379/0`

**Current setup**: Host-native mode (Nish + NSW on host, tooling in Docker)

---

## Environment Variables

For flexibility and per-machine customization, ports can be overridden via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `NSW_BACKEND_PORT` | `8003` | NSW Backend API port |
| `KB_QUERY_HOST_PORT` | `8011` | RAG Query host port |
| `POSTGRES_HOST_PORT` | `5433` | Docker Postgres host port |
| `REDIS_HOST_PORT` | `6380` | Docker Redis host port |

**Note**: Container internal ports (8099, 5432, 6379) are fixed and should not be changed.

---

## Startup Commands

### Apps Only (Nish + NSW)
Use menu-bar **Start Apps** button (clean start, no tooling).

This starts:
- Nish on `8000`
- NSW Backend on `8003`

### Apps + RAG
Use menu-bar **Start Apps + RAG** button.

This starts:
- Nish on `8000`
- NSW Backend on `8003`
- RAG Query on `8011` (Docker)

Optional: "Rebuild KB now?" prompt for indexer.

### Run KB Index Rebuild (Batch Job)
```bash
docker context use mac-desktop
docker compose -f docker-compose.rag.yml --profile index run --rm kb_indexer
```

### Start RAG Query Only
```bash
docker context use mac-desktop
docker compose -f docker-compose.rag.yml --profile rag up -d
```

### Stop RAG Tooling Only
```bash
docker compose -f docker-compose.rag.yml down
```

### Stop All (Apps + Tooling)
Use menu-bar **Stop All** button (stops Nish, NSW, and all Docker containers).

---

## Acceptance Tests (Post-Change Validation)

After implementing port changes, verify with these commands:

```bash
# NSW Backend listening
lsof -iTCP:8003 -sTCP:LISTEN

# RAG Query listening (if started)
lsof -iTCP:8011 -sTCP:LISTEN
curl http://localhost:8011/health

# Optional: Docker Postgres (if profile started)
lsof -iTCP:5433 -sTCP:LISTEN

# Optional: Docker Redis (if profile started)
lsof -iTCP:6380 -sTCP:LISTEN
```

**Expected Results:**
- NSW Backend: `uvicorn` process on port 8003
- RAG Query: `docker` process on port 8011
- Health check: `{"status":"healthy"}` or similar

---

## Migration Checklist

When setting up on a new machine or after port policy changes:

- [ ] Update `backend/.env` with `PORT=8003` (or rely on default)
- [ ] Update `backend/.env` with `REDIS_URL=redis://localhost:6380/0` (if using Redis)
- [ ] Update `frontend/.env` with `VITE_API_BASE_URL=http://localhost:8003/api/v1`
- [ ] Verify no services are running on ports 8003, 8011, 5433, 6380
- [ ] Start services using menu-bar buttons or compose commands
- [ ] Run acceptance tests above
- [ ] Verify frontend connects to backend on 8003

---

## Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -iTCP:8003 -sTCP:LISTEN

# Kill the process (replace PID)
kill <PID>
```

### Services Not Starting
1. Check Docker is running: `docker ps`
2. Check profiles are specified: `docker compose --profile rag up -d`
3. Check logs: `docker compose logs kb_query`

### Frontend Can't Connect to Backend
1. Verify backend is running: `curl http://localhost:8003/health`
2. Check `VITE_API_BASE_URL` in `frontend/.env`
3. Check Vite proxy config in `frontend/vite.config.ts`

---

## Change History

- **2025-01-XX**: Initial port policy established
  - NSW Backend: 8001 → 8003
  - RAG Query: 8099 → 8011
  - Docker Postgres: 5434 → 5433
  - Docker Redis: 6379 → 6380
  - Added Docker Compose profiles

---

**Last Updated**: 2025-01-XX  
**Maintained By**: NSW Estimation Software Team  
**Status**: ✅ Active and Enforced

