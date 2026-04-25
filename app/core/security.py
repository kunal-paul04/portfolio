# app/core/security.py

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = os.getenv("SECRET_KEY")
ALGO = os.getenv("JWT_ALGO")

# 🔒 Password hashing
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# 🔑 JWT
def create_token(data: dict):
    data.update({"exp": datetime.utcnow() + timedelta(hours=3)})
    return jwt.encode(data, SECRET, algorithm=ALGO)

def verify_token(token):
    return jwt.decode(token, SECRET, algorithms=[ALGO])