"""
Audit Logger
Phase-5: Logs audit events to audit_logs table
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text


class AuditLogger:
    """Static class for logging audit events"""
    
    @staticmethod
    def log_event(
        *,
        db: Session,
        tenant_id: int,
        actor_id: Optional[int],
        action_type: str,
        resource_type: str,
        resource_id: int,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        Log an audit event to the audit_logs table.
        
        Args:
            db: Database session
            tenant_id: Tenant ID
            actor_id: User ID who performed the action (optional)
            action_type: Type of action (e.g., "APPLY_RECALC", "RATE_SET")
            resource_type: Type of resource (e.g., "quotation", "quote_bom_item")
            resource_id: ID of the resource
            old_values: Previous state (optional)
            new_values: New state (optional)
            metadata: Additional metadata (optional)
            ip_address: IP address of the request (optional)
            user_agent: User agent string (optional)
        """
        # Import json for JSONB serialization
        import json
        
        # Convert dicts to JSON strings for JSONB columns
        old_values_json = json.dumps(old_values, default=str) if old_values else None
        new_values_json = json.dumps(new_values, default=str) if new_values else None
        
        # Insert audit log entry
        db.execute(
            text("""
                INSERT INTO audit_logs (
                    tenant_id,
                    user_id,
                    action,
                    resource_type,
                    resource_id,
                    old_values,
                    new_values,
                    ip_address,
                    user_agent
                ) VALUES (
                    :tenant_id,
                    :user_id,
                    :action,
                    :resource_type,
                    :resource_id,
                    :old_values::jsonb,
                    :new_values::jsonb,
                    :ip_address,
                    :user_agent
                )
            """),
            {
                "tenant_id": tenant_id,
                "user_id": actor_id,
                "action": action_type,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "old_values": old_values_json,
                "new_values": new_values_json,
                "ip_address": ip_address,
                "user_agent": user_agent,
            }
        )
        # Note: No commit here - caller controls transaction atomicity

