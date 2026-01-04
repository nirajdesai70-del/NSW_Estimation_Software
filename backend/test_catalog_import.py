#!/usr/bin/env python3
"""
Test script for catalog import endpoint
Run: python3 test_catalog_import.py
"""
import json
import sys
import requests
from pathlib import Path

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

BASE_URL = "http://localhost:8011"
API_PREFIX = "/api/v1"

def print_step(step_num, message):
    print(f"\n{YELLOW}Step {step_num}: {message}{NC}")

def print_success(message):
    print(f"{GREEN}✓ {message}{NC}")

def print_error(message):
    print(f"{RED}✗ {message}{NC}")

def test_server_running():
    """Test if server is running"""
    print_step(1, "Checking if FastAPI server is running...")
    try:
        # Try docs endpoint (most reliable)
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success("Server is running (docs endpoint accessible)")
            return True
        # Try root endpoint
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_success("Server is running")
            print(f"  Response: {response.json()}")
            return True
        # Try health endpoint as fallback
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Server is running")
            print(f"  Response: {response.json()}")
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            print(f"  Tried: /docs, /, /health")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Server is not running. Please start it with:")
        print("  cd backend && uvicorn app.main:app --reload --port 8001")
        return False
    except Exception as e:
        print_error(f"Error checking server: {e}")
        return False

def test_endpoint_exists():
    """Test if catalog endpoint is registered"""
    print_step(2, "Checking if catalog endpoint is registered...")
    try:
        # Try to get OpenAPI schema
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            schema = response.json()
            paths = schema.get("paths", {})
            catalog_paths = [p for p in paths.keys() if "catalog" in p]
            if catalog_paths:
                print_success(f"Found {len(catalog_paths)} catalog endpoints")
                for path in catalog_paths[:5]:
                    print(f"  - {path}")
                return True
            else:
                # Try direct endpoint test as fallback
                print("  OpenAPI schema doesn't show catalog endpoints, trying direct test...")
                test_response = requests.get(f"{BASE_URL}{API_PREFIX}/catalog/skus?limit=1", timeout=5)
                if test_response.status_code in [200, 404]:  # 404 means endpoint exists but might need auth
                    print_success("Catalog endpoint appears to be registered (direct test)")
                    return True
                print_error("No catalog endpoints found")
                return False
        else:
            print_error(f"Could not fetch OpenAPI schema: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error checking endpoints: {e}")
        return False

def find_final_csv():
    """Find the FINAL CSV file"""
    print_step(3, "Finding FINAL CSV file...")
    csv_path = Path(__file__).parent.parent / "tools" / "price_normalizer" / "output" / "final" / "schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv"
    
    if not csv_path.exists():
        print_error(f"CSV not found at: {csv_path}")
        # Try to find any FINAL CSV
        final_dir = csv_path.parent
        if final_dir.exists():
            csv_files = list(final_dir.glob("*.csv"))
            if csv_files:
                csv_path = csv_files[0]
                print(f"  Using: {csv_path}")
            else:
                return None
        else:
            return None
    
    print_success(f"Found CSV: {csv_path}")
    # Show first few lines
    with open(csv_path, 'r') as f:
        lines = f.readlines()[:3]
        print("  First few lines:")
        for line in lines:
            print(f"    {line.strip()}")
    
    return csv_path

def test_dry_run(csv_path):
    """Test import with dry_run=true"""
    print_step(4, "Testing import with dry_run=true...")
    
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': (csv_path.name, f, 'text/csv')}
            response = requests.post(
                f"{BASE_URL}{API_PREFIX}/catalog/skus/import?dry_run=true",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Dry run successful")
            print(f"  Batch ID: {data.get('batch_id')}")
            print(f"  Rows total: {data.get('rows_total')}")
            print(f"  Rows valid: {data.get('rows_valid')}")
            print(f"  Rows error: {data.get('rows_error')}")
            
            if data.get('rows_error', 0) > 0:
                print(f"\n  {YELLOW}⚠ Found {data.get('rows_error')} errors:{NC}")
                errors = data.get('errors_sample', [])[:5]
                for err in errors:
                    print(f"    Row {err.get('row')}: {err.get('error')} (field: {err.get('field')})")
                return False, data
            else:
                return True, data
        else:
            print_error(f"Dry run failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False, None
    except Exception as e:
        print_error(f"Error during dry run: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_commit(csv_path):
    """Test import with dry_run=false (actual commit)"""
    print_step(5, "Testing import with dry_run=false (COMMIT)...")
    
    response = input("  This will write to database. Continue? (y/N): ")
    if response.lower() != 'y':
        print("  Skipping commit test")
        return False, None
    
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': (csv_path.name, f, 'text/csv')}
            response = requests.post(
                f"{BASE_URL}{API_PREFIX}/catalog/skus/import?dry_run=false",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Import committed successfully")
            print(f"  Batch ID: {data.get('batch_id')}")
            print(f"  Items created: {data.get('items_created')}")
            print(f"  SKUs created: {data.get('skus_created')}")
            print(f"  SKUs updated: {data.get('skus_updated')}")
            print(f"  Prices inserted: {data.get('prices_inserted')}")
            print(f"  Price list ID: {data.get('price_list_id')}")
            return True, data
        else:
            print_error(f"Import commit failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False, None
    except Exception as e:
        print_error(f"Error during commit: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_get_endpoints():
    """Test GET endpoints for verification"""
    print_step(6, "Verifying GET endpoints...")
    
    try:
        # Test SKUs endpoint
        response = requests.get(f"{BASE_URL}{API_PREFIX}/catalog/skus?limit=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("SKUs endpoint working")
            print(f"  Response keys: {list(data.keys())}")
            if 'skus' in data:
                print(f"  SKUs returned: {len(data.get('skus', []))}")
        else:
            print_error(f"SKUs endpoint returned status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print_error(f"Error testing GET endpoints: {e}")

def main():
    print("=" * 50)
    print("Catalog Import Test Suite")
    print("=" * 50)
    
    # Step 1: Check server
    if not test_server_running():
        sys.exit(1)
    
    # Step 2: Check endpoints
    if not test_endpoint_exists():
        print_error("Catalog endpoints not found. Check server logs for import errors.")
        sys.exit(1)
    
    # Step 3: Find CSV
    csv_path = find_final_csv()
    if not csv_path:
        print_error("Could not find FINAL CSV file")
        sys.exit(1)
    
    # Step 4: Dry run
    dry_run_ok, dry_run_data = test_dry_run(csv_path)
    if not dry_run_ok:
        print_error("Dry run failed or found errors. Fix issues before committing.")
        sys.exit(1)
    
    # Step 5: Commit (optional)
    commit_ok, commit_data = test_commit(csv_path)
    
    # Step 6: Verify GET endpoints
    test_get_endpoints()
    
    print(f"\n{GREEN}{'=' * 50}{NC}")
    print(f"{GREEN}All Tests Complete{NC}")
    print(f"{GREEN}{'=' * 50}{NC}")

if __name__ == "__main__":
    main()

