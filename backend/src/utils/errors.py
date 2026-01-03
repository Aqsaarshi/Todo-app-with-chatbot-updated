from fastapi import HTTPException, status
from typing import Optional
from enum import Enum

class ErrorCode(str, Enum):
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    FORBIDDEN_ACCESS = "FORBIDDEN_ACCESS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

class TodoException(HTTPException):
    def __init__(
        self,
        error_code: ErrorCode,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(status_code=status_code, detail={
            "error": {
                "code": error_code.value,
                "message": detail
            }
        })

def raise_auth_required_error(detail: str = "Authentication required"):
    raise TodoException(
        error_code=ErrorCode.AUTHENTICATION_REQUIRED,
        detail=detail,
        status_code=status.HTTP_401_UNAUTHORIZED
    )

def raise_forbidden_error(detail: str = "Forbidden access"):
    raise TodoException(
        error_code=ErrorCode.FORBIDDEN_ACCESS,
        detail=detail,
        status_code=status.HTTP_403_FORBIDDEN
    )

def raise_not_found_error(detail: str = "Resource not found"):
    raise TodoException(
        error_code=ErrorCode.RESOURCE_NOT_FOUND,
        detail=detail,
        status_code=status.HTTP_404_NOT_FOUND
    )

def raise_validation_error(detail: str = "Validation error"):
    raise TodoException(
        error_code=ErrorCode.VALIDATION_ERROR,
        detail=detail,
        status_code=status.HTTP_400_BAD_REQUEST
    )