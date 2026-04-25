# app/routes/auth.py

from fastapi import APIRouter, Form, HTTPException
from app.db.mongo import db
from app.core.security import verify_password, create_token

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    user = await db.users.find_one({"username": username})

    if not user:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(password, user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({"sub": username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }