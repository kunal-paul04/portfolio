from fastapi import Request, HTTPException, status
from jose import JWTError

from app.core.database import col
from app.core.security import decode_access_token, csrf_tokens_equal


async def get_current_user(request: Request) -> dict:
    """FastAPI dependency — validates JWT cookie and returns the user document."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub", "")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
        )

    user = await col("users").find_one({"username": username}, {"password": 0})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def csrf_protect(request: Request) -> None:
    """FastAPI dependency — validates the CSRF double-submit cookie on mutating requests."""
    csrf_cookie = request.cookies.get("csrf_token", "")
    csrf_header = request.headers.get("X-CSRF-Token", "")
    if not csrf_tokens_equal(csrf_cookie, csrf_header):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF validation failed",
        )
