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
    """
    cells = []
    for v in row.tolist():
        if pd.isna(v):
            continue
        s = str(v).strip()
        if not s:
            continue
        # normalize whitespace
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
    base_dir = "tools/price_normalizer"
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

        if not cells:
            continue

        # Check for series heading row (Tier 1: heading-based)
        is_heading, heading_series = is_heading_row(cells, heading_patterns)
        if is_heading and heading_series:
            if not series_locked:
                current_series = heading_series
            # Don't treat heading row as data
            continue

        # Section marker detection (legacy support, e.g., FRAME-3)
        section_found = False
        for sm in section_markers:
            pat = re.compile(sm["pattern"], re.IGNORECASE)
            if cells and pat.search(cells[0]):
                current_section[sm["capture_as"]] = cells[0]
                # don't treat marker row as data
                section_found = True
                break
        if section_found:
            continue

        total_rows += 1

        if should_ignore_row(cells, ignore_terms):
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
        
        # Candidate SKU heuristic should depend on the sku_raw cell, not the whole row
        if not sku_raw or not re.search(r"[A-Za-z]", str(sku_raw)):
            rows_non_sku_skipped += 1
            continue

        rows_candidate_sku += 1
        price_raw = get_cell("list_price")
        
        # If price is "-" or empty, try next columns until we find a numeric value
        if price_raw in ["-", "", None]:
            price_base_idx = cols.get("list_price", 7)
            if has_frame_in_row:
                price_base_idx += 1  # Already shifted by get_cell, but need base for next attempts
            # Try next 3 columns for price
            for offset in range(1, 4):
                price_idx = price_base_idx + offset
                if price_idx < len(cells):
                    candidate = cells[price_idx]
                    if candidate and candidate != "-" and parse_price(candidate) is not None:
                        price_raw = candidate
                        break

        sku_code, notes = extract_sku(sku_raw)
        
        # Lock series once we start seeing LC1E rows (prevents later headings overriding)
        if sku_code and sku_code.upper().startswith("LC1E"):
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

        # Required field checks
        missing = []
        if "sku_raw" in drop_if_missing and (not sku_raw or not sku_code):
            missing.append("sku_code")
        if "list_price" in drop_if_missing and price is None:
            missing.append("list_price")

        if missing:
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
        # If series is locked, only use it for LC1E SKUs; otherwise use SKU prefix inference
        if series_locked and sku_code and sku_code.upper().startswith("LC1E"):
            series = current_series
        elif not series_locked:
            series = current_series
        else:
            # Series is locked but SKU is not LC1E - use SKU prefix inference
            series = None
        
        if not series:
            series = infer_series_from_sku(sku_code, sku_prefixes)
        
        # Normalize series to canonical label (alias map)
        if series:
            series = series_aliases.get(series, series)
        
        # Scope filtering: skip rows that don't match included series
        if scope_series and series:
            # Check if series matches any scope pattern
            series_lower = series.lower()
            if not any(pattern.lower() in series_lower for pattern in scope_series):
                dropped += 1
                continue
        elif scope_series and not series:
            # If scope is defined but no series detected, skip row
            dropped += 1
            continue
        
        # Optional fields for description
        ac1 = get_cell("ac1")
        ac3 = get_cell("ac3")
        hp = get_cell("hp")
        kw = get_cell("kw")
        aux_no = get_cell("aux_no")
        aux_nc = get_cell("aux_nc")
        # Use FRAME from row if present, otherwise from section marker
        frame = cells[0] if has_frame_in_row else current_section.get("frame")

        desc_parts = [defaults.get("description_prefix", "Item")]
        if frame:
            desc_parts.append(frame)
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

    print("✅ Normalization complete")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
