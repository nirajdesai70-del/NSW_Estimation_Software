#!/usr/bin/env python3
"""
NSW Schema Inventory Generator from DDL
- Parses validated schema.sql to extract table/column/constraint metadata
- Generates 3 CSV files: full inventory, key-only, and diff view
"""

from __future__ import annotations
import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Column:
    name: str
    data_type: str
    nullable: bool
    default: Optional[str] = None
    is_pk: bool = False


@dataclass
class Table:
    name: str
    module: str
    columns: List[Column] = field(default_factory=list)
    foreign_keys: List[str] = field(default_factory=list)  # "col->table.col (RESTRICT)"
    unique_constraints: List[str] = field(default_factory=list)  # "col1+col2"
    check_constraints: List[str] = field(default_factory=list)  # "G-01: description"
    indexes: List[str] = field(default_factory=list)  # "idx_name"
    tenant_scoped: bool = False
    notes: str = ""


# Patterns
TABLE_COMMENT_PAT = re.compile(r"--\s*([A-Z_]+)\.([a-z_]+)", re.MULTILINE)
CREATE_TABLE_PAT = re.compile(r"CREATE TABLE\s+([a-z_]+)\s*\(", re.IGNORECASE)
COLUMN_PAT = re.compile(r"^\s+([a-z_]+)\s+([A-Z0-9()\s,]+?)\s*(?:,|\)|$)", re.IGNORECASE | re.MULTILINE)
PK_PAT = re.compile(r"PRIMARY KEY", re.IGNORECASE)
NOT_NULL_PAT = re.compile(r"NOT NULL", re.IGNORECASE)
DEFAULT_PAT = re.compile(r"DEFAULT\s+([^\s,)]+)", re.IGNORECASE)
FK_PAT = re.compile(r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s+([a-z_]+)\s*\(([^)]+)\)\s*ON DELETE\s+([A-Z]+)", re.IGNORECASE)
UNIQUE_PAT = re.compile(r"(?:UNIQUE|uq_\w+)\s*\(([^)]+)\)", re.IGNORECASE)
CHECK_PAT = re.compile(r"CHECK\s*\(([^)]+)\)", re.IGNORECASE)
INDEX_PAT = re.compile(r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+([a-z0-9_]+)\s+ON\s+([a-z_]+)", re.IGNORECASE)


def parse_schema_ddl(ddl_path: Path) -> Dict[str, Table]:
    """Parse schema.sql and extract table metadata."""
    content = ddl_path.read_text()
    
    tables: Dict[str, Table] = {}
    current_table: Optional[Table] = None
    module_map: Dict[str, str] = {}  # table_name -> module
    
    # First pass: extract table comments (module.table mapping)
    for match in TABLE_COMMENT_PAT.finditer(content):
        module = match.group(1)
        table_name = match.group(2)
        module_map[table_name] = module
    
    # Second pass: parse CREATE TABLE statements
    table_blocks = re.split(r"CREATE TABLE", content, flags=re.IGNORECASE)
    
    for block in table_blocks[1:]:  # Skip first empty split
        # Extract table name
        table_match = re.match(r"\s*([a-z_]+)\s*\(", block)
        if not table_match:
            continue
            
        table_name = table_match.group(1)
        module = module_map.get(table_name, "UNKNOWN")
        
        table = Table(name=table_name, module=module)
        tables[table_name] = table
        
        # Extract columns
        col_section = block.split('(')[1].split(')')[0] if '(' in block and ')' in block else ""
        for line in col_section.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            # Column pattern
            col_match = COLUMN_PAT.match(line)
            if col_match:
                col_name = col_match.group(1)
                type_def = col_match.group(2)
                
                is_pk = PK_PAT.search(type_def) is not None
                nullable = NOT_NULL_PAT.search(type_def) is None
                default_match = DEFAULT_PAT.search(type_def)
                default = default_match.group(1) if default_match else None
                
                # Extract base type (clean up)
                data_type = type_def.split()[0] if type_def.split() else "UNKNOWN"
                
                column = Column(
                    name=col_name,
                    data_type=data_type,
                    nullable=nullable,
                    default=default,
                    is_pk=is_pk
                )
                table.columns.append(column)
                
                # Check if tenant_scoped
                if col_name == 'tenant_id' and not nullable:
                    table.tenant_scoped = True
    
    # Third pass: parse ALTER TABLE and CREATE INDEX statements
    for line in content.split('\n'):
        line = line.strip()
        
        # Foreign keys
        fk_match = FK_PAT.search(line)
        if fk_match:
            table_name = re.search(r"ALTER TABLE\s+([a-z_]+)", line, re.IGNORECASE)
            if table_name and table_name.group(1) in tables:
                col = fk_match.group(1).strip()
                ref_table = fk_match.group(2).strip()
                ref_col = fk_match.group(3).strip()
                on_delete = fk_match.group(4).strip()
                tables[table_name.group(1)].foreign_keys.append(
                    f"{col}->{ref_table}.{ref_col} ({on_delete})"
                )
        
        # Unique constraints
        unique_match = UNIQUE_PAT.search(line)
        if unique_match:
            table_name = re.search(r"ALTER TABLE\s+([a-z_]+)", line, re.IGNORECASE)
            if table_name and table_name.group(1) in tables:
                cols = unique_match.group(1).replace(',', '+').replace(' ', '')
                tables[table_name.group(1)].unique_constraints.append(cols)
        
        # Check constraints
        check_match = CHECK_PAT.search(line)
        if check_match:
            table_name = re.search(r"ALTER TABLE\s+([a-z_]+)", line, re.IGNORECASE)
            if table_name and table_name.group(1) in tables:
                check_expr = check_match.group(1)
                # Try to identify guardrails
                if 'G-01' in line or 'product_id IS NULL' in check_expr:
                    tables[table_name.group(1)].check_constraints.append("G-01: product_id IS NULL")
                elif 'G-02' in line or ("resolution_status <> 'L2'" in check_expr and "product_id IS NOT NULL" in check_expr):
                    tables[table_name.group(1)].check_constraints.append("G-02: L2 requires product_id")
                elif 'G-06' in line or 'FIXED_NO_DISCOUNT' in check_expr:
                    tables[table_name.group(1)].check_constraints.append("G-06: FIXED_NO_DISCOUNT → discount_pct=0")
                elif 'G-07' in line or 'discount_pct BETWEEN 0 AND 100' in check_expr:
                    tables[table_name.group(1)].check_constraints.append("G-07: discount_pct 0-100")
                else:
                    tables[table_name.group(1)].check_constraints.append(check_expr[:100])
        
        # Indexes
        idx_match = INDEX_PAT.search(line)
        if idx_match:
            idx_name = idx_match.group(1)
            idx_table = idx_match.group(2)
            if idx_table in tables:
                tables[idx_table].indexes.append(idx_name)
    
    return tables


def generate_full_inventory(tables: Dict[str, Table], output_path: Path):
    """Generate full column-level inventory CSV."""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'table_name', 'column_name', 'data_type', 'nullable', 'default',
            'pk', 'fk_ref', 'indexes', 'module_owner'
        ])
        
        for table_name in sorted(tables.keys()):
            table = tables[table_name]
            for col in table.columns:
                # Find FK for this column
                fk_ref = ""
                for fk in table.foreign_keys:
                    if fk.startswith(f"{col.name}->"):
                        fk_ref = fk
                        break
                
                # Find indexes for this column
                col_indexes = [idx for idx in table.indexes if col.name.lower() in idx.lower() or 'idx_' + col.name.lower() in idx.lower()]
                
                writer.writerow([
                    table_name,
                    col.name,
                    col.data_type,
                    'false' if not col.nullable else 'true',
                    col.default or '',
                    'true' if col.is_pk else 'false',
                    fk_ref,
                    ';'.join(col_indexes) if col_indexes else '',
                    table.module
                ])


