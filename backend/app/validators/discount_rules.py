"""
Discount rules permission validator
"""
from typing import List


class DiscountPermissionError(Exception):
    """Raised when user lacks permission for discount operations"""
    pass


def assert_bulk_allowed(user_roles: List[str]) -> None:
    """
    Assert that user has permission for bulk discount operations.
    
    Operator, Reviewer, and Approver roles are allowed.
    
    Args:
        user_roles: List of user role names
        
    Raises:
        DiscountPermissionError: If user lacks required role
    """
    allowed_roles = {"Operator", "Reviewer", "Approver"}
    if not any(role in allowed_roles for role in user_roles):
        raise DiscountPermissionError(
            "Only Operator, Reviewer, and Approver roles can perform bulk discount operations"
        )

