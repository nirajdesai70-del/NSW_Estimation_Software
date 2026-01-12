#!/usr/bin/env python3
"""
validate_against_v6_v2.py

Fail-fast validator: compares a rebuilt workbook against the golden v6 workbook.
Supports --report to write validation results to markdown file.

Checks:
- Required sheets exist
- Row counts match for selected sheets
- Key columns exist
- Content hash matches for selected key columns (order-insensitive)

Usage:
  python3 validate_against_v6_v2.py --golden /path/to/v6.xlsx --rebuilt /path/to/rebuilt.xlsx --sheets P8_T1_CANONICAL_ROWS --report report.md
"""

import argparse
import hashlib
import pandas as pd
from pathlib import Path
from datetime import datetime

DEFAULT_SHEETS = [
    "P8_T1_CANONICAL_ROWS",
    "P8_T1_COIL_PRICES",
    "P8_T3_CANONICAL_ROWS",
    "P8_T3_COIL_PRICES",
    "NSW_L2_PRODUCTS",
    "NSW_PRICE_MATRIX",
    "NSW_L1_CONFIG_LINES",
]

KEY_COLS = {
    "P8_T1_CANONICAL_ROWS": ["base_ref_clean","frame_label","poles","ac1_A","ac3_A","motor_hp","motor_kw","aux_no","aux_nc"],
    "P8_T1_COIL_PRICES": ["base_ref_clean","coil_code","voltage_type","voltage_V","price_inr"],
    "P8_T3_CANONICAL_ROWS": ["base_ref_clean","frame_label","poles","ac1_A","ac3_A","motor_hp","motor_kw"],
    "P8_T3_COIL_PRICES": ["base_ref_clean","coil_code","voltage_type","voltage_V","price_inr"],
    "NSW_L2_PRODUCTS": ["l2_product_code","series_name","series_bucket","poles","frame_label","generic_name"],
    "NSW_PRICE_MATRIX": ["l2_product_code","variant_code","voltage_type","voltage_V","rate_inr","effective_from"],
    "NSW_L1_CONFIG_LINES": ["l2_product_code","duty_class","duty_current_A","variant_code","selected_voltage_V","selected_voltage_type","motor_kw","motor_hp","aux_no","aux_nc"],
}

def df_signature(df: pd.DataFrame, cols: list[str]) -> str:
    d = df.copy()
    missing = [c for c in cols if c not in d.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")
    d = d[cols].fillna("")
    for c in cols:
        d[c] = d[c].astype(str).str.strip()
    d = d.sort_values(by=cols).reset_index(drop=True)
    payload = d.to_csv(index=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", required=True, help="Path to golden v6 xlsx")
    ap.add_argument("--rebuilt", required=True, help="Path to rebuilt xlsx to validate")
    ap.add_argument("--sheets", nargs="*", default=DEFAULT_SHEETS, help="Sheets to compare")
    ap.add_argument("--report", help="Path to write validation report (markdown)")
    args = ap.parse_args()

    g = pd.ExcelFile(args.golden)
    r = pd.ExcelFile(args.rebuilt)

    errors = []
    results = []
    status = "PASS"

    # Check sheet presence
    for sh in args.sheets:
        if sh not in g.sheet_names:
            errors.append(f"[GOLDEN] missing sheet: {sh}")
        if sh not in r.sheet_names:
            errors.append(f"[REBUILT] missing sheet: {sh}")

    if errors:
        status = "FAIL"
        if args.report:
            report_path = Path(args.report)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, 'w') as f:
                f.write(f"# Validation Report\n\n")
                f.write(f"**Status**: ❌ **{status}**\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Golden**: `{args.golden}`\n")
                f.write(f"**Rebuilt**: `{args.rebuilt}`\n\n")
                f.write(f"## Errors\n\n")
                for e in errors:
                    f.write(f"- {e}\n")
        print("FAIL: sheet presence check")
        for e in errors:
            print(" -", e)
        raise SystemExit(2)

    # Validate each sheet
    for sh in args.sheets:
        gdf = pd.read_excel(args.golden, sheet_name=sh)
        rdf = pd.read_excel(args.rebuilt, sheet_name=sh)

        sheet_result = {
            "sheet": sh,
            "golden_rows": len(gdf),
            "rebuilt_rows": len(rdf),
            "rowcount_match": len(gdf) == len(rdf),
            "signature_match": None,
            "errors": []
        }

        if len(gdf) != len(rdf):
            errors.append(f"[{sh}] rowcount differs: golden={len(gdf)} rebuilt={len(rdf)}")
            sheet_result["errors"].append(f"Rowcount differs: golden={len(gdf)} rebuilt={len(rdf)}")
            status = "FAIL"

        cols = KEY_COLS.get(sh)
        if cols:
            try:
                gs = df_signature(gdf, cols)
                rs = df_signature(rdf, cols)
                sheet_result["signature_match"] = gs == rs
                if gs != rs:
                    errors.append(f"[{sh}] content differs (key-col signature mismatch)")
                    sheet_result["errors"].append("Content differs (key-col signature mismatch)")
                    status = "FAIL"
            except KeyError as ke:
                errors.append(f"[{sh}] {ke}")
                sheet_result["errors"].append(str(ke))
                status = "FAIL"
        
        results.append(sheet_result)

    # Write report if requested
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(f"# Validation Report\n\n")
            f.write(f"**Status**: {'✅' if status == 'PASS' else '❌'} **{status}**\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Golden**: `{args.golden}`\n")
            f.write(f"**Rebuilt**: `{args.rebuilt}`\n\n")
            f.write(f"## Results\n\n")
            f.write(f"| Sheet | Golden Rows | Rebuilt Rows | Rowcount Match | Signature Match | Status |\n")
            f.write(f"|-------|-------------|--------------|----------------|-----------------|--------|\n")
            for r in results:
                row_match = "✅" if r["rowcount_match"] else "❌"
                sig_match = "✅" if r["signature_match"] else ("❌" if r["signature_match"] is False else "N/A")
                sheet_status = "✅ PASS" if r["rowcount_match"] and (r["signature_match"] is None or r["signature_match"]) else "❌ FAIL"
                f.write(f"| {r['sheet']} | {r['golden_rows']} | {r['rebuilt_rows']} | {row_match} | {sig_match} | {sheet_status} |\n")
            
            if errors:
                f.write(f"\n## Errors\n\n")
                for e in errors:
                    f.write(f"- {e}\n")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(2)

    print("PASS: rebuilt workbook matches golden v6 on all configured checks.")

if __name__ == "__main__":
    main()