def generate_key_only_inventory(tables: Dict[str, Table], output_path: Path):
    """Generate table-level key-only inventory CSV."""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'module', 'table_name', 'tenant_scoped', 'primary_key',
            'unique_keys', 'foreign_keys', 'checks', 'indexes', 'notes'
        ])
        
        for table_name in sorted(tables.keys()):
            table = tables[table_name]
            
            # Find PK column
            pk_col = next((col.name for col in table.columns if col.is_pk), 'id')
            
            # Format constraints
            unique_str = '; '.join(table.unique_constraints) if table.unique_constraints else '—'
            fk_str = '; '.join(table.foreign_keys) if table.foreign_keys else '—'
            checks_str = '; '.join(table.check_constraints) if table.check_constraints else '—'
            indexes_str = '; '.join(table.indexes[:10]) if table.indexes else '—'  # Limit for readability
            
            writer.writerow([
                table.module,
                table_name,
                'Y' if table.tenant_scoped else 'N',
                pk_col,
                unique_str,
                fk_str,
                checks_str,
                indexes_str,
                table.notes
            ])


def generate_diff_view(full_path: Path, key_only_path: Path, output_path: Path):
    """Generate diff view comparing full and key-only inventories."""
    # Read both CSVs
    import pandas as pd
    
    full_df = pd.read_csv(full_path)
    key_only_df = pd.read_csv(key_only_path)
    
    # Get unique tables from each
    full_tables = set(full_df['table_name'].unique())
    key_only_tables = set(key_only_df['table_name'].unique())
    
    # Create diff view
    diff_rows = []
    all_tables = full_tables | key_only_tables
    
    for table in sorted(all_tables):
        in_full = table in full_tables
        in_key_only = table in key_only_tables
        
        if in_full and in_key_only:
            status = 'MATCH'
        elif in_full and not in_key_only:
            status = 'IN_FULL_ONLY'
        else:
            status = 'IN_KEY_ONLY_ONLY'
        
        full_module = full_df[full_df['table_name'] == table]['module_owner'].iloc[0] if in_full else ''
        key_module = key_only_df[key_only_df['table_name'] == table]['module'].iloc[0] if in_key_only else ''
        module_match = full_module == key_module if (in_full and in_key_only) else ''
        
        diff_rows.append({
            'table_name': table,
            'in_full': 'Y' if in_full else 'N',
            'in_key_only': 'Y' if in_key_only else 'N',
            'status': status,
            'full_module': full_module,
            'key_module': key_module,
            'module_match': 'Y' if module_match else 'N' if module_match != '' else ''
        })
    
    diff_df = pd.DataFrame(diff_rows)
    diff_df.to_csv(output_path, index=False)


