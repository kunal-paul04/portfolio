from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import col
from app.middleware.auth import csrf_protect, get_current_user
from app.models.portfolio import (
    ContactIn,
    EducationIn,
    ExperienceIn,
    ProjectIn,
    SkillIn,
)

router = APIRouter()

AuthDep = Annotated[dict, Depends(get_current_user)]
CsrfDep = Annotated[None, Depends(csrf_protect)]


def _doc(d: dict) -> dict:
    """Convert a MongoDB document to a JSON-serialisable dict."""
    if d is None:
        return {}
    d["id"] = str(d.pop("_id"))
    return d


def _docs(docs: list) -> list:
    return [_doc(d) for d in docs]


def _oid(item_id: str) -> ObjectId:
    try:
        return ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")


# ── Projects ────────────────────────────────────────────────────────────────

@router.get("/projects")
async def list_projects(_: AuthDep):
    return _docs(await col("projects").find().to_list(None))


@router.post("/projects", status_code=201)
async def create_project(body: ProjectIn, _: AuthDep, __: CsrfDep):
    result = await col("projects").insert_one(body.model_dump())
    return _doc(await col("projects").find_one({"_id": result.inserted_id}))


@router.put("/projects/{item_id}")
async def update_project(item_id: str, body: ProjectIn, _: AuthDep, __: CsrfDep):
    oid = _oid(item_id)
    res = await col("projects").replace_one({"_id": oid}, body.model_dump())
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return _doc(await col("projects").find_one({"_id": oid}))


@router.delete("/projects/{item_id}", status_code=204)
async def delete_project(item_id: str, _: AuthDep, __: CsrfDep):
    res = await col("projects").delete_one({"_id": _oid(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")


# ── Experience ───────────────────────────────────────────────────────────────

@router.get("/experience")
async def list_experience(_: AuthDep):
    return _docs(await col("experience").find().to_list(None))


@router.post("/experience", status_code=201)
async def create_experience(body: ExperienceIn, _: AuthDep, __: CsrfDep):
    result = await col("experience").insert_one(body.model_dump())
    return _doc(await col("experience").find_one({"_id": result.inserted_id}))


@router.put("/experience/{item_id}")
async def update_experience(item_id: str, body: ExperienceIn, _: AuthDep, __: CsrfDep):
    oid = _oid(item_id)
    res = await col("experience").replace_one({"_id": oid}, body.model_dump())
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return _doc(await col("experience").find_one({"_id": oid}))


@router.delete("/experience/{item_id}", status_code=204)
async def delete_experience(item_id: str, _: AuthDep, __: CsrfDep):
    res = await col("experience").delete_one({"_id": _oid(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")


# ── Skills ───────────────────────────────────────────────────────────────────

@router.get("/skills")
async def list_skills(_: AuthDep):
    return _docs(await col("skills").find().to_list(None))


@router.post("/skills", status_code=201)
async def create_skill(body: SkillIn, _: AuthDep, __: CsrfDep):
    result = await col("skills").insert_one(body.model_dump())
    return _doc(await col("skills").find_one({"_id": result.inserted_id}))


@router.put("/skills/{item_id}")
async def update_skill(item_id: str, body: SkillIn, _: AuthDep, __: CsrfDep):
    oid = _oid(item_id)
    res = await col("skills").replace_one({"_id": oid}, body.model_dump())
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return _doc(await col("skills").find_one({"_id": oid}))


@router.delete("/skills/{item_id}", status_code=204)
async def delete_skill(item_id: str, _: AuthDep, __: CsrfDep):
    res = await col("skills").delete_one({"_id": _oid(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")


# ── Education ────────────────────────────────────────────────────────────────

@router.get("/education")
async def list_education(_: AuthDep):
    return _docs(await col("education").find().to_list(None))


@router.post("/education", status_code=201)
async def create_education(body: EducationIn, _: AuthDep, __: CsrfDep):
    result = await col("education").insert_one(body.model_dump())
    return _doc(await col("education").find_one({"_id": result.inserted_id}))


@router.put("/education/{item_id}")
async def update_education(item_id: str, body: EducationIn, _: AuthDep, __: CsrfDep):
    oid = _oid(item_id)
    res = await col("education").replace_one({"_id": oid}, body.model_dump())
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return _doc(await col("education").find_one({"_id": oid}))


@router.delete("/education/{item_id}", status_code=204)
async def delete_education(item_id: str, _: AuthDep, __: CsrfDep):
    res = await col("education").delete_one({"_id": _oid(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")


# ── Contact ──────────────────────────────────────────────────────────────────

@router.get("/contact")
async def get_contact(_: AuthDep):
    doc = await col("contact").find_one({})
    return _doc(doc) if doc else {}


@router.put("/contact")
async def update_contact(body: ContactIn, _: AuthDep, __: CsrfDep):
    existing = await col("contact").find_one({})
    if existing:
        await col("contact").replace_one({"_id": existing["_id"]}, body.model_dump())
    else:
        await col("contact").insert_one(body.model_dump())
    return _doc(await col("contact").find_one({}))
