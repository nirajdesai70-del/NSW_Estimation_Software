#!/bin/bash

# Script to add RAG telemetry environment variables to .env

cd /Users/nirajdesai/Projects/NSW_Estimation_Software

echo "Adding RAG telemetry configuration to .env..."

# Add telemetry config to .env
echo "" >> .env
echo "# RAG Telemetry Configuration" >> .env
echo "RAG_TELEMETRY_ENABLED=true" >> .env
echo "RAG_TELEMETRY_LOG_CHANNEL=rag_telemetry" >> .env

# Verify it was added
echo ""
echo "✅ Verifying .env update:"
tail -5 .env

# Clear config cache
echo ""
echo "✅ Clearing config cache..."
cd source_snapshot && php artisan config:clear

echo ""
echo "✅ Step 1 complete! Telemetry logging is now enabled."

