#!/usr/bin/env python3
"""
NSW Schema Canon Generator (Option-2)
- Parses CATEGORY_C_STEP1_BLUEPRINT.md for full column definitions
- Uses INVENTORY CSV for: module, tenant_scoped, foreign_keys, uniques, checks, indexes
- Emits executable schema.sql and a build report.

Assumptions:
- Blueprint tables are introduced with: "#### <table_name>" (as in your doc)
- Columns are bullet lines like: - `col_name` TYPE ... (notes allowed)
- Inventory CSV has columns: table_name,module,tenant_scoped,foreign_keys,unique_constraints,check_constraints,indexes_baseline,purpose_short,notes
"""

from __future__ import annotations
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


# ----------------------------
# Paths (repo-relative)
# ----------------------------
BASE = Path(__file__).resolve().parents[1]  # .../04_SCHEMA_CANON
BLUEPRINT = BASE / "CATEGORY_C_STEP1_BLUEPRINT.md"
INVENTORY = BASE / "INVENTORY" / "NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv"
OUT_DIR = BASE / "DDL"
OUT_SQL = OUT_DIR / "schema.sql"
OUT_REPORT = OUT_DIR / "SCHEMA_BUILD_REPORT.md"


# ----------------------------
# Helpers
# ----------------------------
SQL_TYPE_PAT = re.compile(
    r"\b(BIGSERIAL|BIGINT|INTEGER|BOOLEAN|DATE|TIMESTAMPTZ|JSONB|TEXT)\b|"
    r"(VARCHAR\s*\(\s*\d+\s*\)|NUMERIC\s*\(\s*\d+\s*,\s*\d+\s*\))",
    re.IGNORECASE,
)

HEADER_TABLE_PAT = re.compile(r"^####\s+([a-zA-Z_][a-zA-Z0-9_]*)\b", re.MULTILINE)
COL_LINE_PAT = re.compile(r"^\s*-\s+`([^`]+)`\s+(.+?)\s*$", re.MULTILINE)

# FK in blueprint is usually "FK → table.id" — we parse it for informational checks only
FK_ARROW_PAT = re.compile(r"FK\s*→\s*`?([a-zA-Z_][a-zA-Z0-9_]*)\.?([a-zA-Z_][a-zA-Z0-9_]*)?`?", re.IGNORECASE)

# Inventory FK format expected: "col->table.col (CASCADE); col2->table2.col2 (SET NULL)"
INV_FK_SPLIT = re.compile(r"\s*;\s*")
INV_FK_PAT = re.compile(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*->\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\.(\w+))?\s*(.*?)\s*$")

def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def clean_sql_expr(expr: str) -> str:
    """Clean CHECK constraint: remove annotations like [G-01], (optional), double CHECK."""
    # Remove [G-XX] annotations
    expr = re.sub(r"\[G-\d+\]", "", expr)
    # Remove (optional) notes
    expr = re.sub(r"\(optional\)", "", expr, flags=re.IGNORECASE)
    expr = norm_ws(expr)
    # Remove any accidental "CHECK (CHECK(" nesting if present
    expr = re.sub(r"CHECK\s*\(\s*CHECK\s*\(", "(", expr, flags=re.IGNORECASE)
    expr = re.sub(r"\)\s*\)\s*$", ")", expr)
    # If inventory stored "CHECK(...)" keep only inner for CHECK ( <inner> )
    # But preserve the full expression including closing parens for IN clauses
    m = re.search(r"CHECK\s*\((.+)\)\s*$", expr, flags=re.IGNORECASE | re.DOTALL)
    if m:
        inner = m.group(1).strip()
        # Ensure it has proper closing if it's an IN clause or other expression
        # Count opening and closing parens to ensure balance
        open_count = inner.count('(')
        close_count = inner.count(')')
        if open_count > close_count:
            # Missing closing parens - add them
            inner = inner + ')' * (open_count - close_count)
        return inner
    # If no CHECK wrapper, ensure balanced parens
    open_count = expr.count('(')
    close_count = expr.count(')')
    if open_count > close_count:
        expr = expr + ')' * (open_count - close_count)
    return expr

