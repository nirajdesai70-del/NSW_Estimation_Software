#!/bin/bash

# NSW Backend Server Startup Script
# Ensures server starts on port 8003 as per PORT_POLICY.md

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "NSW Backend Server Startup"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: python -m venv venv"
    echo "   Then: source venv/bin/activate"
    echo "   Then: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn not found in virtual environment!"
    echo "   Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists (warn but don't fail)
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   The server may fail to start if DATABASE_URL and SECRET_KEY are not set"
    echo "   You can set them as environment variables or create a .env file"
    echo ""
fi

# Check if port 8003 is already in use
if lsof -Pi :8003 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Warning: Port 8003 is already in use!"
    echo "   Attempting to start anyway (may fail)..."
    echo ""
fi

# Set port explicitly via environment variable
export NSW_BACKEND_PORT=8003

echo "🚀 Starting FastAPI server on port 8003..."
echo "   API: http://localhost:8003"
echo "   Health: http://localhost:8003/health"
echo "   Docs: http://localhost:8003/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003

