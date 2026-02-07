from fastapi import Request, HTTPException, status, Depends
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from src.core.config import settings
from typing import Optional, Dict, Any
import logging
import datetime

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    """
    JWT Bearer token authentication scheme using Better Auth secret.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Verify the JWT token from the request and extract user identity.
        Tries to get the token from Authorization header first, then from cookies.
        """
        token = None

        # First, try to get the token from the Authorization header
        if hasattr(request, "headers") and "authorization" in request.headers:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication scheme."
                    )
                token = credentials.credentials
        elif hasattr(request, "headers") and "Authorization" in request.headers:
            # Alternative header capitalization
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "")

        # If not found in headers, try to get from cookies (Better Auth may store token in cookies)
        if not token and hasattr(request, "cookies"):
            if "better-auth-session" in request.cookies:
                token = request.cookies.get("better-auth-session")
            elif "token" in request.cookies:
                token = request.cookies.get("token")
            elif "__Secure-authjs.session-token" in request.cookies:
                # Common cookie name for auth.js based systems
                token = request.cookies.get("__Secure-authjs.session-token")
            elif "authjs.session-token" in request.cookies:
                # Alternative cookie name
                token = request.cookies.get("authjs.session-token")

        if token:
            user_data = self.verify_jwt_and_extract_user_data(token)

            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired token."
                )

            # Add user data to request state for later use
            request.state.user_id = user_data.get("user_id")
            request.state.user_email = user_data.get("email")
            request.state.token_payload = user_data.get("payload")
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code or missing token."
            )

    def verify_jwt_and_extract_user_data(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify the JWT token using BETTER_AUTH_SECRET and return user data if valid.
        """
        try:
            # Use BETTER_AUTH_SECRET for token verification
            secret = settings.better_auth_secret
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"],
                options={"verify_aud": False}  # Don't verify audience as Better Auth tokens may have different audience values
            )

            # Better Auth typically puts user_id in "sub" field
            user_id: str = payload.get("sub")
            if not user_id:
                # If sub is not present, check for other possible fields
                user_id = payload.get("user_id", payload.get("id"))

            email: str = payload.get("email", "")

            if user_id:
                return {
                    "user_id": user_id,
                    "email": email,
                    "payload": payload
                }
            return None
        except JWTError as e:
            logger.error(f"JWT verification error: {e}")
            return None


def create_access_token(data: dict, expires_delta=None):
    """
    Create a new access token with the provided data.
    """
    import datetime
    to_encode = data.copy()

    # Calculate expiration
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        # Default to 240 minutes if not specified
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.jwt_access_token_expire_minutes)

    to_encode.update({"exp": expire})

    # Use BETTER_AUTH_SECRET for token creation
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm=settings.algorithm)
    return encoded_jwt


# Create an instance of the JWT Bearer scheme
jwt_scheme = JWTBearer()


def get_current_user_id(token: str = Depends(jwt_scheme)) -> str:
    """
    Dependency to extract the current user ID from the JWT token.
    This ensures that only authenticated users can access protected endpoints.
    """
    # The token has already been validated by the jwt_scheme
    # We need to decode it again to extract the user ID
    try:
        secret = settings.better_auth_secret
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"verify_aud": False}  # Don't verify audience as Better Auth tokens may have different audience values
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user_identity(token: str = Depends(jwt_scheme)) -> Dict[str, Any]:
    """
    Dependency to extract the full user identity from the JWT token.
    This includes user ID, email, and any other relevant claims.
    """
    try:
        secret = settings.better_auth_secret
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"verify_aud": False}  # Don't verify audience as Better Auth tokens may have different audience values
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        user_identity = {
            "user_id": user_id,
            "email": payload.get("email", ""),
            "name": payload.get("name", ""),
            "role": payload.get("role", "user"),
            "permissions": payload.get("permissions", []),
            "issuer": payload.get("iss", ""),
            "payload": payload
        }

        return user_identity
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )