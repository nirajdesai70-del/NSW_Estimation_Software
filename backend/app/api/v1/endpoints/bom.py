"""
BOM (Bill of Materials) endpoints
"""
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.raise_api_error import raise_api_error
from app.core.error_codes import ErrorCodes
from app.core.database import get_db
from app.api.v1.schemas.bom import BomExplodeRequest, BomExplodeResponse

router = APIRouter()


def _require_tenant_id(x_tenant_id: Optional[str]) -> int:
    """Extract and validate X-Tenant-ID header"""
    if not x_tenant_id:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_MISSING_TENANT,
            detail="X-Tenant-ID header required",
        )
    try:
        return int(x_tenant_id)
    except ValueError:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_ERROR,
            detail="X-Tenant-ID must be an integer",
        )


@router.post("/explode", response_model=BomExplodeResponse)
def explode_bom(
    payload: BomExplodeRequest,
    db: Session = Depends(get_db),
    x_tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-ID"),
):
    """
    BOM explosion (L1 → L2).
    
    Option A: unmapped L1 lines are returned in `unmapped[]` (non-fatal).
    G-08: many L1 lines may map to the same L2 SKU (aggregation supported).
    
    Returns deterministic output with SKU aggregation and provenance tracking.
    """
    tenant_id = _require_tenant_id(x_tenant_id)

    l1_ids = payload.l1_intent_line_ids
    if not l1_ids:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_MISSING_REQUIRED,
            detail="l1_intent_line_ids must be non-empty",
        )

    # 1) Fetch L1 lines (tenant-scoped)
    l1_rows = (
        db.execute(
            text("""
                SELECT id, line_type, series_bucket, description
                FROM l1_intent_lines
                WHERE tenant_id = :tenant_id AND id = ANY(:l1_ids)
            """),
            {"tenant_id": tenant_id, "l1_ids": l1_ids},
        )
        .mappings()
        .all()
    )
    l1_found_ids = {r["id"] for r in l1_rows}

    # If some requested IDs don't exist under this tenant, treat them as unmapped (non-fatal)
    missing_l1 = sorted([i for i in l1_ids if i not in l1_found_ids])

    # 2) Fetch mappings for found L1 lines
    if l1_found_ids:
        mapping_rows = (
            db.execute(
                text("""
                    SELECT l1_intent_line_id, catalog_sku_id, mapping_type, is_primary
                    FROM l1_l2_mappings
                    WHERE tenant_id = :tenant_id AND l1_intent_line_id = ANY(:l1_ids)
                """),
                {"tenant_id": tenant_id, "l1_ids": sorted(list(l1_found_ids))},
            )
            .mappings()
            .all()
        )
    else:
        mapping_rows = []

    # Group mappings by L1 id
    mappings_by_l1: Dict[int, List[Dict[str, Any]]] = {}
    for m in mapping_rows:
        mappings_by_l1.setdefault(m["l1_intent_line_id"], []).append(
            {
                "catalog_sku_id": m["catalog_sku_id"],
                "mapping_type": m["mapping_type"],
                "is_primary": bool(m["is_primary"]),
            }
        )

    # 3) Build unmapped list (non-fatal)
    unmapped: List[Dict[str, Any]] = []

    # a) L1 ids missing in DB
    for l1_id in missing_l1:
        unmapped.append(
            {
                "l1_intent_line_id": l1_id,
                "reason": "L1_NOT_FOUND",
            }
        )

    # b) L1 ids present but no mappings
    for l1_id in sorted(list(l1_found_ids)):
        if l1_id not in mappings_by_l1:
            unmapped.append(
                {
                    "l1_intent_line_id": l1_id,
                    "reason": "NO_L2_MAPPING",
                }
            )

    # 4) Optional: fetch SKU details (tenant-safe)
    sku_meta: Dict[int, Dict[str, Any]] = {}
    sku_ids = sorted({m["catalog_sku_id"] for m in mapping_rows})

    if payload.include_sku and sku_ids:
        sku_rows = (
            db.execute(
                text("""
                    SELECT id, sku_code, name, uom
                    FROM catalog_skus
                    WHERE tenant_id = :tenant_id AND id = ANY(:sku_ids)
                """),
                {"tenant_id": tenant_id, "sku_ids": sku_ids},
            )
            .mappings()
            .all()
        )
        sku_meta = {r["id"]: dict(r) for r in sku_rows}

    # 5) Build output items
    warnings: List[str] = []
    if unmapped:
        warnings.append("HAS_UNMAPPED_L1_LINES")

    # If include_attributes later: we can pull from l1_attributes and attach per l1_source.
    # For v1.0 basic feature, we keep it optional and off by default.
    # (We'll implement only if needed; doesn't block G-08)

    items: List[Dict[str, Any]] = []

    if payload.aggregate_by_sku:
        # Aggregate: SKU -> sources
        sku_bucket: Dict[int, Dict[str, Any]] = {}

        for l1_id, maps in mappings_by_l1.items():
            for mp in maps:
                sku_id = mp["catalog_sku_id"]
                bucket = sku_bucket.setdefault(
                    sku_id,
                    {
                        "catalog_sku_id": sku_id,
                        "mapping_count": 0,
                        "mapping_types": set(),
                        "l1_sources": [],
                    },
                )

                bucket["mapping_count"] += 1
                bucket["mapping_types"].add(mp["mapping_type"])
                bucket["l1_sources"].append(
                    {
                        "l1_intent_line_id": l1_id,
                        "mapping_type": mp["mapping_type"],
                        "is_primary": mp["is_primary"],
                    }
                )

        # Convert bucket to list; attach SKU meta
        for sku_id, bucket in sku_bucket.items():
            meta = sku_meta.get(sku_id, {}) if payload.include_sku else {}
            item = {
                "catalog_sku_id": sku_id,
                "sku_code": meta.get("sku_code"),
                "name": meta.get("name"),
                "uom": meta.get("uom"),
                "mapping_count": bucket["mapping_count"],
                "mapping_types": sorted(list(bucket["mapping_types"])),
                "l1_sources": sorted(bucket["l1_sources"], key=lambda x: x["l1_intent_line_id"]),
            }
            items.append(item)

        # Deterministic ordering
        items.sort(key=lambda x: x["catalog_sku_id"])

    else:
        # Non-aggregated mode: return mapping rows as-is
        for l1_id, maps in mappings_by_l1.items():
            for mp in maps:
                sku_id = mp["catalog_sku_id"]
                meta = sku_meta.get(sku_id, {}) if payload.include_sku else {}
                items.append(
                    {
                        "l1_intent_line_id": l1_id,
                        "catalog_sku_id": sku_id,
                        "mapping_type": mp["mapping_type"],
                        "is_primary": mp["is_primary"],
                        "sku_code": meta.get("sku_code"),
                        "name": meta.get("name"),
                        "uom": meta.get("uom"),
                    }
                )

        items.sort(key=lambda x: (x.get("catalog_sku_id", 0), x.get("l1_intent_line_id", 0)))

    # 6) Summary
    summary = {
        "l1_lines_requested": len(l1_ids),
        "l1_lines_found": len(l1_found_ids),
        "mappings_found": len(mapping_rows),
        "skus_found": len({i["catalog_sku_id"] for i in items}) if items else 0,
        "unmapped_l1_lines": len(unmapped),
    }

    return {
        "tenant_id": tenant_id,
        "input": {"l1_intent_line_ids": l1_ids},
        "summary": summary,
        "unmapped": unmapped,
        "items": items,
        "warnings": warnings,
    }


@router.get("/{bom_id}")
def get_bom(bom_id: int):
    """Get BOM by ID (still stub)"""
    return {"message": f"Get BOM {bom_id} endpoint - to be implemented"}


