from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import os
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database import get_session
from ..models.user import User


# Initialize security scheme
security = HTTPBearer()


# Get secret key and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "mypassword123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(token: str, db_session: AsyncSession) -> User:
    """
    Verify the JWT token and return the associated user.

    Args:
        token: JWT token to verify
        db_session: Database session

    Returns:
        User object if token is valid

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Convert the user_id from the token to UUID for comparison with the database
    try:
        user_id_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception

    result = await db_session.exec(select(User).where(User.id == user_id_uuid))
    user = result.first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: AsyncSession = Depends(get_session)
) -> User:
    """
    Get the current user based on the JWT token.

    Args:
        credentials: HTTP authorization credentials
        db_session: Database session

    Returns:
        User object
    """
    token = credentials.credentials
    return await verify_token(token, db_session)


async def verify_user_in_path_matches_token(
    user_id: str,  # Changed back to str to let FastAPI handle the conversion properly
    current_user: User = Depends(get_current_user)
) -> bool:
    """
    Verify that the user ID in the path matches the user ID in the token.

    Args:
        user_id: User ID from the path parameter
        current_user: Current user from token

    Returns:
        True if user IDs match

    Raises:
        HTTPException: If user IDs don't match
    """
    # Convert the path user_id to UUID for comparison
    try:
        path_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format"
        )

    # Compare the UUIDs
    if path_user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="User ID in path does not match token"
        )
    return True