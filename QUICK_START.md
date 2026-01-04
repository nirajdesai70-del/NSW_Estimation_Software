# Quick Start Guide - NSW Estimation Software New Build

This guide will help you get the new FastAPI + React + PostgreSQL stack running quickly.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ installed
- Node.js 18+ and npm installed

## Quick Setup (Automated)

Run the setup script:

```bash
./setup_new_build.sh
```

This will:
1. Start PostgreSQL in Docker
2. Set up Python virtual environment
3. Install backend dependencies
4. Install frontend dependencies
5. Create `.env` files from examples

## Manual Setup

### 1. Start PostgreSQL

```bash
docker-compose up -d postgres
```

Verify it's running:
```bash
docker ps
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings (especially DATABASE_URL and SECRET_KEY)

# Run migrations (when you have models)
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8001
```

Backend will be available at:
- API: http://localhost:8001
- Docs: http://localhost:8001/docs
- Health: http://localhost:8001/health

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env if needed (VITE_API_BASE_URL)

# Start dev server
npm run dev
```

Frontend will be available at: http://localhost:3000

## Verify Everything Works

1. Check PostgreSQL:
   ```bash
   docker ps | grep postgres
   ```

2. Check Backend:
   ```bash
   curl http://localhost:8001/health
   ```
   Should return: `{"status":"healthy","service":"nsw-api"}`

3. Check Frontend:
   Open http://localhost:3000 in your browser

## Project Structure

```
NSW_Estimation_Software/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/            # Source code
│   └── package.json
├── docker-compose.yml   # Postgres + Redis
└── NEW_BUILD_ARCHITECTURE.md  # Full architecture docs
```

## Environment Variables

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

## Common Issues

### PostgreSQL Connection Error
- Make sure Docker is running: `docker ps`
- Check if container is up: `docker-compose ps`
- Verify port 5432 is not in use

### Backend Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend API Connection Error
- Check `VITE_API_BASE_URL` in `frontend/.env`
- Make sure backend is running on port 8001
- Check CORS settings in `backend/app/core/config.py`

## Next Steps

1. ✅ FastAPI skeleton with health route + OpenAPI
2. ✅ Postgres 14+ dev setup
3. ⏳ Implement Catalog + SKU import
4. ⏳ Implement BOM explosion logic
5. ⏳ Implement quotation flow + pricing pack

## Documentation

- Full architecture: `NEW_BUILD_ARCHITECTURE.md`
- Backend README: `backend/README.md`
- Frontend README: `frontend/README.md`

