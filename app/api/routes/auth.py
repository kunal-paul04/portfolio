from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import col
from app.core.security import (
    create_access_token,
    generate_csrf_token,
    verify_password,
)
from app.middleware.auth import get_current_user

router = APIRouter()

_COOKIE_MAX_AGE = settings.JWT_EXPIRE_HOURS * 3600
_IS_PROD = settings.ENVIRONMENT == "production"


class LoginRequest(BaseModel):
    username: str
    password: str


def _set_auth_cookies(response: JSONResponse, token: str, csrf: str) -> None:
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=_IS_PROD,
        samesite="lax",
        max_age=_COOKIE_MAX_AGE,
        path="/",
    )
    # Non-httponly so JS can read and send as header (double-submit pattern)
    response.set_cookie(
        "csrf_token",
        csrf,
        httponly=False,
        secure=_IS_PROD,
        samesite="strict",
        max_age=_COOKIE_MAX_AGE,
        path="/",
    )


@router.post("/login")
async def login(body: LoginRequest):
    user = await col("users").find_one({"username": body.username})
    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(body.username)
    csrf = generate_csrf_token()

    response = JSONResponse({"status": "success", "username": body.username})
    _set_auth_cookies(response, token, csrf)
    return response


@router.post("/logout")
async def logout():
    response = JSONResponse({"status": "success"})
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("csrf_token", path="/")
    return response


@router.get("/me")
async def me(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"username": current_user["username"]}
