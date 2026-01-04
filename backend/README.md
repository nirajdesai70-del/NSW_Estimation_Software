# NSW Estimation Software - FastAPI Backend

**New build (canonical going forward)**

This is the FastAPI backend for NSW Estimation Software, designed to work alongside the legacy Laravel application (`/nish`) without interfering with it.

## Architecture

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - ORM with Alembic for migrations
- **PostgreSQL 14+** - Primary database (dev-only)
- **Pydantic v2** - Data validation and schemas
- **JWT** - Authentication (access + refresh tokens)
- **Redis** (optional) - For background jobs if needed

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py           # Settings and configuration
│   │   └── database.py         # Database setup
│   └── api/
│       └── v1/
│           ├── router.py       # Main API router
│           └── endpoints/
│               ├── auth.py     # Authentication
│               ├── catalog.py  # Catalog items, SKU mapping
│               ├── bom.py      # BOM explosion logic
│               ├── pricing.py  # Price import, price rules
│               ├── quotation.py # Quotation management
│               └── audit.py    # Events and change log
├── alembic/                    # Database migrations
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Key settings:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Change this in production
- `CORS_ORIGINS` - React frontend URL

### 3. Start PostgreSQL

Using Docker Compose (from project root):

```bash
docker-compose up -d postgres
```

Or use your own PostgreSQL instance.

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

Or use the startup script:
```bash
./start_server.sh
```

The API will be available at:
- API: http://localhost:8003
- Health: http://localhost:8003/health
- Docs: http://localhost:8003/docs
- ReDoc: http://localhost:8003/redoc

## API Endpoints

All endpoints are prefixed with `/api/v1`:

- `GET /health` - Health check
- `GET /` - Root endpoint
- `/api/v1/auth/*` - Authentication
- `/api/v1/catalog/*` - Catalog management
- `/api/v1/bom/*` - BOM operations
- `/api/v1/pricing/*` - Pricing
- `/api/v1/quotation/*` - Quotations
- `/api/v1/audit/*` - Audit logs

## Development Guidelines

1. **Keep it modular** - Each domain (auth, catalog, bom, etc.) is a separate module
2. **Use OpenAPI** - All endpoints are automatically documented
3. **No legacy coupling** - Do not connect to Laravel/MySQL for live data
4. **Reference only** - Legacy system is for reference/comparison only

## Legacy Reference

The legacy Laravel application (`/nish`) remains untouched. When you need to check old logic:
- Run Laravel + MySQL separately
- Compare outputs manually or via exported CSV
- Implement new logic in FastAPI/Postgres

## Next Steps

1. ✅ FastAPI skeleton with health route + OpenAPI
2. ✅ Postgres 14+ dev setup
3. ⏳ Implement Catalog + SKU import
4. ⏳ Implement BOM explosion logic (L1→L2, multi-SKU → multi-line-items)
5. ⏳ Implement quotation flow + pricing pack

