import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.api.routes import auth
from app.api.routes import portfolio as portfolio_routes
from app.core.config import settings
from app.core.database import col
from app.core.security import decode_access_token, generate_csrf_token

app = FastAPI(
    title="Portfolio CMS",
    docs_url=None,   # Disabled in production
    redoc_url=None,
    openapi_url=None,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Static files & templates ─────────────────────────────────────────────────
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")),
    name="static",
)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ── Secure response headers ───────────────────────────────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers.update(
            {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "geolocation=(), camera=(), microphone=()",
            }
        )
        return response


app.add_middleware(SecurityHeadersMiddleware)

# ── CORS (added last so it is outermost — handles preflight before anything else)
# allow_origins cannot be ["*"] when allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-CSRF-Token"],
)

# ── API routers ───────────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(portfolio_routes.router, prefix="/api", tags=["portfolio"])


# ── Helper: serialize MongoDB docs ────────────────────────────────────────────
def _doc(d: dict) -> dict:
    if d:
        d["id"] = str(d.pop("_id"))
    return d or {}


# ── Public index page (dynamic) ───────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    projects = [_doc(d) for d in await col("projects").find().to_list(None)]
    experience = [_doc(d) for d in await col("experience").find().to_list(None)]

    raw_skills = [_doc(d) for d in await col("skills").find().to_list(None)]
    skills_by_cat: dict = {}
    for s in raw_skills:
        skills_by_cat.setdefault(s.get("cat", "Other"), []).append(s)

    education = [_doc(d) for d in await col("education").find().to_list(None)]
    contact = _doc(await col("contact").find_one({}))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "projects": projects,
            "experience": experience,
            "skills_by_cat": skills_by_cat,
            "all_skills": raw_skills,
            "education": education,
            "contact": contact,
        },
    )


# ── Admin page (server-side auth guard) ──────────────────────────────────────
@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    authenticated = False
    csrf_token = ""

    token = request.cookies.get("access_token")
    if token:
        try:
            decode_access_token(token)
            authenticated = True
            csrf_token = generate_csrf_token()
        except JWTError:
            pass

    is_prod = settings.ENVIRONMENT == "production"
    response = templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "authenticated": authenticated,
            "csrf_token": csrf_token,
        },
    )

    if authenticated:
        # Rotate CSRF cookie on every dashboard load
        response.set_cookie(
            "csrf_token",
            csrf_token,
            httponly=False,
            secure=is_prod,
            samesite="strict",
            max_age=settings.JWT_EXPIRE_HOURS * 3600,
            path="/",
        )

    return response