def main():
    """Main entry point."""
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    ddl_path = base_dir / "DDL" / "schema.sql"
    inventory_dir = base_dir / "INVENTORY"
    inventory_dir.mkdir(exist_ok=True)
    
    print(f"Parsing DDL from: {ddl_path}")
    tables = parse_schema_ddl(ddl_path)
    print(f"Found {len(tables)} tables")
    
    # Generate full inventory
    full_path = inventory_dir / "NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv"
    print(f"Generating full inventory: {full_path}")
    generate_full_inventory(tables, full_path)
    
    # Generate key-only inventory
    key_only_path = inventory_dir / "NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv"
    print(f"Generating key-only inventory: {key_only_path}")
    generate_key_only_inventory(tables, key_only_path)
    
    # Generate diff view
    diff_path = inventory_dir / "NSW_INVENTORY_DIFF_VIEW_v1.0.csv"
    print(f"Generating diff view: {diff_path}")
    try:
        generate_diff_view(full_path, key_only_path, diff_path)
    except ImportError:
        print("Warning: pandas not available, skipping diff view generation")
        print("Install pandas: pip install pandas")
    
    print("\n✅ Inventory generation complete!")
    print(f"  - Full: {full_path}")
    print(f"  - Key-only: {key_only_path}")
    print(f"  - Diff view: {diff_path}")


if __name__ == "__main__":
    main()

