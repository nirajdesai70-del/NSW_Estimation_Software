"""
Override rules validator
Phase-5: Manual override governance checks
"""
from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from app.estimation.types import RateSource


class OverrideValidationError(ValueError):
    """Raised when a manual override request violates governance rules."""


class OverrideRulesValidator:
    """Validates manual override requests for pricing."""

    @staticmethod
    def validate_override_request(
        *,
        rate_source: RateSource,
        override_rate: Decimal | None,
        override_reason: str | None,
        user_roles: Iterable[str],
    ) -> None:
        if rate_source != RateSource.MANUAL:
            return

        allowed_roles = {"Reviewer", "Approver"}
        if not any(role in allowed_roles for role in user_roles):
            raise OverrideValidationError("MANUAL override requires one of roles: Reviewer, Approver")

        if not override_reason:
            raise OverrideValidationError("override_reason is mandatory for MANUAL override")

        if override_rate is None or Decimal(str(override_rate)) <= 0:
            raise OverrideValidationError("override_rate must be > 0 for MANUAL override")

