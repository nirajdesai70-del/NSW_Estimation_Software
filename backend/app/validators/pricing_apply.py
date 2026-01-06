"""
Pricing apply-recalc permission validator
"""
from typing import List


class ApplyRecalcPermissionError(Exception):
    """Raised when user lacks permission to apply recalculation"""
    pass


def assert_apply_recalc_allowed(user_roles: List[str]) -> None:
    """
    Assert that user has permission to apply recalculation.
    
    Only Reviewer and Approver roles are allowed.
    
    Args:
        user_roles: List of user role names
        
    Raises:
        ApplyRecalcPermissionError: If user lacks required role
    """
    allowed_roles = {"Reviewer", "Approver"}
    if not any(role in allowed_roles for role in user_roles):
        raise ApplyRecalcPermissionError(
            "Only Reviewer and Approver roles can apply recalculation"
        )

