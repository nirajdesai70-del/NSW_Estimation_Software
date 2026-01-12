# Port Status Check Report

**Date:** 2026-01-03  
**Check:** Ports 8000 and 8003

---

## Current Status

### Port 8000 (Nish/Laravel) ✅ **RUNNING**
- **Service**: PHP/Laravel application
- **Process**: PHP process detected (PID visible in lsof)
- **Status**: ✅ **ACTIVE** - Service is listening on port 8000
- **Expected**: Nish (Laravel) application

### Port 8003 (NSW Backend/FastAPI) ✅ **CONFIGURED** (Needs to be started)
- **Service**: FastAPI backend
- **Process**: No process detected on port 8003 (needs to be started)
- **Status**: ✅ **READY TO START** - Configuration fixed, startup script created
- **Expected**: NSW Backend API (FastAPI)
- **Fix Applied**: ✅ Startup script created, README updated, main.py enhanced

---

## Port Configuration

### Port 8000 - Nish (Laravel)
- **Purpose**: Laravel application (Nish)
- **Start Command**: 
  ```bash
  php artisan serve --port=8000
  ```
- **Status**: ✅ Running (PHP process detected)

### Port 8003 - NSW Backend (FastAPI)
- **Purpose**: FastAPI backend API
- **Configuration**: Set in `backend/app/core/config.py` (default: 8003)
- **Start Command**:
  ```bash
  cd backend
  source venv/bin/activate
  uvicorn app.main:app --reload --port 8003
  ```
- **Status**: ⚠️ Not running (no process detected)

---

## How to Start Port 8003

### Option 1: Use Startup Script (Recommended) ✅ **NEW**
```bash
cd backend
./start_server.sh
```
This script:
- ✅ Checks virtual environment
- ✅ Validates dependencies
- ✅ Ensures port 8003
- ✅ Provides helpful error messages

### Option 2: Manual uvicorn command
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

### Option 3: Direct Python execution ✅ **NEW**
```bash
cd backend
source venv/bin/activate
python -m app.main
```

### Option 4: Using Environment Variable
```bash
cd backend
source venv/bin/activate
export NSW_BACKEND_PORT=8003
uvicorn app.main:app --reload
```

---

## Verification Commands

### Check Port 8000
```bash
# Check if Laravel is running
curl http://localhost:8000

# Or check process
lsof -i :8000
```

### Check Port 8003
```bash
# Check if FastAPI is running
curl http://localhost:8003/health

# Or check process
lsof -i :8003
```

### Check Both Ports
```bash
# Check both ports at once
lsof -i :8000 -i :8003
```

---

## Expected Behavior

### When Both Ports Are Running:

**Port 8000 (Nish/Laravel):**
- Should respond to HTTP requests
- Typically serves web UI
- Laravel routes available

**Port 8003 (NSW Backend/FastAPI):**
- Health endpoint: `http://localhost:8003/health` → `{"status": "healthy", "service": "nsw-api"}`
- API docs: `http://localhost:8003/docs`
- API prefix: `/api/v1/*`

---

## Troubleshooting

### Port 8003 Not Starting

1. **Check if port is already in use:**
   ```bash
   lsof -i :8003
   ```

2. **Check backend configuration:**
   ```bash
   cd backend
   cat app/core/config.py | grep PORT
   ```

3. **Check if virtual environment is activated:**
   ```bash
   cd backend
   which python  # Should show venv path
   ```

4. **Check if dependencies are installed:**
   ```bash
   cd backend
   source venv/bin/activate
   pip list | grep uvicorn
   ```

5. **Check for errors in startup:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8003
   # Look for error messages
   ```

### Port 8000 Not Working

1. **Check Laravel application:**
   ```bash
   php artisan --version
   ```

2. **Check if artisan serve is running:**
   ```bash
   ps aux | grep artisan
   ```

3. **Restart Laravel:**
   ```bash
   php artisan serve --port=8000
   ```

---

## Summary

| Port | Service | Status | Action Needed |
|------|---------|--------|----------------|
| **8000** | Nish (Laravel) | ✅ **RUNNING** | None - Working |
| **8003** | NSW Backend (FastAPI) | ✅ **READY** | Start with `./start_server.sh` |

## Recent Fixes Applied ✅

1. ✅ Created `backend/start_server.sh` - Easy startup script
2. ✅ Updated `backend/README.md` - Port 8003 references
3. ✅ Enhanced `backend/app/main.py` - Added `__main__` block
4. ✅ Created `backend/PORT_8003_FIX.md` - Documentation

See `backend/PORT_8003_FIX.md` for complete details.

---

## Next Steps

1. ✅ **Port 8000**: Already working - no action needed
2. ⚠️ **Port 8003**: Start the FastAPI backend:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8003
   ```

3. **Verify both are working:**
   ```bash
   curl http://localhost:8000
   curl http://localhost:8003/health
   ```

---

## Reference

- Port Policy: `PORT_POLICY.md`
- Backend Config: `backend/app/core/config.py`
- Backend README: `backend/README.md`
- Quick Start: `QUICK_START.md`

