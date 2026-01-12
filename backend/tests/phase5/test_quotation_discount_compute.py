"""
Tests for Quotation-Level Discount Computation
Phase-5 P0-N1: Verify quotation discount_pct affects pricing totals
"""
import pytest
from unittest.mock import MagicMock
from decimal import Decimal

from app.api.v1.endpoints import quotation as quotation_ep


def test_compute_quote_pricing_applies_quotation_discount(monkeypatch):
    """
    Verify that quotation-level discount_pct from DB is applied correctly.
    
    Scenario:
    - Quotation has discount_pct=5.00
    - One line: qty=2, rate=1000, no line discount
    - Expected: subtotal=2000, discounted_subtotal=1900 (5% off)
    """
    db = MagicMock()
    tenant_id = 1
    quotation_id = 1

    # quotation row includes discount_pct=5
    qrow = MagicMock()
    qrow.mappings.return_value.first.return_value = {
        "id": quotation_id,
        "tenant_id": tenant_id,
        "discount_pct": Decimal("5.00"),
        "tax_profile_id": None,
        "tax_mode": None,
    }

    # one line: qty=2, rate=1000, no line discount
    lrow = MagicMock()
    lrow.mappings.return_value.all.return_value = [{
        "id": 10,
        "sku_id": 101,
        "quantity": Decimal("2"),
        "rate": Decimal("1000"),
        "rate_source": "PRICELIST",
        "discount_pct": None,
        "discount_source": None,
        "make_id": None,
        "series_id": None,
    }]

    # discount rules empty
    rrow = MagicMock()
    rrow.mappings.return_value.all.return_value = []

    # execute order: quotation select, lines select, rules select
    db.execute.side_effect = [qrow, lrow, rrow]

    # Call compute helper
    out = quotation_ep._compute_quote_pricing(
        db=db,
        tenant_id=tenant_id,
        quotation_id=quotation_id
    )

    # subtotal = 2*1000 = 2000
    assert out["subtotal"] == "2000.0000"
    # quote discount 5% -> 1900
    assert out["discounted_subtotal"] == "1900.0000"
    # Verify discount_pct is included in output
    assert Decimal(out["quotation_discount_pct"]) == Decimal("5.00")


def test_compute_quote_pricing_with_zero_discount(monkeypatch):
    """
    Verify that discount_pct=0 (default) works correctly.
    
    Scenario:
    - Quotation has discount_pct=0
    - One line: qty=1, rate=500
    - Expected: subtotal=discounted_subtotal=500
    """
    db = MagicMock()
    tenant_id = 1
    quotation_id = 2

    qrow = MagicMock()
    qrow.mappings.return_value.first.return_value = {
        "id": quotation_id,
        "tenant_id": tenant_id,
        "discount_pct": Decimal("0"),
        "tax_profile_id": None,
        "tax_mode": None,
    }

    lrow = MagicMock()
    lrow.mappings.return_value.all.return_value = [{
        "id": 20,
        "sku_id": 102,
        "quantity": Decimal("1"),
        "rate": Decimal("500"),
        "rate_source": "PRICELIST",
        "discount_pct": None,
        "discount_source": None,
        "make_id": None,
        "series_id": None,
    }]

    rrow = MagicMock()
    rrow.mappings.return_value.all.return_value = []

    db.execute.side_effect = [qrow, lrow, rrow]

    out = quotation_ep._compute_quote_pricing(
        db=db,
        tenant_id=tenant_id,
        quotation_id=quotation_id
    )

    assert out["subtotal"] == "500.0000"
    assert out["discounted_subtotal"] == "500.0000"
    assert Decimal(out["quotation_discount_pct"]) == Decimal("0")


def test_compute_quote_pricing_with_null_discount_defaults_to_zero(monkeypatch):
    """
    Verify that NULL discount_pct defaults to 0.
    
    Scenario:
    - Quotation has discount_pct=None (should default to 0)
    - One line: qty=1, rate=1000
    - Expected: subtotal=discounted_subtotal=1000
    """
    db = MagicMock()
    tenant_id = 1
    quotation_id = 3

    qrow = MagicMock()
    qrow.mappings.return_value.first.return_value = {
        "id": quotation_id,
        "tenant_id": tenant_id,
        "discount_pct": None,  # NULL in DB
        "tax_profile_id": None,
        "tax_mode": None,
    }

    lrow = MagicMock()
    lrow.mappings.return_value.all.return_value = [{
        "id": 30,
        "sku_id": 103,
        "quantity": Decimal("1"),
        "rate": Decimal("1000"),
        "rate_source": "PRICELIST",
        "discount_pct": None,
        "discount_source": None,
        "make_id": None,
        "series_id": None,
    }]

    rrow = MagicMock()
    rrow.mappings.return_value.all.return_value = []

    db.execute.side_effect = [qrow, lrow, rrow]

    out = quotation_ep._compute_quote_pricing(
        db=db,
        tenant_id=tenant_id,
        quotation_id=quotation_id
    )

    assert out["subtotal"] == "1000.0000"
    assert out["discounted_subtotal"] == "1000.0000"
    assert Decimal(out["quotation_discount_pct"]) == Decimal("0")

