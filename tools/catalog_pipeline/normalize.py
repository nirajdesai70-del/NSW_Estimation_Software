#!/usr/bin/env python3
"""
Price List Normalizer
Converts OEM price lists to standardized CSV format using YAML profiles.

Handles wide sheets with empty columns by collapsing rows to non-empty cells first.
Supports TEST/FINAL mode separation for governance.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

import pandas as pd
import yaml

SKU_REGEX = re.compile(r"\b([A-Z0-9]+(?:[A-Z0-9\-])*[*]{0,2})\b")  # keeps * and **


def load_profile(profile_path: str) -> dict:
    """Load YAML profile."""
    with open(profile_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collapse_row_to_cells(row) -> list[str]:
    """
    Collapse a pandas Series row to list of non-empty cells.
    Handles wide sheets with lots of empty columns.
    FIX (2025-12-26): Also splits cells that contain multiple values separated by 2+ spaces
    (e.g., "1000 A  630 A  500  375  -  -  LC1E630*  212810" -> separate cells)
    FIX (2025-12-26): Also handles cells with newlines that contain multiple data rows
    (e.g., "20  4NO  LC1E06004*IN  1915  2280\n32  4NO  LC1E12004*IN  -  -  2115" -> split by newline first)
    """
    cells = []
    for v in row.tolist():
        if pd.isna(v):
            continue
        s = str(v).strip()
        if not s:
            continue
        
        # FIX (2025-12-26): If cell contains newlines, it might have multiple data rows
        # Split by newline first, then process each line
        if '\n' in s and re.search(r'\bLC1E\d+', s, re.IGNORECASE):
            # This cell contains multiple data rows (common in 4P contactor tables)
            lines = s.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Check if this line has 2+ spaces (data row) or is a heading
                if re.search(r'\s{2,}|\t', line):
                    # Split on 2+ spaces or tabs
                    parts = re.split(r'\s{2,}|\t+', line)
                    for part in parts:
                        part = part.strip()
                        if part:
                            part = re.sub(r"\s+", " ", part)
                            cells.append(part)
                else:
                    # Single value or heading - normalize and add
                    line = re.sub(r"\s+", " ", line)
                    cells.append(line)
        # FIX (2025-12-26): Check for multiple spaces BEFORE normalizing
        # If cell contains 2+ consecutive spaces or tabs, split it first
        elif re.search(r'\s{2,}|\t', s):
            # Split on 2+ spaces or tabs, but preserve single spaces within values
            parts = re.split(r'\s{2,}|\t+', s)
            for part in parts:
                part = part.strip()
                if part:
                    # Normalize whitespace within each part
                    part = re.sub(r"\s+", " ", part)
                    cells.append(part)
        else:
            # Normalize whitespace
            s = re.sub(r"\s+", " ", s)
            cells.append(s)
    return cells


def parse_price(x: str) -> float | int | None:
    """Parse price string to numeric value."""
    if x is None:
        return None
    s = str(x).strip()
    s = s.replace(",", "")
    # remove common currency artifacts
    s = re.sub(r"[^\d\.]", "", s)
    if not s:
        return None
    try:
        val = float(s)
        return int(val) if val.is_integer() else val
    except Exception:
        return None


def extract_sku(sku_raw: str) -> tuple[str | None, str]:
    """
    Extract SKU code from raw text.
    Example input: "LC1E0601* 0" -> ("LC1E0601*", "LC1E0601* 0")
    Keeps * or ** in code.
    """
    if sku_raw is None:
        return None, ""
    text = str(sku_raw).strip()
    text = re.sub(r"\s+", " ", text)

    # common issue: "LC1E0601* 0" -> capture first token-like sku
    m = SKU_REGEX.search(text)
    if not m:
        return None, text
    sku = m.group(1)

    # remove trailing standalone "0" if present (as part of the notes, not sku)
    # (we keep sku unchanged)
    return sku, text


def is_valid_sku(sku_code: str | None) -> bool:
    """
    Validate SKU code.
    Must contain at least one alphabet character (not purely numeric).
    """
    if not sku_code:
        return False
    
    # Must contain at least one letter
    if not re.search(r"[A-Za-z]", sku_code):
        return False
    
    # Reject very short codes (likely junk)
    if len(sku_code.strip()) < 3:
        return False
    
    return True


def infer_series_from_sku(sku_code: str | None, sku_prefixes: dict[str, str] | None = None) -> str | None:
    """
    Infer series from SKU prefix (fallback when heading-based series is missing).
    Example: LC1E0601 -> LC1E, LP1K123 -> LP1K
    """
    if not sku_code:
        return None
    
    # Extract prefix (first 4-5 alphanumeric characters before numbers)
    match = re.match(r"^([A-Z]{2,4}[0-9]?[A-Z]?)", sku_code.upper())
    if match:
        prefix = match.group(1)
        # If profile has prefix mappings, use them
        if sku_prefixes and prefix in sku_prefixes:
            return sku_prefixes[prefix]
        return prefix
    
    return None


def is_heading_row(cells: list[str], heading_patterns: list[str] | None = None) -> tuple[bool, str | None]:
    """
    Detect if row is a series heading.
    Returns (is_heading, series_name).
    Handles cases where heading text is in one cell with newlines.
    """
    if not cells:
        return False, None
    
    # Join all cells to handle multi-line headings
    all_text = " ".join(cells).strip()
    all_text_lower = all_text.lower()
    
    # Profile-defined heading patterns
    if heading_patterns:
        for pattern in heading_patterns:
            if pattern.lower() in all_text_lower:
                # Return the pattern itself (standardized name)
                # This ensures scope matching works correctly
                return True, pattern
    
    # Common heading indicators
    heading_indicators = [
        "Power Contactors",
        "Control Relays",
        "Overload Relay",
        "Circuit Breakers",
        "Motor Circuit Breakers",
        "Switches",
        "Accessories",
        "TeSys",
        "Easy TeSys",
    ]
    
    for indicator in heading_indicators:
        if indicator.lower() in all_text_lower:
            # Extract the relevant part
            for cell in cells:
                if indicator.lower() in cell.lower():
                    cleaned = re.sub(r"\s+\d+\s*$", "", cell.strip())
                    return True, cleaned
    
    return False, None


def should_ignore_row(cells: list[str], ignore_terms: list[str]) -> bool:
    """Check if row should be ignored based on ignore terms."""
    if not ignore_terms:
        return False
    joined = " ".join(cells).lower()
    for t in ignore_terms:
        if t.lower() in joined:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(
        description="Normalize OEM price lists to standard CSV format"
    )
    ap.add_argument("--profile", required=True, help="Path to profile YAML")
    ap.add_argument("--file", required=True, help="Input XLSX file path")
    ap.add_argument("--mode", choices=["test", "final"], default="test",
                    help="Import mode: test (disposable) or final (canonical)")
    ap.add_argument("--outdir", help="Custom output directory (overrides mode-based routing)")
    ap.add_argument("--errdir", help="Custom errors directory (overrides mode-based routing)")
    ap.add_argument("--logdir", help="Custom logs directory (overrides mode-based routing)")
    args = ap.parse_args()

    profile = load_profile(args.profile)
    make = profile["make"]
    sheet = profile.get("sheet", 0)
    mode = args.mode

    # Route directories based on mode (unless overridden)
    base_dir = "tools/catalog_pipeline"
    if args.outdir:
        outdir = args.outdir
    else:
        outdir = os.path.join(base_dir, "output", mode)
    
    if args.errdir:
        errdir = args.errdir
    else:
        errdir = os.path.join(base_dir, "errors", mode)
    
    if args.logdir:
        logdir = args.logdir
    else:
        logdir = os.path.join(base_dir, "logs", mode)

    os.makedirs(outdir, exist_ok=True)
    os.makedirs(errdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)

    # Read Excel as strings to preserve formatting
    df = pd.read_excel(args.file, sheet_name=sheet, dtype=str, header=None)

    ignore_terms = profile.get("filters", {}).get("ignore_if_contains_any", [])
    drop_if_missing = set(profile.get("filters", {}).get("drop_if_missing", []))
    cols = profile["columns_by_index"]
    defaults = profile.get("defaults", {})
    
    # Series detection configuration
    heading_patterns = profile.get("series", {}).get("heading_patterns", [])
    sku_prefixes = profile.get("series", {}).get("sku_prefix_mappings", {})
    series_aliases = profile.get("series", {}).get("aliases", {}) or {}
    
    # Scope filtering (include only specified series)
    scope_series = profile.get("scope", {}).get("include_series_contains_any", [])

    # Section markers (legacy support)
    section_markers = profile.get("section_markers", [])
    current_section = {}
    current_series = None  # Heading-based series
    series_locked = False  # Lock series once we enter a table (prevents later headings from overriding)

    out_rows = []
    err_rows = []
    seen = set()  # (make, sku_code) for duplicate detection

    total_rows = 0
    dropped = 0
    duplicates = 0
    rows_candidate_sku = 0
    rows_invalid_sku = 0
    rows_non_sku_skipped = 0
    
    # Diagnostics for dropped LP1K rows
    diag_enabled = bool(profile.get("diagnostics", {}).get("enable", False))
    diag_max = int(profile.get("diagnostics", {}).get("max_rows", 30))
    diag_rows = []

    # Optional: find start row if specified
    start_row = 0
    start_keywords = profile.get("start_row_contains_any", [])
    if start_keywords:
        for idx in range(min(20, len(df))):  # Check first 20 rows
            row = df.iloc[idx]
            cells = collapse_row_to_cells(row)
            joined = " ".join(cells).lower()
            if any(kw.lower() in joined for kw in start_keywords):
                start_row = idx + 1  # Start after header row
                break

    for idx in range(start_row, len(df)):
        row = df.iloc[idx]
        cells = collapse_row_to_cells(row)
        
        # DEBUG (2025-12-26): Track row 75 (LC1E630) for debugging
        debug_row_75 = (idx == 74)  # Row 75 is index 74

        if not cells:
            continue

        # FIX (2025-12-26): Collect all SKUs in row BEFORE heading check (needed for multi-SKU extraction)
        # This must be collected early so it's available for multi-SKU extraction later
        multi_sku_list = []  # Track all SKUs found in this row
        for cell in cells:
            if cell and re.search(r'\bLC1E\d+[A-Z0-9]*\b', str(cell), re.IGNORECASE):
                matches = re.findall(r'\b(LC1E\d+[A-Z0-9]*)\b', str(cell), re.IGNORECASE)
                multi_sku_list.extend(matches)
        # Remove duplicates while preserving order
        seen_skus = set()
        unique_multi_sku_list = []
        for sku in multi_sku_list:
            if sku.upper() not in seen_skus:
                seen_skus.add(sku.upper())
                unique_multi_sku_list.append(sku)
        multi_sku_list = unique_multi_sku_list

        # Check for series heading row (Tier 1: heading-based)
        is_heading, heading_series = is_heading_row(cells, heading_patterns)
        if is_heading and heading_series:
            # FIX (2025-12-26): Don't skip if row also contains SKU data (multi-SKU rows like row 107)
            # Check if row contains LC1E SKUs - if so, it's a data row, not just a heading
            has_sku_data = False
            for cell in cells:
                if cell and re.search(r'\bLC1E\d+[A-Z0-9]*\b', str(cell), re.IGNORECASE):
                    has_sku_data = True
                    break
            
            if has_sku_data:
                # This row has both heading and data - process as data row
                # Apply alias mapping to normalize series name
                if heading_series in series_aliases:
                    heading_series = series_aliases[heading_series]
                if not series_locked:
                    current_series = heading_series
                # Continue processing as data row (don't skip)
            else:
                # Pure heading row - skip it
                # Apply alias mapping to normalize series name
                if heading_series in series_aliases:
                    heading_series = series_aliases[heading_series]
                if not series_locked:
                    current_series = heading_series
                # Don't treat heading row as data
                continue

        # Section marker detection (legacy support, e.g., FRAME-3)
        # FIX (2025-12-26): FRAME rows contain actual data (SKU + price), so don't skip them.
        # Only skip if it's a standalone section marker row (no SKU data).
        # FIX (2025-12-26): Use flexible SKU detection (check for LC1E pattern anywhere in row)
        section_found = False
        for sm in section_markers:
            pat = re.compile(sm["pattern"], re.IGNORECASE)
            if cells and pat.search(cells[0]):
                # Check if this row also contains SKU data (if so, it's a data row, not just a marker)
                # Use flexible detection - check for LC1E SKU pattern anywhere in the row
                has_sku_data = False
                for cell in cells:
                    if cell and re.search(r'\bLC1E\d+[A-Z0-9]*\b', str(cell), re.IGNORECASE):
                        has_sku_data = True
                        break
                
                if has_sku_data:
                    # This is a data row with FRAME marker, process it
                    current_section[sm["capture_as"]] = cells[0]
                    # Don't skip - continue processing
                else:
                    # This is just a section marker row, skip it
                    current_section[sm["capture_as"]] = cells[0]
                    section_found = True
                break
        if section_found:
            continue

        total_rows += 1

        # FIX (2025-12-26): Don't ignore rows that contain SKU data, even if they match ignore terms
        # (e.g., row 107 has "TeSys" but also has LC1E SKUs - should be processed)
        has_sku_in_row = len(multi_sku_list) > 0
        if should_ignore_row(cells, ignore_terms) and not has_sku_in_row:
            dropped += 1
            continue

        # Check if first cell is a FRAME marker (shifts all columns by 1)
        has_frame_in_row = False
        if cells and re.match(r"^FRAME[- ]?\d+", cells[0], re.IGNORECASE):
            has_frame_in_row = True
        
        # Build a small dict from indexed cells (adjust for FRAME if present)
        def get_cell(key):
            i = cols.get(key)
            if i is None:
                return None
            # If FRAME is in this row (not just current_section), shift index by 1
            if has_frame_in_row and key not in ["frame"]:
                i = i + 1
            return cells[i] if i < len(cells) else None

        sku_raw = get_cell("sku_raw")
        sku_pos_in_row = None  # Track actual SKU position for price detection
        
        # FIX (2025-12-26): If multi_sku_list was collected before, use it; otherwise collect now
        # (multi_sku_list should already be populated from before heading check, but safety check)
        if not multi_sku_list:
            for cell in cells:
                if cell and re.search(r'\bLC1E\d+[A-Z0-9]*\b', str(cell), re.IGNORECASE):
                    matches = re.findall(r'\b(LC1E\d+[A-Z0-9]*)\b', str(cell), re.IGNORECASE)
                    multi_sku_list.extend(matches)
        
        # FIX (2025-12-26): For 4P contactors, SKU may be at different positions (2 or 3 instead of 6)
        # Try flexible detection if configured position doesn't have a valid SKU
        if not sku_raw or not re.search(r"[A-Za-z]", str(sku_raw)):
            if multi_sku_list:
                # Use first SKU from multi-SKU list
                sku_raw = multi_sku_list[0]
                # Find position
                for i, cell in enumerate(cells):
                    if multi_sku_list[0].upper() in str(cell).upper():
                        sku_pos_in_row = i
                        break
            else:
                # FIX (2025-12-26): For LC1D standard motor duty table, SKU may be in cell 0 (single-cell format)
                # Scan first few cells (0-3) for LC1D/LP1D patterns
                lc1d_pattern = re.compile(r'\b(LC1D[A-Z0-9]{2,8}[*#]{0,2}|LP1D[A-Z0-9]{3,8}[*#]{0,2})\b', re.IGNORECASE)
                for i in range(min(4, len(cells))):
                    cell_text = str(cells[i])
                    match = lc1d_pattern.search(cell_text)
                    if match:
                        sku_raw = match.group(1)
                        sku_pos_in_row = i
                        break
                
                if not sku_raw or not re.search(r"[A-Za-z]", str(sku_raw)):
                    rows_non_sku_skipped += 1
                    continue
        elif sku_raw and sku_pos_in_row is None:
            # SKU found at configured position, but position not set - find it
            for i, cell in enumerate(cells):
                if str(sku_raw).upper() in str(cell).upper():
                    sku_pos_in_row = i
                    break
        
        # If we found SKU at a different position, use that for price scanning
        if sku_pos_in_row is not None:
            # Override get_cell for this row to use the detected SKU position
            original_get_cell = get_cell
            def get_cell_flexible(key):
                if key == "sku_raw":
                    return cells[sku_pos_in_row] if sku_pos_in_row < len(cells) else None
                return original_get_cell(key)
            get_cell = get_cell_flexible

        rows_candidate_sku += 1
        
        # LP1K-style tables: price columns may vary; scan forward from sku_raw
        # FIX (2025-12-26): For 4P contactors, always scan forward from SKU position
        pricing_config = profile.get("pricing", {})
        price_scan_from_sku = pricing_config.get("scan_forward_from_sku_raw", False)
        # Always scan if SKU was found at non-standard position (4P contactors)
        if sku_pos_in_row is not None:
            price_scan_from_sku = True
        price_scan_window = int(pricing_config.get("scan_window", 8))
        price_raw = None
        
        if price_scan_from_sku:
            # Find sku_raw position in collapsed cells
            if sku_pos_in_row is not None:
                # Use the detected position
                sku_pos = sku_pos_in_row
            else:
                # Try to find it
                try:
                    sku_str = str(sku_raw).strip()
                    sku_pos = None
                    for idx, cell in enumerate(cells):
                        if str(cell).strip() == sku_str or sku_str in str(cell):
                            sku_pos = idx
                            break
                except (ValueError, AttributeError):
                    sku_pos = None
            
            if sku_pos is not None:
                # FIX (2025-12-26): For single-cell format (LC1D standard motor duty table),
                # SKU and prices may be in the same cell. Parse within cell if needed.
                sku_cell_content = str(cells[sku_pos])
                sku_str = str(sku_raw).strip()
                
                # Check if cell contains SKU followed by numbers (likely prices in same cell)
                if sku_str in sku_cell_content and len(sku_cell_content.split()) > 5:
                    # Split cell content and find SKU position within it
                    cell_parts = sku_cell_content.split()
                    sku_in_cell_pos = None
                    for i, part in enumerate(cell_parts):
                        if sku_str.upper() in part.upper():
                            sku_in_cell_pos = i
                            break
                    
                    # If SKU found in cell, scan forward within same cell for prices
                    if sku_in_cell_pos is not None:
                        for j in range(sku_in_cell_pos + 1, min(len(cell_parts), sku_in_cell_pos + 5)):
                            candidate = cell_parts[j]
                            if candidate != "-" and parse_price(candidate) is not None:
                                price_val = parse_price(candidate)
                                # Valid price range check (reasonable for contactors: 1000-100000)
                                if price_val and 1000 <= price_val <= 100000:
                                    price_raw = candidate
                                    break
                
                # If no price found in same cell, scan forward to next cells (multi-cell format)
                if price_raw is None:
                    for j in range(sku_pos + 1, min(len(cells), sku_pos + 1 + price_scan_window)):
                        cand = cells[j]
                        if cand and str(cand).strip() != "-" and parse_price(cand) is not None:
                            price_val = parse_price(cand)
                            if price_val and 1000 <= price_val <= 100000:
                                price_raw = cand
                                break
        
        # Fallback to configured list_price column if scan didn't find a price
        if price_raw is None:
            price_raw = get_cell("list_price")
        
        # If price is "-" or empty, try next columns until we find a numeric value
        # FIX (2025-12-26): For large frame contactors (FRAME-5, FRAME-6, etc.), price is often
        # at position 9 (after SKU at 7, and "-" at 8). The fallback must account for FRAME shift.
        # Check if price is invalid (None, empty, "-", or non-numeric)
        if not price_raw or price_raw in ["-", ""] or parse_price(price_raw) is None:
            # Get the actual position where we looked (accounting for FRAME shift)
            # For FRAME rows: get_cell("list_price") already shifted by 1, so we need the base position
            price_base_idx = cols.get("list_price", 7)
            if has_frame_in_row:
                # get_cell already added 1, so price_base_idx should be the position after shift
                # But we want the actual cell position, so we add 1 more to account for FRAME
                price_base_idx = price_base_idx + 1
            # Try next 8 columns for price (increased from 6 to 8 for large frames)
            # This handles: small frames (price at 7), large frames (price at 9), and LP1K BD/FD/MD variants
            for offset in range(1, 9):
                price_idx = price_base_idx + offset
                if price_idx < len(cells):
                    candidate = cells[price_idx]
                    if candidate and candidate != "-" and parse_price(candidate) is not None:
                        price_raw = candidate
                        break

        sku_code, notes = extract_sku(sku_raw)
        
        # Lock series once we start seeing LC1E rows (prevents later headings overriding)
        # FIX (2025-12-26): Don't lock too early - allow 4P headings to set series
        if sku_code and sku_code.upper().startswith("LC1E") and current_series:
            # Only lock if we already have a series set (prevents overriding with wrong series)
            series_locked = True
        
        # SKU validation (must contain alphabet, not purely numeric)
        if not is_valid_sku(sku_code):
            rows_invalid_sku += 1
            err_rows.append({
                "row_index": idx + 1,
                "reason": "Invalid SKU (fails validation)",
                "cells": " | ".join(cells),
            })
            continue
        
        price = parse_price(price_raw)

        # If price scan fails for LP1K rows, treat as dropped (not an error)
        if price is None and sku_code and sku_code.upper().startswith("LP1K"):
            dropped += 1
            # Capture diagnostic sample for dropped LP1K rows
            if diag_enabled and len(diag_rows) < diag_max:
                try:
                    sku_str = str(sku_raw).strip()
                    sku_pos = None
                    for k, cell in enumerate(cells):
                        if sku_str in str(cell):
                            sku_pos = k
                            break
                except Exception:
                    sku_pos = None
                
                window = []
                if sku_pos is not None:
                    window = cells[sku_pos: min(len(cells), sku_pos + 26)]
                diag_rows.append({
                    "row_index": idx + 1,
                    "sku_raw": str(sku_raw),
                    "sku_code": sku_code or "",
                    "window_cells": " | ".join(window) if window else "NO_SKU_POS",
                    "reason": "NO_NUMERIC_PRICE_FOUND",
                })
            continue

        # Required field checks
        missing = []
        if "sku_raw" in drop_if_missing and (not sku_raw or not sku_code):
            missing.append("sku_code")
        if "list_price" in drop_if_missing and price is None:
            missing.append("list_price")

        if missing:
            # DEBUG (2025-12-26): Log row 75 if dropped by missing fields
            if debug_row_75:
                print(f"DEBUG Row 75: Dropped by missing fields: {missing}. sku_code: {sku_code}, price: {price}", file=sys.stderr)
            err_rows.append({
                "row_index": idx + 1,
                "reason": f"Missing/invalid fields: {', '.join(missing)}",
                "cells": " | ".join(cells),
            })
            continue

        key = (make, sku_code)
        if key in seen:
            duplicates += 1
            # last-wins: remove previous row with same key
            out_rows = [r for r in out_rows if not (r["make"] == make and r["sku_code"] == sku_code)]
        else:
            seen.add(key)

        # Determine series (Tier 1: heading-based, Tier 2: SKU-prefix fallback)
        # FIX (2025-12-26): Always try SKU prefix inference if current_series is None or doesn't match scope,
        # even when series_locked. This ensures large frame contactors (far from headings)
        # are still detected via their SKU prefix.
        series = None
        if series_locked and sku_code and sku_code.upper().startswith("LC1E"):
            # Use current_series if available, otherwise infer from SKU
            series = current_series if current_series else infer_series_from_sku(sku_code, sku_prefixes)
        elif not series_locked:
            # Not locked, use current_series if available, otherwise infer
            series = current_series if current_series else infer_series_from_sku(sku_code, sku_prefixes)
        else:
            # Series is locked but SKU is not LC1E - use SKU prefix inference
            series = infer_series_from_sku(sku_code, sku_prefixes)
        
        # Final fallback: if still no series, try inference
        if not series:
            series = infer_series_from_sku(sku_code, sku_prefixes)
        
        # Additional safety: if we have a series but it doesn't match scope and SKU suggests LC1E,
        # try inference to get the correct series name
        if series and scope_series and sku_code and sku_code.upper().startswith("LC1E"):
            series_lower = series.lower()
            if not any(pattern.lower() in series_lower for pattern in scope_series):
                # Current series doesn't match scope, try inference
                inferred = infer_series_from_sku(sku_code, sku_prefixes)
                if inferred:
                    series = inferred
        
        # Normalize series to canonical label (alias map)
        if series:
            series = series_aliases.get(series, series)
        
        # Scope filtering: skip rows that don't match included series
        if scope_series and series:
            # Check if series matches any scope pattern
            series_lower = series.lower()
            if not any(pattern.lower() in series_lower for pattern in scope_series):
                # DEBUG (2025-12-26): Log row 75 if dropped by scope
                if debug_row_75:
                    print(f"DEBUG Row 75: Dropped by scope filter. Series: {series}, Scope: {scope_series}", file=sys.stderr)
                # Capture diagnostic for dropped LP1K rows (scope filter)
                if diag_enabled and len(diag_rows) < diag_max and sku_code and sku_code.upper().startswith("LP1K"):
                    try:
                        sku_str = str(sku_raw).strip()
                        sku_pos = None
                        for k, cell in enumerate(cells):
                            if sku_str in str(cell):
                                sku_pos = k
                                break
                    except Exception:
                        sku_pos = None
                    window = []
                    if sku_pos is not None:
                        window = cells[sku_pos: min(len(cells), sku_pos + 26)]
                    diag_rows.append({
                        "row_index": idx + 1,
                        "sku_raw": str(sku_raw),
                        "sku_code": sku_code,
                        "window_cells": " | ".join(window) if window else "NO_SKU_POS",
                        "reason": "SCOPE_FILTER_MISMATCH",
                    })
                dropped += 1
                continue
        elif scope_series and not series:
            # If scope is defined but no series detected, skip row
            # Capture diagnostic for dropped LP1K rows (no series detected)
            if diag_enabled and len(diag_rows) < diag_max and sku_code and sku_code.upper().startswith("LP1K"):
                try:
                    sku_str = str(sku_raw).strip()
                    sku_pos = None
                    for k, cell in enumerate(cells):
                        if sku_str in str(cell):
                            sku_pos = k
                            break
                except Exception:
                    sku_pos = None
                window = []
                if sku_pos is not None:
                    window = cells[sku_pos: min(len(cells), sku_pos + 26)]
                diag_rows.append({
                    "row_index": idx + 1,
                    "sku_raw": str(sku_raw),
                    "sku_code": sku_code,
                    "window_cells": " | ".join(window) if window else "NO_SKU_POS",
                    "reason": "NO_SERIES_DETECTED",
                })
            dropped += 1
            continue
        
        # Optional fields for description
        # FIX (2025-12-26): For 4P contactors, column structure is different
        # 4P structure: [Rating, PoleConfig, SKU, Price1, Price2, ...]
        # 3P structure: [AC1, AC3, HP, kW, NO, NC, SKU, Price]
        is_4p_row = False
        if sku_code:
            clean_sku = sku_code.upper().rstrip('*')
            if clean_sku.endswith("04") or clean_sku.endswith("08"):
                is_4p_row = True
        
        if is_4p_row and sku_pos_in_row is not None and sku_pos_in_row >= 2:
            # 4P row structure: use cells around SKU
            ac1 = cells[sku_pos_in_row - 2] if sku_pos_in_row >= 2 else None  # Rating
            ac3 = cells[sku_pos_in_row - 1] if sku_pos_in_row >= 1 else None  # Pole config (4NO or 2NO+2NC)
            hp = None
            kw = None
            aux_no = None
            aux_nc = None
        else:
            # 3P row structure: use configured columns
            ac1 = get_cell("ac1")
            ac3 = get_cell("ac3")
            hp = get_cell("hp")
            kw = get_cell("kw")
            aux_no = get_cell("aux_no")
            aux_nc = get_cell("aux_nc")
        
        # Use FRAME from row if present, otherwise from section marker
        frame = cells[0] if has_frame_in_row else current_section.get("frame")

        # Determine pole configuration from SKU pattern or row context
        pole_config = None
        if sku_code:
            clean_sku = sku_code.upper().rstrip('*')
            if clean_sku.endswith("04") or clean_sku.endswith("08"):
                pole_config = "4P"
            elif clean_sku.endswith("02"):
                pole_config = "2P"
            else:
                # Check row context for 4P indicators
                row_str = " ".join(cells).lower()
                if "4 pole" in row_str or "4p" in row_str or "4no" in row_str or "2no+2nc" in row_str:
                    pole_config = "4P"
                elif "2 pole" in row_str or "2p" in row_str:
                    pole_config = "2P"
                else:
                    pole_config = "3P"  # Default assumption for LC1E

        desc_parts = [defaults.get("description_prefix", "Item")]
        if frame:
            desc_parts.append(frame)
        if pole_config:
            desc_parts.append(f"Poles={pole_config}")
        if ac1:
            desc_parts.append(f"AC1={ac1}")
        if ac3:
            desc_parts.append(f"AC3={ac3}")
        if hp:
            desc_parts.append(f"HP={hp}")
        if kw:
            desc_parts.append(f"kW={kw}")
        if aux_no is not None and aux_nc is not None:
            desc_parts.append(f"Aux(NO/NC)={aux_no}/{aux_nc}")

        description = " | ".join(desc_parts)

        out_rows.append({
            "import_stage": mode.upper(),  # TEST or FINAL
            "make": make,
            "series": series or "",  # Empty string if no series detected
            "sku_code": sku_code,
            "description": description,
            "uom": defaults.get("uom", "EA"),
            "list_price": price,
            "currency": defaults.get("currency", "INR"),
            "notes": notes,
        })
        
        # FIX (2025-12-26): If this row has multiple SKUs, process the remaining ones
        # Note: multi_sku_list is collected before heading check, so it should be available here
        # But if it's empty, collect it again (safety check)
        if not multi_sku_list:
            for cell in cells:
                if cell and re.search(r'\bLC1E\d+[A-Z0-9]*\b', str(cell), re.IGNORECASE):
                    matches = re.findall(r'\b(LC1E\d+[A-Z0-9]*)\b', str(cell), re.IGNORECASE)
                    multi_sku_list.extend(matches)
        
        if len(multi_sku_list) > 1:
            # Normalize the first SKU for comparison (remove asterisk)
            first_sku_clean = sku_code.upper().rstrip('*') if sku_code else None
            processed_skus = {first_sku_clean} if first_sku_clean else set()
            for other_sku in multi_sku_list:
                other_sku_clean = other_sku.upper().rstrip('*')
                if other_sku_clean in processed_skus:
                    continue
                processed_skus.add(other_sku_clean)
                
                # Find position of this SKU in cells
                other_sku_pos = None
                for i, cell in enumerate(cells):
                    if other_sku.upper() in str(cell).upper():
                        other_sku_pos = i
                        break
                
                if other_sku_pos is not None:
                    # Extract SKU code
                    other_sku_raw = cells[other_sku_pos]
                    other_sku_code, other_notes = extract_sku(other_sku_raw)
                    
                    if not is_valid_sku(other_sku_code):
                        continue
                    
                    # Find price for this SKU (scan forward from SKU position)
                    other_price = None
                    for j in range(other_sku_pos + 1, min(len(cells), other_sku_pos + 6)):
                        price_candidate = cells[j]
                        other_price = parse_price(price_candidate)
                        if other_price:
                            break
                    
                    if other_price is None:
                        continue  # Skip if no price found
                    
                    # Build description for this SKU
                    other_is_4p = other_sku_code.upper().rstrip('*').endswith("04") or other_sku_code.upper().rstrip('*').endswith("08")
                    if other_is_4p and other_sku_pos >= 2:
                        other_ac1 = cells[other_sku_pos - 2] if other_sku_pos >= 2 else None
                        other_ac3 = cells[other_sku_pos - 1] if other_sku_pos >= 1 else None
                    else:
                        other_ac1 = get_cell("ac1")
                        other_ac3 = get_cell("ac3")
                    
                    other_pole_config = "4P" if other_is_4p else "3P"
                    other_desc_parts = [defaults.get("description_prefix", "Item")]
                    if frame:
                        other_desc_parts.append(frame)
                    other_desc_parts.append(f"Poles={other_pole_config}")
                    if other_ac1:
                        other_desc_parts.append(f"AC1={other_ac1}")
                    if other_ac3:
                        other_desc_parts.append(f"AC3={other_ac3}")
                    other_description = " | ".join(other_desc_parts)
                    
                    # Check for duplicates
                    other_key = (make, other_sku_code)
                    if other_key not in seen:
                        seen.add(other_key)
                        out_rows.append({
                            "import_stage": mode.upper(),
                            "make": make,
                            "series": series or "",
                            "sku_code": other_sku_code,
                            "description": other_description,
                            "uom": defaults.get("uom", "EA"),
                            "list_price": other_price,
                            "currency": defaults.get("currency", "INR"),
                            "notes": other_notes or "",
                        })

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(args.file))[0]
    out_csv = os.path.join(outdir, f"{make.lower()}_{base}_normalized_{ts}.csv")
    err_xlsx = os.path.join(errdir, f"{make.lower()}_{base}_errors_{ts}.xlsx")
    log_json = os.path.join(logdir, f"{make.lower()}_{base}_summary_{ts}.json")

    # Ensure output columns are in correct order
    output_columns = [
        "import_stage",
        "make",
        "series",
        "sku_code",
        "description",
        "uom",
        "list_price",
        "currency",
        "notes",
    ]
    
    df_out = pd.DataFrame(out_rows)
    # Reorder columns if they exist
    existing_cols = [col for col in output_columns if col in df_out.columns]
    df_out = df_out[existing_cols]
    df_out.to_csv(out_csv, index=False, encoding="utf-8")

    if err_rows:
        pd.DataFrame(err_rows).to_excel(err_xlsx, index=False, engine="openpyxl")

    summary = {
        "make": make,
        "mode": mode,
        "input_file": args.file,
        "output_csv": out_csv,
        "errors_file": err_xlsx if err_rows else None,
        "counts": {
            "rows_seen": total_rows,
            "rows_output": len(out_rows),
            "rows_error": len(err_rows),
            "rows_dropped": dropped,
            "duplicates_skipped": duplicates,
            "rows_candidate_sku": rows_candidate_sku,
            "rows_invalid_sku": rows_invalid_sku,
            "rows_non_sku_skipped": rows_non_sku_skipped,
        },
        "series_coverage": {
            "rows_with_series": sum(1 for r in out_rows if r.get("series")),
            "rows_without_series": sum(1 for r in out_rows if not r.get("series")),
        },
    }
    with open(log_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Write diagnostic CSV if enabled and rows captured
    if diag_enabled:
        if diag_rows:
            diag_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            diag_path = os.path.join(base_dir, "diagnostics", f"{make.lower()}_{base}_lp1k_dropped_samples_{diag_ts}.csv")
            os.makedirs(os.path.dirname(diag_path), exist_ok=True)
            pd.DataFrame(diag_rows).to_csv(diag_path, index=False, encoding="utf-8")
            print("🧪 Diagnostics written:", diag_path, f"({len(diag_rows)} rows)")
        else:
            print("🧪 Diagnostics enabled but no dropped LP1K rows captured")
    
    print("✅ Normalization complete")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
