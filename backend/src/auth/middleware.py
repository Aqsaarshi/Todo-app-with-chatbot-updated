from fastapi import Request, HTTPException, status
from typing import Optional
from uuid import UUID
from .jwt import verify_token

async def user_ownership_middleware(request: Request, call_next):
    """
    Middleware to ensure users can only access their own data
    This middleware checks if the user_id in the JWT token matches
    the user_id in the request path parameters
    """
    # Extract token from query parameters or headers
    token = request.query_params.get("token")
    if not token:
        # Try to get token from authorization header
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if token:
        payload = verify_token(token)
        if payload:
            current_user_id = payload.get("sub")
            if current_user_id:
                # Add current user ID to request state for later use
                request.state.current_user_id = UUID(current_user_id)

                # Check if path contains user_id parameter and validate ownership
                path_parts = request.url.path.split("/")
                for i, part in enumerate(path_parts):
                    if part == "tasks" and i > 0:
                        # The previous part should be the user_id
                        try:
                            requested_user_id = UUID(path_parts[i-1])
                            if UUID(current_user_id) != requested_user_id:
                                raise HTTPException(
                                    status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Not authorized to access this resource"
                                )
                        except ValueError:
                            # If it's not a valid UUID, continue
                            pass

    response = await call_next(request)
    return response