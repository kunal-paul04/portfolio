from pydantic import BaseModel, field_validator


class ProjectIn(BaseModel):
    name: str
    type: str
    cat: str
    tags: list[str]
    url: str
    img: str
    desc: str

    @field_validator("cat")
    @classmethod
    def validate_cat(cls, v: str) -> str:
        if v not in ("personal", "professional"):
            raise ValueError("cat must be 'personal' or 'professional'")
        return v

    @field_validator("name", "type", "desc")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class ExperienceIn(BaseModel):
    role: str
    company: str
    start: str
    end: str
    tags: list[str]
    desc: str

    @field_validator("role", "company")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class SkillIn(BaseModel):
    name: str
    cat: str
    pct: int

    @field_validator("pct")
    @classmethod
    def validate_pct(cls, v: int) -> int:
        if not 0 <= v <= 100:
            raise ValueError("pct must be 0–100")
        return v

    @field_validator("name")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class EducationIn(BaseModel):
    deg: str
    short: str
    inst: str
    year: str
    grade: str

    @field_validator("deg", "inst")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank")
        return v.strip()


class ContactIn(BaseModel):
    name: str
    email: str
    phone1: str
    phone2: str
    location: str
    resume: str
    github: str
    linkedin: str
    available: bool
