import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import auth

app = FastAPI()

# Base path fix (VERY IMPORTANT for Vercel)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static & Templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app/static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Include Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Page Route
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# @app.get("/admin", response_class=HTMLResponse)
# async def admin_page(request: Request):
#     return templates.TemplateResponse(request, "admin.html")