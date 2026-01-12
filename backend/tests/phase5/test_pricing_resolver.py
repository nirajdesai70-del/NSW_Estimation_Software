"""
Tests for Pricing Resolver
Phase-5 Commit 1: Rate resolution with override governance
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session

from app.estimation.types import RateSource, LineInput, PriceSnapshot
from app.estimation.pricing_resolver import PricingResolver
from app.validators.override_rules import OverrideValidationError


class MockProductRateLookup:
    """Mock product rate lookup for testing"""

    def __init__(self, rates: dict):
        """
        Initialize with a dict mapping (product_id, quote_id) -> rate
        """
        self.rates = rates

    def get_rate_for_product(self, *, product_id: int, quote_id: int) -> Decimal:
        key = (product_id, quote_id)
        if key not in self.rates:
            raise ValueError(f"No rate found for product_id={product_id}, quote_id={quote_id}")
        return Decimal(str(self.rates[key]))


class TestPricingResolver:
    """Test suite for PricingResolver"""

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        db = MagicMock(spec=Session)
        db.execute = MagicMock()
        db.commit = MagicMock()
        return db

    @pytest.fixture
    def resolver(self, mock_db):
        """Create PricingResolver instance with tenant_id"""
        return PricingResolver(db=mock_db, tenant_id=1)

    @pytest.fixture
    def product_lookup(self):
        """Create mock product lookup with default rates"""
        return MockProductRateLookup({
            (101, 1): 1000.00,
            (102, 1): 2000.00,
        })

    def test_resolve_pricelist_rate_success(self, resolver, product_lookup, mock_db):
        """Test successful PRICELIST rate resolution"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.PRICELIST,
            override_rate=None,
            override_reason=None,
        )

        snapshot = resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Operator"],
            product_rate_lookup=product_lookup,
        )

        assert snapshot.rate_source == RateSource.PRICELIST
        assert snapshot.applied_rate == Decimal("1000.00")
        assert snapshot.sku_rate == Decimal("1000.00")
        assert snapshot.override_rate is None

    def test_resolve_pricelist_does_not_write_db(self, resolver, product_lookup, mock_db):
        """Test PRICELIST resolve does not write to DB (audit happens in snapshot)"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.PRICELIST,
            override_rate=None,
            override_reason=None,
        )

        resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Operator"],
            product_rate_lookup=product_lookup,
        )

        # resolve_line_rate should not write to DB
        assert mock_db.execute.call_count == 0
        assert not mock_db.commit.called

    def test_resolve_pricelist_missing_product_id(self, resolver, product_lookup):
        """Test PRICELIST requires product_id"""
        line = LineInput(
            line_id=1,
            product_id=None,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.PRICELIST,
            override_rate=None,
            override_reason=None,
        )

        with pytest.raises(ValueError, match="product_id is required"):
            resolver.resolve_line_rate(
                quote_id=1,
                line=line,
                user_id=1,
                user_roles=["Operator"],
                product_rate_lookup=product_lookup,
            )

    def test_resolve_manual_override_success(self, resolver, product_lookup, mock_db):
        """Test successful MANUAL override with proper role and reason"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.MANUAL,
            override_rate=Decimal("1500.00"),
            override_reason="Special customer pricing",
        )

        snapshot = resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Reviewer"],
            product_rate_lookup=product_lookup,
        )

        assert snapshot.rate_source == RateSource.MANUAL
        assert snapshot.applied_rate == Decimal("1500.00")
        assert snapshot.override_rate == Decimal("1500.00")
        # resolve_line_rate should not write to DB (audit in snapshot_line_rate)
        assert mock_db.execute.call_count == 0

    def test_resolve_manual_override_operator_denied(self, resolver, product_lookup):
        """Test MANUAL override denied for Operator role"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.MANUAL,
            override_rate=Decimal("1500.00"),
            override_reason="Special customer pricing",
        )

        with pytest.raises(OverrideValidationError, match="requires one of roles"):
            resolver.resolve_line_rate(
                quote_id=1,
                line=line,
                user_id=1,
                user_roles=["Operator"],
                product_rate_lookup=product_lookup,
            )

    def test_resolve_manual_override_missing_reason(self, resolver, product_lookup):
        """Test MANUAL override requires reason"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.MANUAL,
            override_rate=Decimal("1500.00"),
            override_reason=None,
        )

        with pytest.raises(OverrideValidationError, match="override_reason is mandatory"):
            resolver.resolve_line_rate(
                quote_id=1,
                line=line,
                user_id=1,
                user_roles=["Reviewer"],
                product_rate_lookup=product_lookup,
            )

    def test_resolve_manual_override_zero_rate(self, resolver, product_lookup):
        """Test MANUAL override requires positive rate"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.MANUAL,
            override_rate=Decimal("0"),
            override_reason="Test reason",
        )

        with pytest.raises(OverrideValidationError, match="override_rate must be > 0"):
            resolver.resolve_line_rate(
                quote_id=1,
                line=line,
                user_id=1,
                user_roles=["Reviewer"],
                product_rate_lookup=product_lookup,
            )

    def test_resolve_manual_override_approver_allowed(self, resolver, product_lookup, mock_db):
        """Test Approver role can perform manual override"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.MANUAL,
            override_rate=Decimal("1500.00"),
            override_reason="Approved override",
        )

        snapshot = resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Approver"],
            product_rate_lookup=product_lookup,
        )

        assert snapshot.rate_source == RateSource.MANUAL
        assert snapshot.applied_rate == Decimal("1500.00")

    def test_snapshot_line_rate(self, resolver, mock_db):
        """Test rate snapshot persistence with audit"""
        # Mock the SELECT query for old_values
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = {
            "rate_source": "PRICELIST",
            "rate": Decimal("1000.00"),
            "override_rate": None,
            "override_reason": None,
        }
        mock_db.execute.return_value = mock_result

        snapshot = PriceSnapshot(
            sku_rate=Decimal("1000.00"),
            override_rate=None,
            applied_rate=Decimal("1000.00"),
            rate_source=RateSource.PRICELIST,
        )

        resolver.snapshot_line_rate(
            quote_id=1,
            line_id=1,
            snapshot=snapshot,
            actor_id=1,
        )

        # Verify update was called (SELECT + UPDATE + INSERT audit)
        assert mock_db.execute.call_count >= 2  # SELECT + UPDATE + audit INSERT
        # Note: commit removed from snapshot_line_rate (caller controls atomicity)
        # But we still verify it was NOT called since caller should do it
        assert not mock_db.commit.called

    def test_snapshot_manual_override_with_audit(self, resolver, mock_db):
        """Test manual override snapshot includes audit"""
        # Mock the SELECT query for old_values
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = {
            "rate_source": "PRICELIST",
            "rate": Decimal("1000.00"),
            "override_rate": None,
            "override_reason": None,
        }
        mock_db.execute.return_value = mock_result

        snapshot = PriceSnapshot(
            sku_rate=Decimal("1000.00"),
            override_rate=Decimal("1500.00"),
            applied_rate=Decimal("1500.00"),
            rate_source=RateSource.MANUAL,
        )

        resolver.snapshot_line_rate(
            quote_id=1,
            line_id=1,
            snapshot=snapshot,
            actor_id=1,
            override_reason="Special pricing",
            product_id=101,
        )

        # Should have SELECT (old_values) + UPDATE + INSERT (audit)
        assert mock_db.execute.call_count >= 3
        # Note: commit removed (caller controls atomicity)
        assert not mock_db.commit.called

    def test_determinism_same_input_same_output(self, resolver, product_lookup, mock_db):
        """Test determinism: same input produces same output"""
        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.PRICELIST,
            override_rate=None,
            override_reason=None,
        )

        snapshot1 = resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Operator"],
            product_rate_lookup=product_lookup,
        )

        snapshot2 = resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Operator"],
            product_rate_lookup=product_lookup,
        )

        assert snapshot1.applied_rate == snapshot2.applied_rate
        assert snapshot1.rate_source == snapshot2.rate_source

    def test_decimal_quantization(self, resolver):
        """Test that rates are quantized to 4 decimal places"""
        # Create lookup with imprecise rate
        lookup = MockProductRateLookup({
            (101, 1): 1000.123456789,  # Will be quantized to 1000.1235
        })

        line = LineInput(
            line_id=1,
            product_id=101,
            qty=Decimal("2.0"),
            item_discount_pct=Decimal("10.0"),
            rate_source=RateSource.PRICELIST,
            override_rate=None,
            override_reason=None,
        )

        snapshot = resolver.resolve_line_rate(
            quote_id=1,
            line=line,
            user_id=1,
            user_roles=["Operator"],
            product_rate_lookup=lookup,
        )

        # Should be quantized to 4 decimal places
        assert snapshot.applied_rate == Decimal("1000.1235")
