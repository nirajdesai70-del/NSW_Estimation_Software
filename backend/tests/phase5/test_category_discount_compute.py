"""
Tests for Category Discount Computation
Phase-5 P0-N2: Verify category discount rules apply correctly with precedence
"""
from unittest.mock import MagicMock, patch
from decimal import Decimal

from app.api.v1.endpoints import quotation as quotation_ep
from app.estimation.discount_rule_types import DiscountRule, DiscountScope


def _mk_db_side_effect(quotation_row, lines, rules):
    """
    Helper to create a mock DB that returns quotation, lines, and rules.
    
    Args:
        quotation_row: Dict for quotation query result
        lines: List of dicts for lines query result
        rules: List of DiscountRule objects (will be returned by DiscountRuleLookup)
    """
    db = MagicMock()

    # Quotation query result
    qres = MagicMock()
    qres.mappings.return_value.first.return_value = quotation_row

    # Lines query result
    lres = MagicMock()
    lres.mappings.return_value.all.return_value = lines

    # db.execute is called for quotation and lines
    db.execute.side_effect = [qres, lres]

    # Rules are loaded via DiscountRuleLookup, so we patch that
    return db, rules


def test_category_rule_applies_when_no_make_series_match():
    """
    Verify category discount applies when no make/series match exists.
    
    Scenario:
    - Line has category_id=5, no make/series
    - Category rule exists: category:5 => 10%
    - Expected: subtotal reflects 10% category discount
    """
    tenant_id = 1
    quotation_id = 1

    quotation_row = {
        "id": quotation_id,
        "tenant_id": tenant_id,
        "discount_pct": Decimal("0.00"),
        "tax_profile_id": None,
        "tax_mode": None,
    }

    # one line: category_id=5, no make/series => CATEGORY should apply
    lines = [{
        "id": 10,
        "sku_id": 101,
        "quantity": Decimal("2"),
        "rate": Decimal("1000"),
        "rate_source": "PRICELIST",
        "discount_pct": None,
        "discount_source": None,
        "make_id": None,
        "series_id": None,
        "category_id": 5,
    }]

    # category:5 => 10%
    rules = [
        DiscountRule(
            id=1,
            tenant_id=tenant_id,
            quotation_id=quotation_id,
            scope_type=DiscountScope.CATEGORY,
            scope_key="category:5",
            discount_pct=Decimal("10.00"),
            is_active=True,
            reason=None,
            created_by=None,
            created_at=None,
        )
    ]

    db, rules_list = _mk_db_side_effect(quotation_row, lines, rules)

    # Patch DiscountRuleLookup to return our rules
    with patch.object(quotation_ep.DiscountRuleLookup, 'list_active_rules_for_quote', return_value=rules_list):
        out = quotation_ep._compute_quote_pricing(
            db=db,
            tenant_id=tenant_id,
            quotation_id=quotation_id
        )

    # base subtotal = 2*1000 = 2000
    # category 10% => 1800
    assert out["subtotal"] == "1800.0000"


def test_make_series_overrides_category():
    """
    Verify make/series discount takes precedence over category discount.
    
    Scenario:
    - Line has both make_id/series_id and category_id
    - Rules exist for both make/series (20%) and category (10%)
    - Expected: make/series 20% discount wins
    """
    tenant_id = 1
    quotation_id = 1

    quotation_row = {
        "id": quotation_id,
        "tenant_id": tenant_id,
        "discount_pct": Decimal("0.00"),
        "tax_profile_id": None,
        "tax_mode": None,
    }

    # line has both make/series and category => MAKE_SERIES should win
    lines = [{
        "id": 10,
        "sku_id": 101,
        "quantity": Decimal("2"),
        "rate": Decimal("1000"),
        "rate_source": "PRICELIST",
        "discount_pct": None,
        "discount_source": None,
        "make_id": 1,
        "series_id": 2,
        "category_id": 5,
    }]

    # make:1|series:2 => 20% (should win)
    # category:5 => 10% (should lose)
    r_make = DiscountRule(
        id=1,
        tenant_id=tenant_id,
        quotation_id=quotation_id,
        scope_type=DiscountScope.MAKE_SERIES,
        scope_key="make:1|series:2",
        discount_pct=Decimal("20.00"),
        is_active=True,
        reason=None,
        created_by=None,
        created_at=None,
    )
    r_cat = DiscountRule(
        id=2,
        tenant_id=tenant_id,
        quotation_id=quotation_id,
        scope_type=DiscountScope.CATEGORY,
        scope_key="category:5",
        discount_pct=Decimal("10.00"),
        is_active=True,
        reason=None,
        created_by=None,
        created_at=None,
    )

    db, rules_list = _mk_db_side_effect(quotation_row, lines, [r_make, r_cat])

    with patch.object(quotation_ep.DiscountRuleLookup, 'list_active_rules_for_quote', return_value=rules_list):
        out = quotation_ep._compute_quote_pricing(
            db=db,
            tenant_id=tenant_id,
            quotation_id=quotation_id
        )

    # base subtotal = 2000
    # make/series 20% => 1600
    assert out["subtotal"] == "1600.0000"


def test_category_rule_falls_back_to_site():
    """
    Verify that if category_id is NULL, category discount doesn't apply; SITE should.
    
    Scenario:
    - Line has category_id=None
    - Category rule exists but can't match
    - Site rule exists (5%)
    - Expected: site discount applies
    """
    tenant_id = 1
    quotation_id = 1

    quotation_row = {
        "id": quotation_id,
        "tenant_id": tenant_id,
        "discount_pct": Decimal("0.00"),
        "tax_profile_id": None,
        "tax_mode": None,
    }

    lines = [{
        "id": 10,
        "sku_id": 101,
        "quantity": Decimal("2"),
        "rate": Decimal("1000"),
        "rate_source": "PRICELIST",
        "discount_pct": None,
        "discount_source": None,
        "make_id": None,
        "series_id": None,
        "category_id": None,  # missing
    }]

    r_site = DiscountRule(
        id=9,
        tenant_id=tenant_id,
        quotation_id=quotation_id,
        scope_type=DiscountScope.SITE,
        scope_key="site",
        discount_pct=Decimal("5.00"),
        is_active=True,
        reason=None,
        created_by=None,
        created_at=None,
    )

    db, rules_list = _mk_db_side_effect(quotation_row, lines, [r_site])

    with patch.object(quotation_ep.DiscountRuleLookup, 'list_active_rules_for_quote', return_value=rules_list):
        out = quotation_ep._compute_quote_pricing(
            db=db,
            tenant_id=tenant_id,
            quotation_id=quotation_id
        )

    # base subtotal = 2000
    # site 5% => 1900
    assert out["subtotal"] == "1900.0000"

