#!/bin/bash

# NSW Estimation Software - New Build Setup Script
# This script helps set up the new FastAPI + React + PostgreSQL stack

set -e

echo "🚀 Setting up NSW Estimation Software - New Build"
echo "=================================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start PostgreSQL
echo "📦 Starting PostgreSQL container..."
docker-compose up -d postgres
echo "✅ PostgreSQL started on port 5432"
echo ""

# Setup Backend
echo "🐍 Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your settings"
else
    echo "✅ .env file already exists"
fi

echo "Running database migrations..."
alembic upgrade head || echo "⚠️  No migrations to run yet (this is normal for first setup)"

cd ..
echo "✅ Backend setup complete"
echo ""

# Setup Frontend
echo "⚛️  Setting up React frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "✅ Node modules already installed"
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

cd ..
echo "✅ Frontend setup complete"
echo ""

echo "=================================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your database credentials"
echo "2. Start the backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8001"
echo "3. Start the frontend: cd frontend && npm run dev"
echo ""
echo "Access points:"
echo "- API: http://localhost:8001"
echo "- API Docs: http://localhost:8001/docs"
echo "- Frontend: http://localhost:3000"
echo ""

