from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from models.intro import Intro
from models.resume import Resume
from lib.mongo_lib import database_connection
from schemas.schema import intro_list, intro, certificate_list_entity, certification, skillset_list, skillset, resume, education_list, education, work_list, work, tech_skill_list, tech_skill
from fastapi.templating import Jinja2Templates

route = APIRouter()
conn = database_connection()
templates = Jinja2Templates(directory="templates")


@route.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # to fetch data from a collection, use: <connection_var>.<db name>.<collection name>
    about = conn.portfolio.intro.find({})
    resume = conn.portfolio.resume.find_one({})
    skillset = conn.portfolio.skillset.find({})
    certificates = conn.portfolio.certification.find({})
    education_list = conn.portfolio.education.find({})
    work_list = conn.portfolio.job.find({})
    tech_skill = conn.portfolio.tech_skill.find({})
    return templates.TemplateResponse(request=request, name="index.html", context={"intro": about, "resume": resume, "skillset": skillset, "certificates": certificates, "education_list": education_list, "work_list": work_list, "tech_skill": tech_skill})

