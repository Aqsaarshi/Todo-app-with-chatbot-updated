from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from typing import Dict, Any
from ..database import get_session
from ..models.user import User, UserCreate, UserRead
from ..services.auth_service import create_user, authenticate_user
from ..auth.jwt import create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/auth/register", response_model=Dict[str, Any])
async def register(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    """Register a new user"""
    try:
        db_user = await create_user(session, user_create)
        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(db_user.id), "email": db_user.email},
            expires_delta=access_token_expires
        )
        return {
            "user_id": str(db_user.id),
            "token": access_token,
            "message": "User registered successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

@router.post("/auth/login", response_model=Dict[str, Any])
async def login(email: str, password: str, session: AsyncSession = Depends(get_session)):
    """Authenticate user and return access token"""
    try:
        user = await authenticate_user(session, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        return {
            "user_id": str(user.id),
            "token": access_token,
            "message": "Login successful"
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )

@router.post("/auth/logout")
async def logout():
    """Logout user (client-side token invalidation)"""
    return {"message": "Logout successful"}