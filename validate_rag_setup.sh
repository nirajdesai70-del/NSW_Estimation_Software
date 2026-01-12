#!/bin/bash

# RAG UI Validation Script
# Run this from your project root directory

set -e

echo "=========================================="
echo "RAG UI Validation Setup"
echo "=========================================="
echo ""

# Step 1: Enable Feature Flags
echo "Step 1: Enabling RAG feature flags..."
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Please create it first."
    exit 1
fi

# Check if flags already exist
if grep -q "RAG_UI_ENABLED" .env; then
    echo "  → RAG_UI_ENABLED already exists in .env"
    # Update it to true
    sed -i '' 's/^RAG_UI_ENABLED=.*/RAG_UI_ENABLED=true/' .env 2>/dev/null || \
    sed -i 's/^RAG_UI_ENABLED=.*/RAG_UI_ENABLED=true/' .env
else
    echo "  → Adding RAG_UI_ENABLED=true to .env"
    echo "RAG_UI_ENABLED=true" >> .env
fi

if grep -q "RAG_EXPLAIN_WHY_ENABLED" .env; then
    echo "  → RAG_EXPLAIN_WHY_ENABLED already exists in .env"
    # Update it to true
    sed -i '' 's/^RAG_EXPLAIN_WHY_ENABLED=.*/RAG_EXPLAIN_WHY_ENABLED=true/' .env 2>/dev/null || \
    sed -i 's/^RAG_EXPLAIN_WHY_ENABLED=.*/RAG_EXPLAIN_WHY_ENABLED=true/' .env
else
    echo "  → Adding RAG_EXPLAIN_WHY_ENABLED=true to .env"
    echo "RAG_EXPLAIN_WHY_ENABLED=true" >> .env
fi

echo "  ✅ Feature flags configured"
echo ""

# Step 2: Clear Config Cache
echo "Step 2: Clearing Laravel config cache..."
if [ -f artisan ]; then
    php artisan config:clear
    echo "  ✅ Config cache cleared"
else
    echo "  ⚠️  artisan file not found. Are you in the Laravel root directory?"
    echo "  → Please run manually: php artisan config:clear"
fi
echo ""

# Step 3: Check kb_query Service
echo "Step 3: Checking kb_query service health..."
echo "  → Trying localhost:8099..."
if curl -s -f http://localhost:8099/health > /dev/null 2>&1; then
    echo "  ✅ kb_query is reachable on localhost:8099"
    curl -s http://localhost:8099/health | jq . 2>/dev/null || curl -s http://localhost:8099/health
elif curl -s -f http://kb_query:8099/health > /dev/null 2>&1; then
    echo "  ✅ kb_query is reachable on kb_query:8099"
    curl -s http://kb_query:8099/health | jq . 2>/dev/null || curl -s http://kb_query:8099/health
else
    echo "  ⚠️  kb_query service not reachable"
    echo "     Try: docker-compose ps (if using docker)"
    echo "     Or: curl http://localhost:8099/health"
fi
echo ""

# Step 4: Verify Route
echo "Step 4: Route information..."
echo "  → Test harness route: /examples/rag-catalog"
echo "  → API endpoint: POST /ui/rag/query"
echo "  → Make sure your Laravel app is running"
echo ""

# Step 5: Summary
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Make sure your Laravel app is running"
echo "  2. Navigate to: http://your-app-url/examples/rag-catalog"
echo "  3. Follow the UX checklist in RAG_KB/CATALOG_INTEGRATION_TEST.md"
echo ""
echo "Current .env settings:"
grep -E "RAG_UI_ENABLED|RAG_EXPLAIN_WHY_ENABLED" .env 2>/dev/null || echo "  (Could not read .env)"
echo ""