def safe_ident(name: str) -> str:
    """Basic identifier guard; assumes input already snake_case."""
    return name.strip()

def generate_constraint_name(table: str, kind: str, seq: int, expr: str = "") -> str:
    """Generate unique constraint name with descriptive tag. Always includes seq for uniqueness."""
    if kind == "ck":
        # Create tag from expression
        if "product_id IS NULL" in expr:
            tag = "g01_product_id_null"
        elif "resolution_status" in expr and "product_id" in expr:
            tag = "g02_l2_requires_product"
        elif "FIXED_NO_DISCOUNT" in expr and "discount_pct" in expr:
            tag = "g06_fixed_no_discount"
        elif "discount_pct BETWEEN" in expr:
            tag = "g07_discount_range"
        elif "IN (" in expr:
            # Extract column name and first enum value for better naming
            col_match = re.search(r"(\w+)\s+IN\s*\(", expr, re.IGNORECASE)
            enum_match = re.search(r"IN\s*\(['\"]?(\w+)", expr, re.IGNORECASE)
            if col_match and enum_match:
                col = col_match.group(1).lower()
                first_val = enum_match.group(1).lower()
                tag = f"{col}_in_{first_val}"
            else:
                tag = f"enum_{seq}"
        else:
            tag = f"check_{seq}"
        # Always append seq to ensure uniqueness
        return f"{kind}_{table}__{tag}_{seq}"
    return f"{kind}_{table}_{seq}"


# ----------------------------
# Data models
# ----------------------------
@dataclass
class BlueprintColumn:
    name: str
    col_type: str
    not_null: bool
    default: Optional[str]
    raw: str

@dataclass
class TableBlueprint:
    table: str
    columns: List[BlueprintColumn]
    # extracted notes (optional)
    uniques_hint: List[str]
    checks_hint: List[str]

@dataclass
class InventoryTable:
    table: str
    module: str
    tenant_scoped: bool
    purpose: str
    notes: str
    foreign_keys: List[Tuple[str, str, str, str]]  # (local_col, remote_table, remote_col, on_delete)
    uniques_raw: str
    checks_raw: str
    indexes_raw: str


# ----------------------------
# Parse Blueprint
# ----------------------------
def parse_blueprint(md: str) -> Dict[str, TableBlueprint]:
    """Extract per-table sections and their bullet-defined columns."""
    tables: Dict[str, TableBlueprint] = {}
    # Find table headers and slice sections
    headers = list(HEADER_TABLE_PAT.finditer(md))
    for i, h in enumerate(headers):
        table = h.group(1).strip()
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(md)
        section = md[start:end]

        # columns
        cols: List[BlueprintColumn] = []
        for m in COL_LINE_PAT.finditer(section):
            col_name = m.group(1).strip()
            remainder = m.group(2).strip()

            # Skip id column if it's just "PK" (we handle id separately as BIGSERIAL PRIMARY KEY)
            if col_name == "id" and (remainder.strip() == "PK" or remainder.strip().startswith("PK")):
                continue

            # Extract type
            type_m = SQL_TYPE_PAT.search(remainder)
            if not type_m:
                continue
            # Handle both group 1 (simple types) and group 2 (parameterized types)
            col_type = (type_m.group(1) or type_m.group(2) or "").upper().replace(" ", "")

            # NOT NULL / DEFAULT
            not_null = bool(re.search(r"\bNOT\s+NULL\b", remainder, flags=re.IGNORECASE))
            # Extract DEFAULT - look for DEFAULT followed by value, stop at FK, UNIQUE, or end
            default_m = re.search(r"\bDEFAULT\b\s+([^\s]+(?:\s+[^\s]+)*?)(?:\s+FK|\s+UNIQUE|\s*$)", remainder, flags=re.IGNORECASE)
            if not default_m:
                # Try simpler pattern
                default_m = re.search(r"\bDEFAULT\b\s+([^\s]+)", remainder, flags=re.IGNORECASE)
            default_val = norm_ws(default_m.group(1)) if default_m else None
            # Clean default value (handle now(), booleans, and string literals)
            if default_val:
                default_val = default_val.strip()
                if default_val.lower() == "now()":
                    default_val = "now()"
                elif default_val.lower() in ("true", "false"):
                    default_val = default_val.lower()
                elif default_val.upper() in ("ACTIVE", "INACTIVE", "DRAFT", "APPROVED", "FINALIZED"):
                    # Preserve as-is (will be quoted in SQL if needed)
                    default_val = f"'{default_val}'"
                elif not default_val.startswith("'") and not default_val.isdigit() and "." not in default_val:
                    # String literal - add quotes if not already quoted
                    default_val = f"'{default_val}'"

            cols.append(BlueprintColumn(
                name=col_name,
                col_type=col_type,
                not_null=not_null,
                default=default_val,
                raw=remainder
            ))

        # hints (informational; not used for enforcement)
        uniques_hint = []
        checks_hint = []
        for line in section.splitlines():
            if "**Unique:**" in line or "Unique:" in line:
                uniques_hint.append(norm_ws(line))
            if "**Check:**" in line or "Check:" in line:
                checks_hint.append(norm_ws(line))

        if cols:
            tables[table] = TableBlueprint(table=table, columns=cols, uniques_hint=uniques_hint, checks_hint=checks_hint)

    return tables


