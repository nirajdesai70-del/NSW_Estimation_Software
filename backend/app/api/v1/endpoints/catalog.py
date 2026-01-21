"""
Catalog endpoints (v1)
SKU-first, item-browse friendly
"""
import csv
import io
import re
import uuid
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File

from app.core.raise_api_error import raise_api_error
from app.core.error_codes import ErrorCodes
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.catalog import (
    CatalogItem,
    CatalogSku,
    SkuPrice,
    PriceList,
    SKUType,
)

router = APIRouter(tags=["catalog"])

# Required columns for import
REQUIRED_COLUMNS = {"make", "sku_code", "uom", "list_price", "currency"}
OPTIONAL_COLUMNS = {"import_stage", "series", "description", "notes"}


def _to_decimal(x: str) -> Optional[Decimal]:
    """Convert string to Decimal, return None if invalid."""
    try:
        return Decimal(str(x).strip())
    except (InvalidOperation, ValueError, AttributeError):
        return None


def slugify(s: str) -> str:
    """Create stable slug from string for item_code generation."""
    s = (s or "").upper().strip()
    s = re.sub(r"[^A-Z0-9]+", "_", s)
    return s.strip("_")[:100]


@router.get("/items")
def list_items(
    q: Optional[str] = Query(default=None),
    make: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """
    List catalog items (browse/search).
    NOTE: Pricing truth is SKU; items are grouping/browse entities.
    """
    query = db.query(CatalogItem)

    if make:
        query = query.filter(CatalogItem.make == make)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(CatalogItem.item_code.ilike(like), CatalogItem.name.ilike(like)))

    total = query.count()
    items = (
        query.order_by(CatalogItem.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [
            {
                "id": i.id,
                "item_code": i.item_code,
                "name": i.name,
                "make": i.make,
                "category": i.category,
                "is_active": i.is_active,
                "created_at": i.created_at,
                "updated_at": i.updated_at,
            }
            for i in items
        ],
    }


@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get catalog item by ID.
    """
    item = db.query(CatalogItem).filter(CatalogItem.id == item_id).one_or_none()
    if not item:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_ITEM,
            detail="Item not found",
        )

    skus = (
        db.query(CatalogSku)
        .filter(CatalogSku.catalog_item_id == item.id)
        .order_by(CatalogSku.sku_code.asc())
        .all()
    )

    return {
        "id": item.id,
        "item_code": item.item_code,
        "name": item.name,
        "description": item.description,
        "make": item.make,
        "category": item.category,
        "is_active": item.is_active,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "skus": [
            {
                "id": s.id,
                "sku_code": s.sku_code,
                "sku_type": s.sku_type.value if s.sku_type else None,
                "name": s.name,
                "description": s.description,
                "make": s.make,
                "uom": s.uom,
                "is_active": s.is_active,
                "current_price": str(s.current_price) if s.current_price is not None else None,
                "current_currency": s.current_currency,
                "current_price_updated_at": s.current_price_updated_at,
            }
            for s in skus
        ],
    }


@router.get("/skus")
def list_skus(
    q: Optional[str] = Query(default=None),
    make: Optional[str] = Query(default=None),
    item_id: Optional[int] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """
    List SKUs (pricing truth).
    """
    query = db.query(CatalogSku)

    if make:
        query = query.filter(CatalogSku.make == make)

    if item_id:
        query = query.filter(CatalogSku.catalog_item_id == item_id)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            CatalogSku.sku_code.ilike(like),
            CatalogSku.name.ilike(like),
            CatalogSku.description.ilike(like),
        ))

    total = query.count()
    skus = (
        query.order_by(CatalogSku.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "skus": [
            {
                "id": s.id,
                "catalog_item_id": s.catalog_item_id,
                "sku_code": s.sku_code,
                "sku_type": s.sku_type.value if s.sku_type else None,
                "name": s.name,
                "make": s.make,
                "uom": s.uom,
                "is_active": s.is_active,
                "current_price": str(s.current_price) if s.current_price is not None else None,
                "current_currency": s.current_currency,
                "current_price_updated_at": s.current_price_updated_at,
            }
            for s in skus
        ],
    }


@router.get("/skus/{sku_id}")
def get_sku(sku_id: int, db: Session = Depends(get_db)):
    """
    Get SKU by ID.
    """
    sku = db.query(CatalogSku).filter(CatalogSku.id == sku_id).one_or_none()
    if not sku:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_SKU,
            detail="SKU not found",
        )

    prices = (
        db.query(SkuPrice)
        .filter(SkuPrice.sku_id == sku.id)
        .order_by(SkuPrice.effective_from.desc(), SkuPrice.id.desc())
        .limit(50)
        .all()
    )

    return {
        "id": sku.id,
        "catalog_item_id": sku.catalog_item_id,
        "sku_code": sku.sku_code,
        "sku_type": sku.sku_type.value if sku.sku_type else None,
        "name": sku.name,
        "description": sku.description,
        "make": sku.make,
        "uom": sku.uom,
        "is_active": sku.is_active,
        "current_price": str(sku.current_price) if sku.current_price is not None else None,
        "current_currency": sku.current_currency,
        "current_price_updated_at": sku.current_price_updated_at,
        "price_history": [
            {
                "id": p.id,
                "price_list_id": p.price_list_id,
                "price": str(p.price),
                "currency": p.currency,
                "effective_from": p.effective_from,
                "effective_to": p.effective_to,
                "import_batch_id": getattr(p, "import_batch_id", None),
                "source_file": getattr(p, "source_file", None),
                "created_at": p.created_at,
            }
            for p in prices
        ],
    }


@router.post("/skus/import")
def import_skus(
    file: UploadFile = File(..., description="CSV price list"),
    dry_run: bool = Query(default=True, description="Validate only, do not write"),
    db: Session = Depends(get_db),
):
    """
    Import SKUs from a FINAL CSV price list.
    - SKU is the pricing truth (ADR-0001)
    - Auto-creates CatalogItem grouped by series
    - Upserts CatalogSku (make+sku_code unique)
    - Creates PriceList for the batch
    - Archives prices in SkuPrice
    - Updates CatalogSku.current_price for fast quoting
    
    Behavior:
    - dry_run=True: validate only, return errors
    - dry_run=False: reject if any errors, else commit
    """
    if not file.filename:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_MISSING_REQUIRED,
            detail="No file provided",
        )

    # Read file content
    content = file.file.read()
    try:
        text = content.decode("utf-8")
    except Exception:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_ERROR,
            detail="File must be UTF-8 CSV",
        )

    # Parse CSV
    reader = csv.DictReader(io.StringIO(text))
    cols = set(reader.fieldnames or [])

    # Validate required columns
    missing_cols = REQUIRED_COLUMNS - cols
    if missing_cols:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_MISSING_REQUIRED,
            detail=f"Missing required columns: {sorted(list(missing_cols))}",
        )

    batch_id = str(uuid.uuid4())
    source_file = file.filename
    now = datetime.utcnow()

    rows = list(reader)
    errors = []
    valid = []

    # --- Row validation ---
    for i, r in enumerate(rows, start=2):  # CSV header is row 1
        make = (r.get("make") or "").strip()
        sku_code = (r.get("sku_code") or "").strip()
        uom = (r.get("uom") or "").strip()
        currency = (r.get("currency") or "").strip().upper()
        price_raw = (r.get("list_price") or "").strip()
        stage = (r.get("import_stage") or "").strip().upper()

        # FINAL-only guard (strict governance)
        if stage and stage != "FINAL":
            errors.append({
                "row": i,
                "field": "import_stage",
                "error": "Only FINAL imports allowed",
                "value": stage
            })
            continue

        # Required field validation
        if not make or not sku_code:
            errors.append({
                "row": i,
                "field": "make/sku_code",
                "error": "Required fields missing",
                "value": f"make='{make}', sku_code='{sku_code}'"
            })
            continue

        # SKU validation
        if len(sku_code) < 3 or not any(c.isalpha() for c in sku_code):
            errors.append({
                "row": i,
                "field": "sku_code",
                "error": "Invalid SKU (must be at least 3 chars and contain letters)",
                "value": sku_code
            })
            continue

        # Currency validation
        if currency and len(currency) != 3:
            errors.append({
                "row": i,
                "field": "currency",
                "error": "Must be 3-letter code (e.g., INR, USD)",
                "value": currency
            })
            continue

        # Price validation
        price = _to_decimal(price_raw)
        if price is None or price < 0:
            errors.append({
                "row": i,
                "field": "list_price",
                "error": "Invalid price (must be numeric >= 0)",
                "value": price_raw
            })
            continue

        valid.append({
            "make": make,
            "sku_code": sku_code,
            "series": (r.get("series") or "").strip() or None,
            "description": (r.get("description") or "").strip() or None,
            "uom": uom or "EA",
            "currency": currency or "INR",
            "notes": (r.get("notes") or "").strip() or None,
            "list_price": price,
            "import_stage": (r.get("import_stage") or "").strip() or None,
        })

    summary = {
        "batch_id": batch_id,
        "source_file": source_file,
        "rows_total": len(rows),
        "rows_valid": len(valid),
        "rows_error": len(errors),
        "dry_run": dry_run,
        "errors_sample": errors[:50],  # Limit error sample
    }

    # If dry_run or errors exist, return summary
    if dry_run:
        return summary

    # Reject commit if errors exist (strict governance)
    if errors:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.CONFLICT_IMPORT_HAS_ERRORS,
            detail={
                "message": "Cannot commit import with validation errors. Fix errors first.",
                "summary": summary,
            },
        )

    # --- DB writes (upsert) ---
    items_created = 0
    skus_created = 0
    skus_updated = 0
    prices_inserted = 0

    # Create or reuse PriceList for this batch (idempotent)
    valid_make = valid[0]["make"] if valid else "Unknown"
    valid_currency = valid[0]["currency"] if valid else "INR"
    price_list_name = f"{valid_make} - {source_file}"
    price_list = (
        db.query(PriceList)
        .filter(PriceList.name == price_list_name)
        .one_or_none()
    )
    if price_list is None:
        price_list = PriceList(
            name=price_list_name,
            description=f"Imported from {source_file}, batch={batch_id}",
            currency=valid_currency,
            effective_from=now,
            effective_to=None,
            is_active=True,
        )
        db.add(price_list)
        db.flush()  # Get price_list.id

    # Group by series for CatalogItem creation
    series_to_item = {}  # series -> CatalogItem

    for r in valid:
        # Auto-create CatalogItem grouped by series (Option A)
        series = r.get("series") or "UNSPECIFIED"
        if series not in series_to_item:
            # Create or find CatalogItem for this series using stable slug
            item_code = f"{slugify(r['make'])}__{slugify(series)}"
            catalog_item = (
                db.query(CatalogItem)
                .filter(CatalogItem.item_code == item_code)
                .one_or_none()
            )
            if catalog_item is None:
                catalog_item = CatalogItem(
                    item_code=item_code,
                    name=series,
                    description=None,
                    make=r["make"],
                    category="Contactor",  # v1 default
                    is_active=True,
                )
                db.add(catalog_item)
                db.flush()
                items_created += 1
            series_to_item[series] = catalog_item

        catalog_item = series_to_item[series]

        # Upsert CatalogSku
        sku = (
            db.query(CatalogSku)
            .filter(CatalogSku.make == r["make"], CatalogSku.sku_code == r["sku_code"])
            .one_or_none()
        )

        if sku is None:
            sku = CatalogSku(
                catalog_item_id=catalog_item.id,
                sku_code=r["sku_code"],
                sku_type=SKUType.PRIMARY,
                name=r["sku_code"],  # v1: use SKU code as name
                description=r.get("description"),
                make=r["make"],
                uom=r["uom"],
                is_active=True,
            )
            db.add(sku)
            db.flush()
            skus_created += 1
        else:
            # Last-wins update + ensure linked
            sku.catalog_item_id = catalog_item.id
            sku.description = r.get("description") or sku.description
            sku.uom = r.get("uom") or sku.uom
            skus_updated += 1

        # Append-only price history (archive)
        sku_price = SkuPrice(
            sku_id=sku.id,
            price_list_id=price_list.id,
            price=r["list_price"],
            currency=r["currency"],
            effective_from=price_list.effective_from,
            effective_to=price_list.effective_to,
            import_batch_id=batch_id,
            source_file=source_file,
        )
        db.add(sku_price)
        prices_inserted += 1

        # Fast current price snapshot (Option-1)
        sku.current_price = r["list_price"]
        sku.current_currency = r["currency"]
        sku.current_price_updated_at = now

    db.commit()

    summary.update({
        "items_created": items_created,
        "skus_created": skus_created,
        "skus_updated": skus_updated,
        "prices_inserted": prices_inserted,
        "price_list_id": price_list.id,
        "price_list_name": price_list_name,
    })
    return summary


