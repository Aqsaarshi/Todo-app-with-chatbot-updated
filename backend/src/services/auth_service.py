from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from ..models.user import User, UserCreate
from ..auth.jwt import get_password_hash, verify_password
from uuid import UUID

async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    user = result.first()
    return user

async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    existing_user = await get_user_by_email(session, user_create.email)
    if existing_user:
        raise ValueError("User with this email already exists")

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        password_hash=hashed_password
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user