"""
Test for FIXED_NO_DISCOUNT excluded from quotation-level discount (G-06)
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
    """
    Very small fake for SQLAlchemy Session.execute(text(...)).
    Returns pre-baked results for:
      1) quotation header SELECT
      2) quote_bom_items SELECT
      3) discount_rules listing (via DiscountRuleLookup -> db)
    """
    def __init__(self, quote_row, line_rows, rules_rows=None):
        self.quote_row = quote_row
        self.line_rows = line_rows
        self.rules_rows = rules_rows or []

    def execute(self, stmt, params=None):
        sql = str(stmt)

        # quotations header fetch
        if "FROM quotations" in sql and "SELECT id, tenant_id" in sql:
            return _Result(first_row=self.quote_row)

        # quote lines fetch
        if "FROM quote_bom_items" in sql and "ORDER BY id ASC" in sql:
            return _Result(rows=self.line_rows)

        # discount rules fetch (DiscountRuleLookup list_active_rules_for_quote)
        if "FROM discount_rules" in sql:
            return _Result(rows=self.rules_rows)

        raise AssertionError(f"Unhandled SQL in FakeDB.execute():\n{sql}")


def test_fixed_no_discount_excluded_from_quotation_discount(monkeypatch):
    """
    Ensure FIXED_NO_DISCOUNT lines:
      - are included in totals
      - do NOT receive quotation-level discount
    Scenario:
      fixed line: 100 × 1  (no discount)
      normal line: 100 × 1 (quotation discount 10%)
    Expected discounted_subtotal = 100 + 90 = 190
    """
    # Patch DiscountRuleLookup to return no rules (keep test focused)
    class _NoRulesLookup:
        def __init__(self, db): ...
        def list_active_rules_for_quote(self, tenant_id, quotation_id):  # noqa: ARG002
            return []

    monkeypatch.setattr(quotation_ep, "DiscountRuleLookup", _NoRulesLookup)

    db = FakeDB(
        quote_row={
            "id": 1,
            "tenant_id": 1,
            "discount_pct": Decimal("10.0"),
            "tax_profile_id": None,
            "tax_mode": None,
        },
        line_rows=[
            {
                "id": 1,
                "product_id": 101,
                "quantity": Decimal("1.000"),
                "rate": Decimal("100.00"),
                "rate_source": "FIXED_NO_DISCOUNT",
                "discount_pct": Decimal("0.00"),
                "discount_source": None,
                "make_id": None,
                "series_id": None,
                "category_id": None,
                "is_price_missing": False,
            },
            {
                "id": 2,
                "product_id": 102,
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

    assert Decimal(out["subtotal"]) == Decimal("200.0000")
    assert Decimal(out["discounted_subtotal"]) == Decimal("190.0000")
    assert Decimal(out["grand_total"]) == Decimal("190.0000")
    assert "HAS_FIXED_NO_DISCOUNT_LINES" in out["flags"]

