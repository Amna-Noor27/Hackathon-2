from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
from sqlmodel import Session
from fastapi import HTTPException, status
from jose import JWTError, jwt
from src.models.user import User
from src.core.config import settings
import bcrypt
from src.auth.utils import get_password_hash, verify_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data.
    Uses standardized JWT payload structure for consistency across services.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Use JWT setting if available, otherwise fall back to original setting
        expire_minutes = settings.jwt_access_token_expire_minutes if hasattr(settings, 'jwt_access_token_expire_minutes') else settings.access_token_expire_minutes
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)

    # Standardized JWT payload structure
    token_payload = {
        "sub": data.get("sub", data.get("user_id")),  # Subject (user ID)
        "email": data.get("email", ""),  # User's email
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at time
        "iss": "todo-app",  # Issuer
        "aud": "todo-users",  # Audience
        "role": data.get("role", "user"),  # User role
        "permissions": data.get("permissions", [])  # User permissions
    }

    # Use consistent settings for JWT - prioritize Better Auth settings for compatibility
    secret = getattr(settings, 'better_auth_secret', getattr(settings, 'jwt_secret_key', getattr(settings, 'secret_key', 'your-secret-key-change-in-production')))
    algorithm = getattr(settings, 'jwt_algorithm', getattr(settings, 'algorithm', 'HS256'))
    encoded_jwt = jwt.encode(token_payload, secret, algorithm=algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify the provided token and return the user ID if valid.
    """
    try:
        # Use consistent settings for JWT - prioritize Better Auth settings for compatibility
        secret = getattr(settings, 'better_auth_secret', getattr(settings, 'jwt_secret_key', getattr(settings, 'secret_key', 'your-secret-key-change-in-production')))
        algorithm = getattr(settings, 'jwt_algorithm', getattr(settings, 'algorithm', 'HS256'))

        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm],
            options={"verify_aud": False}  # Don't verify audience as Better Auth tokens may have different audience values
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id, payload  # Also return the full payload
    except JWTError:
        raise credentials_exception


def get_current_user(token: str, session: Session):
    """
    Get the current user from the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id, payload = verify_token(token, credentials_exception)

    # Verify the user exists in the database
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user


def decode_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and return the token payload without validation.
    Use this for inspection purposes only.
    """
    try:
        # Use consistent settings for JWT - prioritize Better Auth settings for compatibility
        secret = getattr(settings, 'better_auth_secret', getattr(settings, 'jwt_secret_key', getattr(settings, 'secret_key', 'your-secret-key-change-in-production')))
        algorithm = getattr(settings, 'jwt_algorithm', getattr(settings, 'algorithm', 'HS256'))
        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm],
            options={"verify_exp": False, "verify_aud": False}  # Don't verify expiration or audience for inspection
        )
        return payload
    except JWTError:
        return None