from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Import the bcrypt patch to fix compatibility issue
from ..utils import bcrypt_patch

load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Truncate password to 72 characters to comply with bcrypt limit
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    try:
        return pwd_context.verify(truncated_password, hashed_password)
    except ValueError as e:
        # Handle bcrypt password length errors
        if "password cannot be longer than 72 bytes" in str(e):
            # This shouldn't happen due to truncation, but just in case
            return False
        raise e

def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    # Truncate password to 72 characters to comply with bcrypt limit
    truncated_password = password[:72] if len(password) > 72 else password
    try:
        return pwd_context.hash(truncated_password)
    except ValueError as e:
        # Handle bcrypt password length errors
        if "password cannot be longer than 72 bytes" in str(e):
            raise ValueError("Password exceeds maximum length of 72 characters")
        raise e

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a token and return the payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None