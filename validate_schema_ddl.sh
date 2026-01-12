#!/bin/bash
# Schema DDL Validation Script
# Validates schema.sql against PostgreSQL in Docker
# 
# Usage:
#   ./validate_schema_ddl.sh              # Run validation and cleanup
#   ./validate_schema_ddl.sh --keep       # Keep container for inspection
#   ./validate_schema_ddl.sh --inspect    # Same as --keep
#   ./validate_schema_ddl.sh --context desktop-linux  # Use specific Docker context
#
# Based on one-liner pattern:
#   unset DOCKER_HOST; docker rm -f nswpg >/dev/null 2>&1 || true; docker run -d --name nswpg ...
#
# Schema file: docs/PHASE_5/04_SCHEMA_CANON/DDL/schema.sql

set -euo pipefail

# Auto-detect repo root via git (works from any directory)
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SCHEMA_DDL="${REPO_ROOT}/docs/PHASE_5/04_SCHEMA_CANON/DDL/schema.sql"
CONTAINER_NAME="nswpg"
DB_NAME="nsw_schema_tmp"
DB_USER="postgres"
DB_PASSWORD="postgres"
POSTGRES_IMAGE="postgres:16-alpine"

# Parse arguments
KEEP_CONTAINER=false
DOCKER_CONTEXT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep|--inspect)
            KEEP_CONTAINER=true
            shift
            ;;
        --context)
            DOCKER_CONTEXT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--keep|--inspect] [--context CONTEXT]"
            exit 1
            ;;
    esac
done

# Setup Docker command
# Explicitly unset DOCKER_HOST to avoid conflicts (use default socket or context)
unset DOCKER_HOST
DOCKER_CMD="docker"
if [ -n "$DOCKER_CONTEXT" ]; then
    DOCKER_CMD="docker --context $DOCKER_CONTEXT"
fi

echo "=========================================="
echo "NSW Schema DDL Validation"
echo "=========================================="
echo ""
echo "Schema file: $SCHEMA_DDL"
echo "Container: $CONTAINER_NAME"
echo "Database: $DB_NAME"
echo "Keep container: $KEEP_CONTAINER"
echo ""

# Validate schema file exists
if [ ! -f "$SCHEMA_DDL" ]; then
    echo "❌ ERROR: Schema DDL file not found: $SCHEMA_DDL"
    exit 1
fi

# Step 1: Clean up any existing container
echo "Step 1: Cleaning up any existing container..."
$DOCKER_CMD rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
echo "✅ Cleanup complete"
echo ""

# Step 2: Start PostgreSQL container
echo "Step 2: Starting PostgreSQL container..."
$DOCKER_CMD run -d \
    --name "$CONTAINER_NAME" \
    -e POSTGRES_PASSWORD="$DB_PASSWORD" \
    "$POSTGRES_IMAGE" >/dev/null
echo "✅ Container started"
echo ""

# Step 3: Wait for PostgreSQL to be ready
echo "Step 3: Waiting for PostgreSQL to be ready..."
MAX_WAIT=30
WAIT_COUNT=0
while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    if $DOCKER_CMD exec "$CONTAINER_NAME" pg_isready -U "$DB_USER" >/dev/null 2>&1; then
        echo "✅ PostgreSQL is ready"
        break
    fi
    echo "   Waiting... ($WAIT_COUNT/$MAX_WAIT seconds)"
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
done

if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
    echo "❌ ERROR: PostgreSQL did not become ready within $MAX_WAIT seconds"
    echo "   Check container logs: $DOCKER_CMD logs $CONTAINER_NAME"
    $DOCKER_CMD rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    exit 1
fi
echo ""

# Step 4: Create test database
echo "Step 4: Creating test database..."
$DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS $DB_NAME;" >/dev/null 2>&1 || true
if ! $DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE $DB_NAME;" >/dev/null 2>&1; then
    echo "❌ ERROR: Failed to create database"
    exit 1
fi

# Verify database was created (wait a moment for commit)
sleep 1
DB_CHECK=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -tA -c "SELECT COUNT(*) FROM pg_database WHERE datname='$DB_NAME';" 2>/dev/null | tr -d ' ')
if [ "$DB_CHECK" != "1" ]; then
    echo "❌ ERROR: Database creation verification failed (found: $DB_CHECK)"
    exit 1
fi
echo "✅ Database created: $DB_NAME"
echo ""

# Step 5: Copy schema.sql into container
echo "Step 5: Copying schema.sql into container..."
$DOCKER_CMD cp "$SCHEMA_DDL" "$CONTAINER_NAME:/schema.sql"
echo "✅ Schema file copied"
echo ""

