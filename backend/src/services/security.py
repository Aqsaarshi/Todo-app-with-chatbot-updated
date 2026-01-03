from ..utils.logging import log_security_event
from uuid import UUID
from typing import Optional


def log_access_attempt(user_id: Optional[str], endpoint: str, success: bool, details: dict = None):
    """Log access attempts for security monitoring"""
    event_type = "ACCESS_ATTEMPT_SUCCESS" if success else "ACCESS_ATTEMPT_FAILED"
    log_security_event(
        event_type=event_type,
        user_id=user_id,
        details={
            "endpoint": endpoint,
            "timestamp": str(__import__('datetime').datetime.utcnow()),
            **(details or {})
        }
    )


def log_authentication_event(user_id: str, event_type: str, success: bool, details: dict = None):
    """Log authentication events for security monitoring"""
    event_subtype = "SUCCESS" if success else "FAILED"
    full_event_type = f"AUTHENTICATION_{event_type}_{event_subtype}"

    log_security_event(
        event_type=full_event_type,
        user_id=user_id,
        details={
            "timestamp": str(__import__('datetime').datetime.utcnow()),
            **(details or {})
        }
    )


def log_data_access_violation(attempting_user_id: str, requested_resource_user_id: str, resource_type: str, endpoint: str):
    """Log data access violations for security monitoring"""
    log_security_event(
        event_type="DATA_ACCESS_VIOLATION",
        user_id=attempting_user_id,
        details={
            "requested_resource_user_id": requested_resource_user_id,
            "resource_type": resource_type,
            "endpoint": endpoint,
            "timestamp": str(__import__('datetime').datetime.utcnow())
        }
    )


def validate_user_ownership(requesting_user_id: UUID, resource_user_id: UUID, resource_type: str, endpoint: str) -> bool:
    """Validate that a user has ownership of a resource"""
    is_valid = requesting_user_id == resource_user_id

    if not is_valid:
        log_data_access_violation(
            str(requesting_user_id),
            str(resource_user_id),
            resource_type,
            endpoint
        )

    return is_valid