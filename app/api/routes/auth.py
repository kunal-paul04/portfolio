from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login")
async def login(request: Request):
    data = await request.json()
    result = await AuthService.process_login(data)
    return JSONResponse(content=result)