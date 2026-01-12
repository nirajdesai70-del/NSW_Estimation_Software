# KB Refresh Tool

**Purpose:** Populate RAG Knowledge Pack from Phase 5 sources

## Usage

```bash
# Dry run (see what would be done)
python3 tools/kb_refresh/run_kb_refresh.py --dry-run

# Actual refresh
python3 tools/kb_refresh/run_kb_refresh.py

# Verbose output
python3 tools/kb_refresh/run_kb_refresh.py --verbose
```

## What It Does

1. Scans Phase 5 folders (`docs/PHASE_5/`, `tools/catalog_pipeline_v2/`, etc.)
2. Selects latest/final file per folder (CANONICAL > most recent)
3. Copies files to `RAG_KB/phase5_pack/` with metadata headers
4. Builds `00_INDEX.json` manifest
5. Generates `00_FOLDER_MAP.md` structure map
6. Produces `DELTA_SINCE_LAST.md` report

## Output

All outputs go to:
- `RAG_KB/phase5_pack/` - Knowledge pack files
- `RAG_KB/build_reports/` - Delta and gap reports

## Configuration

Edit `SCAN_ROOTS` in `run_kb_refresh.py` to add/remove scan locations.

