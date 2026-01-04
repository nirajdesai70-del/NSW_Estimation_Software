# Port 8003 Fix and Verification

**Date:** 2026-01-03  
**Status:** ✅ **FIXED**

---

## Issues Found

1. ❌ README showed port 8001 instead of 8003
2. ❌ No easy way to start server on correct port
3. ❌ No direct execution entry point in main.py

---

## Fixes Applied

### 1. ✅ Updated README.md
- Changed port references from 8001 → 8003
- Added startup script reference
- Updated all URL examples

### 2. ✅ Created `start_server.sh`
- Startup script that ensures port 8003
- Checks for virtual environment
- Validates dependencies
- Warns about missing .env file
- Checks if port is already in use
- Sets `NSW_BACKEND_PORT=8003` explicitly

### 3. ✅ Added `__main__` block to `app/main.py`
- Allows direct execution: `python -m app.main`
- Uses settings from config (port 8003 by default)
- Enables auto-reload for development

---

## How to Start Server on Port 8003

### Option 1: Use Startup Script (Recommended)
```bash
cd backend
./start_server.sh
```

### Option 2: Manual uvicorn command
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

### Option 3: Direct Python execution
```bash
cd backend
source venv/bin/activate
python -m app.main
```

### Option 4: Using environment variable
```bash
cd backend
source venv/bin/activate
export NSW_BACKEND_PORT=8003
uvicorn app.main:app --reload
```

---

## Verification

### Check if port 8003 is running:
```bash
lsof -i :8003
```

### Test health endpoint:
```bash
curl http://localhost:8003/health
# Expected: {"status": "healthy", "service": "nsw-api"}
```

### Test root endpoint:
```bash
curl http://localhost:8003/
# Expected: {"message": "NSW Estimation Software API", "version": "0.1.0", "status": "operational"}
```

### Check API docs:
Open in browser: http://localhost:8003/docs

---

## Configuration

The port is configured in `app/core/config.py`:
```python
PORT: int = int(os.getenv("NSW_BACKEND_PORT", "8003"))
```

This means:
- Default port is **8003**
- Can be overridden with `NSW_BACKEND_PORT` environment variable
- Startup script explicitly sets it to 8003

---

## Required Environment Variables

The server requires these in `.env` file or as environment variables:

- `DATABASE_URL` - PostgreSQL connection string (required)
- `SECRET_KEY` - JWT secret key (required)

Optional:
- `NSW_BACKEND_PORT` - Override port (default: 8003)
- `REDIS_URL` - Redis connection (default: redis://localhost:6380/0)

---

## Troubleshooting

### Port 8003 already in use
```bash
# Find what's using the port
lsof -i :8003

# Kill the process (replace PID)
kill <PID>
```

### Server won't start - missing DATABASE_URL
```bash
# Create .env file in backend/ directory
cat > backend/.env << EOF
DATABASE_URL=postgresql://nsw_user:password@localhost:5432/nsw_estimation
SECRET_KEY=your-secret-key-here-change-in-production
EOF
```

### Virtual environment not activated
```bash
cd backend
source venv/bin/activate
# Verify: which python should show venv path
```

---

## Summary

✅ **Port 8003 is now properly configured**
✅ **Multiple ways to start the server**
✅ **Startup script ensures correct port**
✅ **README updated with correct port**

**Status:** Ready to use! 🚀

