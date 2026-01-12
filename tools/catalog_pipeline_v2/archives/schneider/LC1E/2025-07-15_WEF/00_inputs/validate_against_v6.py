#!/usr/bin/env python3
"""
validate_against_v6.py

Fail-fast validator: compares a rebuilt workbook against the golden v6 workbook.

Checks:
- Required sheets exist
- Row counts match for selected sheets
- Key columns exist
- Content hash matches for selected key columns (order-insensitive)

Usage:
  python3 validate_against_v6.py --golden /path/to/v6.xlsx --rebuilt /path/to/rebuilt.xlsx
"""

import argparse
import hashlib
import pandas as pd

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
    args = ap.parse_args()

    g = pd.ExcelFile(args.golden)
    r = pd.ExcelFile(args.rebuilt)

    errors = []

    for sh in args.sheets:
        if sh not in g.sheet_names:
            errors.append(f"[GOLDEN] missing sheet: {sh}")
        if sh not in r.sheet_names:
            errors.append(f"[REBUILT] missing sheet: {sh}")

    if errors:
        print("FAIL: sheet presence check")
        for e in errors:
            print(" -", e)
        raise SystemExit(2)

    for sh in args.sheets:
        gdf = pd.read_excel(args.golden, sheet_name=sh)
        rdf = pd.read_excel(args.rebuilt, sheet_name=sh)

        if len(gdf) != len(rdf):
            errors.append(f"[{sh}] rowcount differs: golden={len(gdf)} rebuilt={len(rdf)}")

        cols = KEY_COLS.get(sh)
        if cols:
            try:
                gs = df_signature(gdf, cols)
                rs = df_signature(rdf, cols)
                if gs != rs:
                    errors.append(f"[{sh}] content differs (key-col signature mismatch)")
            except KeyError as ke:
                errors.append(f"[{sh}] {ke}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(2)

    print("PASS: rebuilt workbook matches golden v6 on all configured checks.")

if __name__ == "__main__":
    main()
