#!/bin/bash

# Start All Services with RAG
# This script starts the RAG query service and handles orphan containers

set -e  # Exit on error

# Get the project root directory (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Set Docker context if needed (uncomment if you use a specific context)
# docker context use mac-desktop

echo "Starting RAG services with orphan container cleanup..."

# Start RAG Query service with --remove-orphans flag to clean up orphan containers
docker compose -f docker-compose.rag.yml --profile rag up -d --remove-orphans

echo "RAG services started successfully!"
echo ""
echo "Services running:"
docker compose -f docker-compose.rag.yml --profile rag ps

echo ""
echo "RAG Query service should be available at: http://localhost:8011"
echo "Health check: curl http://localhost:8011/health"
