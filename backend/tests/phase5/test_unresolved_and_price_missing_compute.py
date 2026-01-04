"""
Test for UNRESOLVED and is_price_missing contributing zero (G-03, G-05)
"""
from decimal import Decimal
import pytest

from app.api.v1.endpoints import quotation as quotation_ep


class _Result:
    def __init__(self, rows=None, first_row=None):
        self._rows = rows or []
        self._first = first_row

    def mappings(self):
        return self

    def first(self):
        return self._first

    def all(self):
        return self._rows


class FakeDB:
    def __init__(self, quote_row, line_rows, rules_rows=None):
        self.quote_row = quote_row
        self.line_rows = line_rows
        self.rules_rows = rules_rows or []

    def execute(self, stmt, params=None):
        sql = str(stmt)

        if "FROM quotations" in sql and "SELECT id, tenant_id" in sql:
            return _Result(first_row=self.quote_row)

        if "FROM quote_bom_items" in sql and "ORDER BY id ASC" in sql:
            return _Result(rows=self.line_rows)

        if "FROM discount_rules" in sql:
            return _Result(rows=self.rules_rows)

        raise AssertionError(f"Unhandled SQL in FakeDB.execute():\n{sql}")


def test_unresolved_or_price_missing_contributes_zero(monkeypatch):
    """
    Ensure:
      - rate_source=UNRESOLVED contributes 0
      - is_price_missing=true contributes 0
      - flags are raised for operator visibility
    """
    class _NoRulesLookup:
        def __init__(self, db): ...
        def list_active_rules_for_quote(self, tenant_id, quotation_id):  # noqa: ARG002
            return []

    monkeypatch.setattr(quotation_ep, "DiscountRuleLookup", _NoRulesLookup)

    db = FakeDB(
        quote_row={
            "id": 1,
            "tenant_id": 1,
            "discount_pct": Decimal("0.0"),
            "tax_profile_id": None,
            "tax_mode": None,
        },
        line_rows=[
            {
                "id": 1,
                "product_id": None,
                "quantity": Decimal("5.000"),
                "rate": Decimal("999.00"),
                "rate_source": "UNRESOLVED",
                "discount_pct": Decimal("0.00"),
                "discount_source": None,
                "make_id": None,
                "series_id": None,
                "category_id": None,
                "is_price_missing": False,
            },
            {
                "id": 2,
                "product_id": 202,
                "quantity": Decimal("3.000"),
                "rate": Decimal("500.00"),
                "rate_source": "PRICELIST",
                "discount_pct": Decimal("0.00"),
                "discount_source": None,
                "make_id": None,
                "series_id": None,
                "category_id": None,
                "is_price_missing": True,
            },
            {
                "id": 3,
                "product_id": 203,
                "quantity": Decimal("1.000"),
                "rate": Decimal("100.00"),
                "rate_source": "PRICELIST",
                "discount_pct": Decimal("0.00"),
                "discount_source": None,
                "make_id": None,
                "series_id": None,
                "category_id": None,
                "is_price_missing": False,
            },
        ],
    )

    out = quotation_ep._compute_quote_pricing(db=db, tenant_id=1, quotation_id=1)

    # only the third line counts
    assert Decimal(out["subtotal"]) == Decimal("100.0000")
    assert Decimal(out["discounted_subtotal"]) == Decimal("100.0000")
    assert Decimal(out["grand_total"]) == Decimal("100.0000")

    assert "HAS_UNRESOLVED_LINES" in out["flags"]
    assert "HAS_PRICE_MISSING_LINES" in out["flags"]

