# Port Registry (Human Authority)

**Machine authority:** `ops/ports.env`  
**Rule:** Do not hardcode ports in new docs/scripts. Prefer reading from `ops/ports.env` (or run compose with `--env-file ops/ports.env`).

---

## Canonical ports

| Variable | Default | Service | Container port | Exposure | Source |
| --- | ---: | --- | ---: | --- | --- |
| `POSTGRES_HOST_PORT` | 5433 | `postgres` | 5432 | Host → container | `docker-compose.yml` |
| `REDIS_HOST_PORT` | 6380 | `redis` | 6379 | Host → container | `docker-compose.yml` |
| `KB_QUERY_HOST_PORT` | 8011 | `kb_query` | 8099 | Host → container | `docker-compose.rag.yml` |
| `DECISION_RAG_HOST_PORT` | 8021 | `decisions_query` | 8099 | Host → container | `docker-compose.rag.decisions.yml` |

---

## Usage

- **Docker Compose** (recommended):

```bash
docker compose --env-file ops/ports.env -f docker-compose.yml up -d
docker compose --env-file ops/ports.env -f docker-compose.rag.yml up -d
docker compose --env-file ops/ports.env -f docker-compose.rag.decisions.yml up -d
```
