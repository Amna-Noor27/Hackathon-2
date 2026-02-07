from fastapi import Depends, HTTPException, status
from src.auth.jwt_middleware import jwt_scheme, get_current_user_id, get_current_user_identity
from typing import Dict, Any


async def get_current_user_id_dep(
    user_id: str = Depends(get_current_user_id)
) -> str:
    """
    Dependency to get the current user ID from the JWT token.
    This ensures that only authenticated users can access protected endpoints.
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user_id


def get_current_user_identity_dep(
    user_identity: Dict[str, Any] = Depends(get_current_user_identity)
) -> Dict[str, Any]:
    """
    Dependency to get the current user identity from the JWT token.
    This includes user ID, email, and any other relevant claims.
    """
    if not user_identity or not user_identity.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user_identity