# ----------------------------
# Parse Inventory CSV
# ----------------------------
def parse_inventory(path: Path) -> Dict[str, InventoryTable]:
    inv: Dict[str, InventoryTable] = {}
    with path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            table = (row.get("table_name") or "").strip()
            if not table:
                continue

            module = (row.get("module") or "").strip()
            tenant_scoped = ((row.get("tenant_scoped") or "").strip().upper() == "Y")
            purpose = (row.get("purpose_short") or "").strip()
            notes = (row.get("notes") or "").strip()

            fks_raw = (row.get("foreign_keys") or "").strip()
            fks: List[Tuple[str, str, str, str]] = []
            if fks_raw and fks_raw != "—":
                for part in INV_FK_SPLIT.split(fks_raw):
                    part = part.strip()
                    if not part:
                        continue
                    # Parse: "col->table.col (CASCADE)" or "col->table.id (SET NULL)"
                    m = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*->\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\.(\w+))?\s*(.*?)\s*$", part)
                    if not m:
                        continue
                    local = m.group(1)
                    rtbl = m.group(2)
                    rcol = m.group(3) or "id"
                    policy_blob = (m.group(4) or "").upper()
                    on_delete = "RESTRICT"
                    if "CASCADE" in policy_blob:
                        on_delete = "CASCADE"
                    elif "SET NULL" in policy_blob or "SET_NULL" in policy_blob:
                        on_delete = "SET NULL"
                    elif "RESTRICT" in policy_blob:
                        on_delete = "RESTRICT"
                    fks.append((local, rtbl, rcol, on_delete))

            inv[table] = InventoryTable(
                table=table,
                module=module,
                tenant_scoped=tenant_scoped,
                purpose=purpose,
                notes=notes,
                foreign_keys=fks,
                uniques_raw=(row.get("unique_constraints") or "").strip(),
                checks_raw=(row.get("check_constraints") or "").strip(),
                indexes_raw=(row.get("indexes_baseline") or "").strip(),
            )
    return inv


# ----------------------------
# DDL assembly
# ----------------------------
def topo_sort_tables(inv: Dict[str, InventoryTable]) -> List[str]:
    """Kahn-ish topo sort based on FK dependencies, ignoring self-references."""
    deps: Dict[str, set] = {t: set() for t in inv.keys()}
    rev: Dict[str, set] = {t: set() for t in inv.keys()}

    for t, info in inv.items():
        for (_, rtbl, _, _) in info.foreign_keys:
            if rtbl == t:
                continue
            if rtbl in inv:
                deps[t].add(rtbl)
                rev[rtbl].add(t)

    ready = [t for t in inv.keys() if len(deps[t]) == 0]
    ready.sort()
    out: List[str] = []
    while ready:
        n = ready.pop(0)
        out.append(n)
        for child in sorted(rev[n]):
            deps[child].discard(n)
            if len(deps[child]) == 0:
                if child not in out and child not in ready:
                    ready.append(child)
                    ready.sort()

    # add any remaining (cycles/self refs)
    for t in sorted(inv.keys()):
        if t not in out:
            out.append(t)
    return out