# Step 6: Execute schema.sql DDL
echo "Step 6: Executing schema.sql DDL..."
LOG_FILE="/tmp/schema_validation_${DB_NAME}_$(date +%Y%m%d_%H%M%S).log"
if $DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 -f /schema.sql > "$LOG_FILE" 2>&1; then
    echo "✅ Schema DDL executed successfully!"
    echo ""
    
    # Step 7: Validate tables were created
    echo "Step 7: Validating table creation..."
    TABLE_COUNT=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';" | tr -d ' ')
    echo "   Tables created: $TABLE_COUNT"
    
    if [ "$TABLE_COUNT" -ge 30 ]; then
        echo "✅ Expected ~34 tables, found $TABLE_COUNT (acceptable)"
    else
        echo "⚠️  WARNING: Expected ~34 tables, but found only $TABLE_COUNT"
    fi
    echo ""
    
    # Step 8: Validate CHECK constraints (critical spot checks)
    echo "Step 8: Validating CHECK constraints..."
    echo ""
    echo "All CHECK constraints:"
    $DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT conrelid::regclass AS table_name, conname AS constraint_name FROM pg_constraint WHERE contype='c' AND conname LIKE 'ck_%' ORDER BY 1, 2;"
    echo ""
    
    CK_COUNT=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM pg_constraint WHERE contype='c' AND conname LIKE 'ck_%';" | tr -d ' ')
    echo "   Total CHECK constraints: $CK_COUNT"
    
    # Critical spot checks
    echo ""
    echo "Critical spot checks:"
    
    # G-01 on master_bom_items
    G01=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -tA -c \
"SELECT COUNT(*) FROM pg_constraint WHERE contype='c' AND conrelid='master_bom_items'::regclass AND conname LIKE 'ck_master_bom_items%g01%';")
    if [ "$G01" -ge 1 ]; then
        echo "   ✅ master_bom_items: G-01 present"
    else
        echo "   ❌ master_bom_items: G-01 MISSING"
    fi
    
    # quote_bom_items should have at least these 3 guardrails
    G02=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -tA -c \
"SELECT COUNT(*) FROM pg_constraint WHERE contype='c' AND conrelid='quote_bom_items'::regclass AND conname LIKE 'ck_quote_bom_items%g02%';")
    G06=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -tA -c \
"SELECT COUNT(*) FROM pg_constraint WHERE contype='c' AND conrelid='quote_bom_items'::regclass AND conname LIKE 'ck_quote_bom_items%g06%';")
    G07=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -tA -c \
"SELECT COUNT(*) FROM pg_constraint WHERE contype='c' AND conrelid='quote_bom_items'::regclass AND conname LIKE 'ck_quote_bom_items%g07%';")
    
    if [ "$G02" -ge 1 ] && [ "$G06" -ge 1 ] && [ "$G07" -ge 1 ]; then
        echo "   ✅ quote_bom_items: G-02/G-06/G-07 present"
    else
        echo "   ❌ quote_bom_items: Missing guardrails: G02=$G02 G06=$G06 G07=$G07"
    fi
    
    echo ""
    
    # Step 9: Validate primary keys and foreign keys
    echo "Step 9: Validating constraints..."
    PK_COUNT=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.table_constraints WHERE constraint_type='PRIMARY KEY' AND table_schema='public';" | tr -d ' ')
    FK_COUNT=$($DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.table_constraints WHERE constraint_type='FOREIGN KEY' AND table_schema='public';" | tr -d ' ')
    
    echo "   Primary Keys: $PK_COUNT"
    echo "   Foreign Keys: $FK_COUNT"
    echo ""
    
    echo "=========================================="
    echo "✅ VALIDATION SUCCESSFUL"
    echo "=========================================="
    echo ""
    echo "Test database: $DB_NAME"
    echo "Container: $CONTAINER_NAME"
    echo "Log file: $LOG_FILE"
    echo ""
    
    if [ "$KEEP_CONTAINER" = true ]; then
        echo "Container kept for inspection."
        echo ""
        echo "To inspect the database:"
        echo "  $DOCKER_CMD exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME"
        echo ""
        echo "To clean up:"
        echo "  $DOCKER_CMD rm -f $CONTAINER_NAME"
    else
        echo "Cleaning up container..."
        $DOCKER_CMD rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
        echo "✅ Container removed"
    fi
    echo ""
    
else
    echo "❌ ERROR: Schema DDL execution failed"
    echo ""
    echo "Error log:"
    cat "$LOG_FILE"
    echo ""
    
    if [ "$KEEP_CONTAINER" = true ]; then
        echo "Container kept for inspection."
        echo "To inspect the database state:"
        echo "  $DOCKER_CMD exec -it $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME"
        echo ""
        echo "To clean up:"
        echo "  $DOCKER_CMD rm -f $CONTAINER_NAME"
    else
        echo "Cleaning up container..."
        $DOCKER_CMD rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
    exit 1
fi