def ddl_for_table(table: str, inv: InventoryTable, bp: Optional[TableBlueprint]) -> Tuple[str, List[str]]:
    """Returns (create_table_sql, post_sql_lines[])"""
    lines: List[str] = []
    post: List[str] = []

    lines.append(f"-- {inv.module}.{table}")
    if inv.purpose:
        lines.append(f"-- Purpose: {inv.purpose}")
    if inv.notes:
        lines.append(f"-- Notes: {inv.notes}")

    lines.append(f"CREATE TABLE {safe_ident(table)} (")

    # Build column list
    col_map: Dict[str, BlueprintColumn] = {}
    if bp:
        for c in bp.columns:
            col_map[c.name] = c

    # Ensure id exists (BIGSERIAL PK)
    lines.append("    id BIGSERIAL PRIMARY KEY,")

    # tenant_id if tenant_scoped (inventory-driven)
    if inv.tenant_scoped:
        if "tenant_id" in col_map:
            c = col_map["tenant_id"]
            nn = " NOT NULL" if c.not_null or inv.tenant_scoped else ""
            lines.append(f"    tenant_id BIGINT{nn},")
        else:
            lines.append("    tenant_id BIGINT NOT NULL,")

    # Add remaining blueprint columns (skip id; skip tenant_id already added above)
    if bp:
        for c in bp.columns:
            if c.name in ("id", "tenant_id"):
                continue
            # Basic formatting: use parsed type, NOT NULL, DEFAULT
            nn = " NOT NULL" if c.not_null else ""
            dv = f" DEFAULT {c.default}" if c.default else ""
            lines.append(f"    {safe_ident(c.name)} {c.col_type}{nn}{dv},")
    else:
        # placeholder if no blueprint section exists
        lines.append("    -- TODO: Missing blueprint section for this table; add columns per Step-1,")
        lines.append("    placeholder_col TEXT NULL,")

    # Timestamps: only add if not already present in blueprint
    if not bp or ("created_at" not in col_map):
        lines.append("    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),")
    if not bp or ("updated_at" not in col_map):
        lines.append("    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()")

    # Ensure last comma correctness
    if lines[-1].endswith(","):
        lines[-1] = lines[-1].rstrip(",")

    lines.append(");")
    lines.append("")

    # FKs (inventory-driven)
    for i, (lcol, rtbl, rcol, ondel) in enumerate(inv.foreign_keys, start=1):
        cname = f"fk_{table}_{lcol}"
        post.append(f"ALTER TABLE {table} ADD CONSTRAINT {cname} FOREIGN KEY ({lcol}) REFERENCES {rtbl}({rcol}) ON DELETE {ondel};")

    # Uniques (inventory-driven; supports partial uniques)
    u = inv.uniques_raw
    if u and u != "—":
        for j, part in enumerate([p.strip() for p in u.split(";") if p.strip()], start=1):
            part_u = part
            # Remove any "(recommended)" etc
            part_u = re.sub(r"\(recommended\)", "", part_u, flags=re.IGNORECASE).strip()

            m_partial = re.search(r"UNIQUE\s*\(([^)]+)\)\s+WHERE\s+(.+)$", part_u, flags=re.IGNORECASE)
            m_plain = re.search(r"UNIQUE\s*\(([^)]+)\)", part_u, flags=re.IGNORECASE)

            if m_partial:
                cols = norm_ws(m_partial.group(1))
                cond = norm_ws(m_partial.group(2))
                # Clean condition
                cond = re.sub(r"\(optional\)", "", cond, flags=re.IGNORECASE).strip()
                idx_name = f"ux_{table}_{j}"
                post.append(f"CREATE UNIQUE INDEX {idx_name} ON {table} ({cols}) WHERE {cond};")
            elif m_plain:
                cols = norm_ws(m_plain.group(1))
                cname = f"uq_{table}_{j}"
                post.append(f"ALTER TABLE {table} ADD CONSTRAINT {cname} UNIQUE ({cols});")

    # Checks (inventory-driven)
    c = inv.checks_raw
    if c and c != "—":
        for k, part in enumerate([p.strip() for p in c.split(";") if p.strip()], start=1):
            expr = clean_sql_expr(part)
            cname = generate_constraint_name(table, "ck", k, expr)
            post.append(f"ALTER TABLE {table} ADD CONSTRAINT {cname} CHECK ({expr});")

    # Indexes baseline (inventory-driven)
    if inv.tenant_scoped:
        post.append(f"CREATE INDEX idx_{table}_tenant_id ON {table} (tenant_id);")

    # Additionally parse baseline index list like: "INDEX(col); INDEX(col2,col3)"
    idx = inv.indexes_raw
    if idx and idx != "—":
        for m in re.finditer(r"INDEX\s*\(([^)]+)\)", idx, flags=re.IGNORECASE):
            cols = norm_ws(m.group(1))
            # avoid duplicate tenant index
            if cols.lower().replace(" ", "") == "tenant_id":
                continue
            # Create unique index name
            iname = f"ix_{table}_{abs(hash(cols)) % 10_000_000}"
            post.append(f"CREATE INDEX {iname} ON {table} ({cols});")

    return "\n".join(lines), post


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    bp_text = BLUEPRINT.read_text(encoding="utf-8")
    blueprint_tables = parse_blueprint(bp_text)
    inv_tables = parse_inventory(INVENTORY)

    order = topo_sort_tables(inv_tables)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ddl_lines: List[str] = []
    ddl_lines.append(f"-- NSW Schema Canon v1.0 - DDL (Blueprint-driven)")
    ddl_lines.append(f"-- Generated: {now}")
    ddl_lines.append(f"-- Blueprint: {BLUEPRINT.name}")
    ddl_lines.append(f"-- Inventory: {INVENTORY.name}")
    ddl_lines.append("")
    ddl_lines.append("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    ddl_lines.append("")

    post_all: List[str] = []
    missing_bp: List[str] = []
    present_bp = set(blueprint_tables.keys())

    for t in order:
        inv = inv_tables[t]
        bp = blueprint_tables.get(t)
        if not bp:
            missing_bp.append(t)
        create_sql, post_sql = ddl_for_table(t, inv, bp)
        ddl_lines.append(create_sql)
        post_all.extend(post_sql)

    ddl_lines.append("-- Constraints / Indexes")
    ddl_lines.append("")
    ddl_lines.extend(post_all)
    ddl_lines.append("")
    ddl_lines.append("-- END")

    OUT_SQL.write_text("\n".join(ddl_lines) + "\n", encoding="utf-8")

    # Report
    report = []
    report.append(f"# SCHEMA_BUILD_REPORT.md")
    report.append("")
    report.append(f"Generated: {now}")
    report.append("")
    report.append(f"Tables in inventory: **{len(inv_tables)}**")
    report.append(f"Tables with blueprint sections: **{len(present_bp & set(inv_tables.keys()))}**")
    report.append("")
    if missing_bp:
        report.append("## Tables missing from Blueprint (placeholders emitted)")
        for t in missing_bp:
            report.append(f"- {t}")
    else:
        report.append("## Blueprint coverage")
        report.append("✅ All inventory tables have blueprint sections.")

    report.append("")
    report.append("## Next verification commands")
    report.append("```bash")
    report.append(f"psql -v ON_ERROR_STOP=1 -f {OUT_SQL.as_posix()}")
    report.append("```")

    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"✅ Wrote: {OUT_SQL}")
    print(f"✅ Wrote: {OUT_REPORT}")
    if missing_bp:
        print("⚠️ Missing blueprint sections for:", ", ".join(missing_bp))


if __name__ == "__main__":
    main()

